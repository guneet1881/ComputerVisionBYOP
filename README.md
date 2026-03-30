# Smart Document Scanner

This is an OpenCV-based pipeline for finding, cropping, and enhancing documents (e.g., notes, receipts) in photos to resemble a top-down document scan.

## Requirements
Ensure you have Python 3 installed. Install the dependencies using:

```bash
pip install -r requirements.txt
```

## Usage

This project is completely CLI-driven. You can run the following command to scan an image:

```bash
python scanner.py --image <path_to_image> --output <path_to_save_output.png>
```

**Example:**
```bash
python scanner.py --image images/receipt.jpg --output processed/scan.png
```

## How it works

1. **Edge Detection:** The image is converted to grayscale, blurred slightly to remove noise, and passed through a Canny Edge Detector.
2. **Contour Finding:** We find contours (curves) in the edge map. We sort them by area and assume the largest contour with exactly 4 points is our document.
3. **Perspective Transformation:** We use OpenCV's perspective functions to perform a "homography", mapping the angled document to a flat top-down view.
4. **Enhancement:** The image is thresholded to look like a black-and-white scan.
