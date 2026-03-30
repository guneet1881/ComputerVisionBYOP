import numpy as np
import cv2

def reorder_corners(corner_points):
    """
    Given a list of four points, this function orders them conceptually as:
    [top-left, top-right, bottom-right, bottom-left].
    This ordered orientation is necessary to perform a consistent 
    top-down perspective projection layout.
    """
    sorted_corners = np.zeros((4, 2), dtype="float32")

    # To find the top-left and bottom-right points, we can compute the sum 
    # of the (x, y) coordinates. The point with the smallest sum will be 
    # our top-left corner, and the largest sum will be our bottom-right.
    coordinate_sum = corner_points.sum(axis=1)
    sorted_corners[0] = corner_points[np.argmin(coordinate_sum)]
    sorted_corners[2] = corner_points[np.argmax(coordinate_sum)]

    # Now we differentiate between the remaining points by taking the difference
    # between the y and x values. The smallest difference is our top-right corner, 
    # and the largest difference will be our bottom-left.
    coordinate_diff = np.diff(corner_points, axis=1)
    sorted_corners[1] = corner_points[np.argmin(coordinate_diff)]
    sorted_corners[3] = corner_points[np.argmax(coordinate_diff)]

    return sorted_corners

def extract_birdseye_view(original_image, focus_points):
    """
    Generates a calculated perspective matrix and warps an angled document 
    into a flat, top-down projection representation.
    """
    ordered_corners = reorder_corners(focus_points)
    (top_left, top_right, bottom_right, bottom_left) = ordered_corners

    # Distance computation to determine the exact pixel width of our new 
    # flattened canvas. We use the Pythogorean theorem on the coordinates.
    bottom_width_span = np.sqrt(((bottom_right[0] - bottom_left[0]) ** 2) + ((bottom_right[1] - bottom_left[1]) ** 2))
    top_width_span = np.sqrt(((top_right[0] - top_left[0]) ** 2) + ((top_right[1] - top_left[1]) ** 2))
    target_width = max(int(bottom_width_span), int(top_width_span))

    # Similar calculation to deduce the height of the new canvas, comparing 
    # the distances between the left and right structural sides.
    right_height_span = np.sqrt(((top_right[0] - bottom_right[0]) ** 2) + ((top_right[1] - bottom_right[1]) ** 2))
    left_height_span = np.sqrt(((top_left[0] - bottom_left[0]) ** 2) + ((top_left[1] - bottom_left[1]) ** 2))
    target_height = max(int(right_height_span), int(left_height_span))

    # We map the four corners of the isolated document to standard orthogonal
    # vertices [0, 0] → [target_width, 0], etc. This achieves mapping an angled object
    # directly onto a 2D straight plane viewing.
    flat_mapping = np.array([
        [0, 0],
        [target_width - 1, 0],
        [target_width - 1, target_height - 1],
        [0, target_height - 1]], dtype="float32")

    # Generate the actual mathematical transform formula using OpenCV, then 
    # execute applying it via warping.
    transform_matrix = cv2.getPerspectiveTransform(ordered_corners, flat_mapping)
    flattened_view_image = cv2.warpPerspective(original_image, transform_matrix, (target_width, target_height))

    return flattened_view_image
