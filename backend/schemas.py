from pydantic import BaseModel
from typing import List, Optional


class Box(BaseModel):
    x: int
    y: int
    w: int
    h: int


class AnalyzeResponse(BaseModel):
    ssim_score: float
    boxes: List[Box]
    overlay_b64: str  # PNG base64 (suspect with red boxes)
    heatmap_b64: str  # SSIM map visualization (jet)
    iou: Optional[float] = None
    message: str = "ok"


