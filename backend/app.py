import base64
from typing import Optional

import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from schemas import AnalyzeResponse, Box
from ssim_pipeline import compute_ssim_map, localize, draw_boxes
from metrics import iou as iou_fn


MAX_UPLOAD_MB = 12
ALLOWED_MIME_TYPES = {
    "image/png",
    "image/jpeg",
    # PDFs are intentionally rejected in this MVP to avoid heavy deps.
}


app = FastAPI(title="SSIM Forgery Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def read_image(file: UploadFile) -> np.ndarray:
    data = file.file.read()
    arr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(status_code=400, detail="Unsupported image or decode error")
    return img


def to_b64_png(bgr: np.ndarray) -> str:
    ok, buf = cv2.imencode(".png", bgr)
    return base64.b64encode(buf.tobytes()).decode("utf-8") if ok else ""


def _scale_boxes(
    boxes_xywh: list[tuple[int, int, int, int]], from_hw: tuple[int, int], to_hw: tuple[int, int]
) -> list[tuple[int, int, int, int]]:
    from_h, from_w = from_hw
    to_h, to_w = to_hw
    sx = to_w / max(1, from_w)
    sy = to_h / max(1, from_h)
    scaled: list[tuple[int, int, int, int]] = []
    for x, y, w, h in boxes_xywh:
        scaled.append((int(round(x * sx)), int(round(y * sy)), int(round(w * sx)), int(round(h * sy))))
    return scaled


def _validate_uploads(request: Request, files: list[Optional[UploadFile]]):
    content_length = request.headers.get("content-length")
    if content_length is not None:
        try:
            if int(content_length) > MAX_UPLOAD_MB * 1024 * 1024:
                raise HTTPException(status_code=413, detail="Payload too large")
        except ValueError:
            pass
    for f in files:
        if f is None:
            continue
        if f.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(status_code=415, detail=f"Unsupported media type: {f.content_type}")


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    request: Request,
    reference: UploadFile = File(...),
    suspect: UploadFile = File(...),
    gt_mask: Optional[UploadFile] = File(None),
):
    _validate_uploads(request, [reference, suspect])

    ref = read_image(reference)
    sus = read_image(suspect)

    score, diff = compute_ssim_map(ref, sus)
    thr, boxes_xywh = localize(diff, min_area=0)

    diff_h, diff_w = diff.shape[:2]
    sus_h, sus_w = sus.shape[:2]
    boxes_scaled = _scale_boxes(boxes_xywh, (diff_h, diff_w), (sus_h, sus_w))
    boxes = [Box(x=int(x), y=int(y), w=int(w), h=int(h)) for (x, y, w, h) in boxes_scaled]

    overlay = draw_boxes(sus, boxes_scaled)
    heatmap_small = cv2.applyColorMap(diff, cv2.COLORMAP_JET)
    heatmap = cv2.resize(heatmap_small, (sus_w, sus_h), interpolation=cv2.INTER_NEAREST)

    # Optional IoU if ground truth mask is provided
    iou_val = None
    if gt_mask is not None:
        if gt_mask.content_type not in {"image/png", "image/jpeg"}:
            raise HTTPException(status_code=415, detail="gt_mask must be an image (png or jpeg)")
        gt = read_image(gt_mask)
        gt = cv2.cvtColor(gt, cv2.COLOR_BGR2GRAY)
        # Resize predicted threshold (diff space) to suspect size, then threshold to binary
        thr_resized = cv2.resize(thr, (sus_w, sus_h), interpolation=cv2.INTER_NEAREST)
        _, thr_bin = cv2.threshold(thr_resized, 0, 255, cv2.THRESH_BINARY)
        _, gt_bin = cv2.threshold(gt, 0, 255, cv2.THRESH_BINARY)
        iou_val = float((np.logical_and(thr_bin > 0, gt_bin > 0)).sum()) / float((np.logical_or(thr_bin > 0, gt_bin > 0)).sum() + 1e-9)

    return AnalyzeResponse(
        ssim_score=float(score),
        boxes=boxes,
        overlay_b64=to_b64_png(overlay),
        heatmap_b64=to_b64_png(heatmap),
        iou=iou_val,
        message="ok",
    )


