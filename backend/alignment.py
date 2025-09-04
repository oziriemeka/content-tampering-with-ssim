import numpy as np


def center_crop_to_match(a: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Naive size match by center-cropping to the smallest common dimensions.
    TODO: Optional enhancement: ORB keypoints + findHomography + warpPerspective for robust alignment
    """
    h = min(a.shape[0], b.shape[0])
    w = min(a.shape[1], b.shape[1])
    return a[:h, :w], b[:h, :w]


