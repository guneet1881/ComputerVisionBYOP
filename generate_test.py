import cv2
import numpy as np
import os

def create_synthetic_receipt():
    # 1. Create a white background for the receipt
    receipt = np.ones((600, 400, 3), dtype=np.uint8) * 255
    
    # Add some text to it
    cv2.putText(receipt, "XYZ GROCERY STORE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    cv2.putText(receipt, "Bread .............. $2.99", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    cv2.putText(receipt, "Milk ............... $1.99", (30, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    cv2.putText(receipt, "Eggs ............... $3.49", (30, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    cv2.putText(receipt, "Total .............. $8.47", (30, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    cv2.putText(receipt, "THANK YOU!", (120, 500), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    # 2. Apply a random perspective transform to simulate a badly angled photo
    # Source points (corners of the receipt)
    h, w = receipt.shape[:2]
    src_pts = np.array([[0, 0], [w, 0], [w, h], [0, h]], dtype=np.float32)
    
    # Destination points (simulate tilting and perspective)
    dst_pts = np.array([
        [w*0.2, h*0.1], 
        [w*0.8, h*0.2], 
        [w*0.9, h*0.9], 
        [w*0.1, h*0.8]
    ], dtype=np.float32)
    
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    
    # 3. Create a dark "table" background
    table = np.ones((800, 600, 3), dtype=np.uint8) * 50  # Dark gray/brownish
    
    warped_receipt = cv2.warpPerspective(receipt, M, (600, 800), borderMode=cv2.BORDER_CONSTANT, borderValue=(50, 50, 50))
    
    # 4. Save the synthetic image
    os.makedirs('images', exist_ok=True)
    cv2.imwrite('images/test_receipt.jpg', warped_receipt)
    print("Generated images/test_receipt.jpg")

if __name__ == "__main__":
    create_synthetic_receipt()
