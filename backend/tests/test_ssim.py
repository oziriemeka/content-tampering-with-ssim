import cv2
import numpy as np

from ssim_pipeline import compute_ssim_map, localize


def test_ssim_map_runs():
    ref = np.zeros((200, 300, 3), dtype=np.uint8)
    sus = ref.copy()
    cv2.rectangle(sus, (50, 50), (120, 120), (255, 255, 255), -1)
    score, diff = compute_ssim_map(ref, sus)
    assert 0 <= score <= 1
    thr, boxes = localize(diff, min_area=50)
    assert len(boxes) >= 1


