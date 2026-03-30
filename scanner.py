import cv2
import argparse
import imutils
import numpy as np
from skimage.filters import threshold_local
from transform import extract_birdseye_view
import os
from PIL import Image

class DocumentProcessor:
    """
    A unified class that encapsulates the lifecycle of digesting a raw photograph
    and morphing it into a clean, top-down enhanced documentary scan.
    """
    def __init__(self, image_path, target_height_res=500):
        self.raw_image_path = image_path
        self.height_resolution = target_height_res
        self.reference_image = None
        self.scaled_clone = None
        self.scaling_ratio = 1.0

    def load_and_scale(self):
        """Loads physical file and pre-scales it to optimize detection processing."""
        if not os.path.exists(self.raw_image_path):
            raise FileNotFoundError(f"Missing file at payload location: {self.raw_image_path}")
            
        disk_image = cv2.imread(self.raw_image_path)
        self.scaling_ratio = disk_image.shape[0] / float(self.height_resolution)
        self.reference_image = disk_image.copy()
        self.scaled_clone = imutils.resize(disk_image, height=self.height_resolution)
        
        return self

    def _locate_document_perimeter(self):
        """Builds a high-contrast edge map and traces bounding geometries."""
        # Convert to a single channel spectrum and blur away minor grit 
        # before passing it through the Canny morphological edge trace limit
        monochrome = cv2.cvtColor(self.scaled_clone, cv2.COLOR_BGR2GRAY)
        smoothed = cv2.GaussianBlur(monochrome, (5, 5), 0)
        edge_map = cv2.Canny(smoothed, 75, 200)

        # Detect raw polygon lines within the map topology
        candidate_contours = cv2.findContours(edge_map.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        candidate_contours = imutils.grab_contours(candidate_contours)
        
        # Sort out noise; we only need to look at major geometric entities
        top_candidates = sorted(candidate_contours, key=cv2.contourArea, reverse=True)[:5]
        
        document_corners = None
        
        for contour in top_candidates:
            # Approximate the curve behavior into defined segments
            perimeter_length = cv2.arcLength(contour, True)
            geometric_approximation = cv2.approxPolyDP(contour, 0.02 * perimeter_length, True)

            # A standard document outline will collapse into precisely a 4-vertex quadrilateral
            if len(geometric_approximation) == 4:
                document_corners = geometric_approximation
                break
                
        return document_corners

    def execute_pipeline(self):
        """Runs the fully integrated pipeline end-to-end to yield a finalized scan matrix."""
        print("[*] Commencing document localization routines.")
        document_corners = self._locate_document_perimeter()
        
        if document_corners is None:
            print("[!] Warning: Document corners undetected. Using flat image fallback.")
            flattened_scan = self.reference_image
        else:
            print("[+] Target document boundaries established.")
            # Map coordinates from the scaled working space back to the high-res base
            mapped_corners = document_corners.reshape(4, 2) * self.scaling_ratio
            flattened_scan = extract_birdseye_view(self.reference_image, mapped_corners)

        print("[*] Transitioning to local adaptive enhancement protocol.")
        
        base_grayscale = cv2.cvtColor(flattened_scan, cv2.COLOR_BGR2GRAY)
        
        # New Feature Addition: 
        # CLAHE (Contrast Limited Adaptive Histogram Equalization) is used to drastically reduce
        # environmental gradient shadows while accentuating dark ink text over standard local thresholds.
        clahe_optimizer = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        optimized_base = clahe_optimizer.apply(base_grayscale)

        local_block_thresholding = threshold_local(optimized_base, 11, offset=10, method="gaussian")
        final_enhanced_binaurized = (optimized_base > local_block_thresholding).astype("uint8") * 255
        
        return final_enhanced_binaurized

def export_to_disk(rendered_data, output_path, export_pdf=True):
    """Handles the writing procedures from runtime memory directly to I/O interfaces."""
    base_dir = os.path.dirname(output_path)
    if base_dir and not os.path.exists(base_dir):
        os.makedirs(base_dir, exist_ok=True)
        
    cv2.imwrite(output_path, rendered_data)
    print(f"[SUCCESS] Native PNG snapshot secured at: {output_path}")

    if export_pdf:
        # Generate companion PDF file using PIL
        pdf_path = output_path.rsplit('.', 1)[0] + '.pdf'
        # Convert from BGR cv2 to PIL compatible RGB layout, although image is technically grayscale
        converted_rgb = cv2.cvtColor(rendered_data, cv2.COLOR_GRAY2RGB)
        pil_instance = Image.fromarray(converted_rgb)
        pil_instance.save(pdf_path, "PDF", resolution=100.0)
        print(f"[SUCCESS] Portable Document representation generated at: {pdf_path}")

def main():
    cli_parser = argparse.ArgumentParser(description="Object Oriented CLI Document Morphing Pipeline")
    cli_parser.add_argument("-i", "--image", required=True, help="Absolute or relative file payload location")
    cli_parser.add_argument("-o", "--output", required=True, help="Designated file system trajectory for writing")
    args = vars(cli_parser.parse_args())

    try:
        app_instance = DocumentProcessor(args["image"])
        app_instance.load_and_scale()
        final_payload = app_instance.execute_pipeline()
        
        export_to_disk(final_payload, args["output"], export_pdf=True)
        
    except Exception as hardware_error:
        print(f"[SYSTEM FAILURE] Run terminated: {str(hardware_error)}")

if __name__ == "__main__":
    main()
