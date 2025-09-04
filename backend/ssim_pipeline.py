import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim


def preprocess(bgr: np.ndarray, target_wh: tuple[int, int] = (250, 160)) -> np.ndarray:
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    g = cv2.resize(g, target_wh, interpolation=cv2.INTER_AREA)
    return g


def compute_ssim_map(ref_bgr: np.ndarray, sus_bgr: np.ndarray) -> tuple[float, np.ndarray]:
    ref = preprocess(ref_bgr)
    sus = preprocess(sus_bgr)
    score, ssim_map = ssim(ref, sus, full=True)
    # scale SSIM map to 0..255 (uint8). Following the reference approach (no inversion)
    diff = (ssim_map * 255.0).astype(np.uint8)
    return score, diff


def localize(diff: np.ndarray, min_area: int = 0) -> tuple[np.ndarray, list[tuple[int, int, int, int]]]:
    # Smooth to reduce salt-and-pepper artifacts then threshold
    blurred = cv2.GaussianBlur(diff, (5, 5), 0)
    _, thr = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Morphology to merge nearby fragments
    kernel = np.ones((3, 3), np.uint8)
    thr = cv2.morphologyEx(thr, cv2.MORPH_CLOSE, kernel, iterations=1)
    thr = cv2.dilate(thr, kernel, iterations=1)

    h, w = thr.shape[:2]
    area_thresh = max(min_area, int(0.0005 * w * h))  # relative area filter

    cnts, _ = cv2.findContours(thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes: list[tuple[int, int, int, int]] = []
    for c in cnts:
        if cv2.contourArea(c) < area_thresh:
            continue
        x, y, bw, bh = cv2.boundingRect(c)
        pad = 2
        x = max(0, x - pad)
        y = max(0, y - pad)
        bw = min(w - x, bw + 2 * pad)
        bh = min(h - y, bh + 2 * pad)
        boxes.append((x, y, bw, bh))

    return thr, boxes


def draw_boxes(bgr: np.ndarray, boxes: list[tuple[int, int, int, int]]) -> np.ndarray:
    out = bgr.copy()
    for (x, y, w, h) in boxes:
        cv2.rectangle(out, (x, y), (x + w, y + h), (0, 0, 255), 2)
    return out


