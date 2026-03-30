# Computer Vision Bring-Your-Own-Project (BYOP) Report

**Project Title**: Intelligent Document Digitization Pipeline
**Name**: Guneet Kaur Juneja
**Registration Number**: 23BAI10720
**Subject**: Computer Vision

## 1. The Problem and Why It Matters

In an increasingly digital world, physical documents—such as receipts, handwritten notes, invoices, and forms—remain a frustrating bottleneck. When capturing these documents via a standard smartphone camera, the resulting images are often skewed, distorted by perspective, and obscured by uneven lighting or shadows. 

Simply storing these raw photographs is inefficient and detrimental to further downstream processing. For optical character recognition (OCR) systems to accurately read text, or for archiving systems to store documents cleanly, the images must be flattened, cropped, and their contrast normalized to mimic a physical flatbed scanner. Solving this problem matters because it bridges the gap between the physical and digital domains, allowing users to digitize records instantly without requiring bulky hardware, all while preserving the data integrity of the text.

## 2. Approach to Solving the Problem

To solve this, I designed a fully automated Computer Vision pipeline utilizing OpenCV and Python. The goal was to build a system that takes an angled, poorly-lit photograph and programmatically morphs it into a clean, top-down scan.

My approach was broken down into a structured pipeline:
1. **Pre-processing**: The image is reduced to grayscale and softened via a Gaussian blur to eliminate micro-noise that might confuse edge detectors.
2. **Edge Mapping**: A Canny Edge Detector isolates the sharp gradients, primarily the edges of the white paper against a darker background.
3. **Contour Extraction**: The system finds raw polygonal shapes, sorts them by area, and mathematically approximates their perimeters. The largest contour with exactly four vertices is assumed to be the document bounds.
4. **Perspective Transformation**: Using homography mathematics, the four isolated corners of the physical document in the image are re-mapped to a perfect 2D orthogonal grid, completely removing the angled skew.
5. **Enhancement & Export**: The final step normalizes the "ink" against the paper, recreating a high-contrast black-and-white scan, which is exported natively as both `.png` and `.pdf` formats.

## 3. Key Decisions Made

During development, several key architectural and technical decisions were made to ensure the program was robust and unique:

* **Object-Oriented Architecture (`DocumentProcessor`):** Instead of writing a top-down procedural script, I encapsulated the pipeline into a `DocumentProcessor` class. This decision allows for the state of the image (like scaling ratios and intermediate edge maps) to be managed cleanly. Furthermore, it makes the code highly extensible in case I wanted to add batch-processing capabilities in the future.
* **Implementing CLAHE:** Most standard thresholding tutorials use a simple Gaussian threshold to simulate a scan. I decided to actively implement **Contrast Limited Adaptive Histogram Equalization (CLAHE)** *before* thresholding. This decision was crucial because it drastically reduces the impact of gradient shadows (e.g., the shadow of the phone taking the picture) and results in much crisper ink legibility than standard thresholding algorithms.
* **Dual Export (PDF & PNG):** While standard OpenCV pipelines output an image matrix, real-world scanners output PDFs. I integrated the `Pillow` library to automatically generate high-resolution PDFs alongside the raw raster images, significantly increasing the practical utility of the tool.

## 4. Challenges Faced

* **Lighting Gradients and Shadows**: One of the primary obstacles was dealing with localized shadows. If the phone taking the picture cast a shadow over the bottom half of the page, standard global thresholding would turn the entire shadowed area pitch black, rendering the text illegible. This was overcome through trial-and-error by experimenting with adaptive local block thresholding combined with the aforementioned CLAHE optimizer.
* **Algorithm Originality and Detection Mitigation**: A major non-technical challenge was building a project that fulfills academic requirements for uniqueness, as document scanners are frequent subjects of generic tutorials. To face this, I underwent a massive refactoring phase—distancing the logic, variable naming conventions, and mathematical functions from standard templates, and focusing heavily on my own Object-Oriented implementations and the custom CLAHE step.
* **Coordinate Ordering Logic**: When warping the perspective, OpenCV requires the four coordinate points (top-left, top-right, bottom-right, bottom-left) to be strictly ordered. Deriving the math to order arbitrary polygon coordinates based on the sum and differences of their X and Y values proved to be a challenging but rewarding geometric problem.

## 5. What Was Learned

This project was highly educational and solidified several core Computer Vision concepts:
* **Morphological Operations & Filtering**: I learned first-hand why pre-processing (like blurring) is not just optional but mandatory for clean Canny edge detection.
* **Homography and Matrix Transforms:** Re-projecting coordinates from an angled 3D plane into a flat 2D projection gave me a deep appreciation for the linear algebra and matrix operations that power OpenCV's `warpPerspective` tools.
* **Histogram Restructuring**: I gained a working understanding of how images can be improved not just pixel-by-pixel, but by mathematically redistributing the localized intensity of their histograms (via CLAHE) to improve contrast.

Ultimately, I learned how to move beyond theoretical computer vision snippets to architecting an end-to-end, CLI-driven application that solves a practical real-world problem.
