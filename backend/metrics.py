import numpy as np


def iou(pred_mask: np.ndarray, gt_mask: np.ndarray) -> float:
    pred = (pred_mask > 0).astype(np.uint8)
    gt = (gt_mask > 0).astype(np.uint8)
    inter = np.logical_and(pred, gt).sum()
    union = np.logical_or(pred, gt).sum()
    return float(inter) / float(union + 1e-9)


