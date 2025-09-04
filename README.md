# SSIM Content Tampering Prototype

Minimal web app to detect and localize potential content tampering using SSIM.

## Stack
- Backend: FastAPI, Uvicorn, OpenCV, scikit-image, NumPy
- Frontend: React + Vite + TypeScript
- Build: Docker, docker-compose
- Tests: Pytest (backend), Vitest (frontend)
- Lint/Format: Ruff (py TODO), ESLint + Prettier (ts)

## Run locally (Docker)
1. Ensure Docker is installed
2. Copy environment example and adjust if needed:
   ```bash
   cp .env.example .env
   ```
3. Build and start:
   ```bash
   docker-compose up --build
   ```
4. Open web UI at `http://localhost:5173` and API docs at `http://localhost:8000/docs`.

## API
POST `/analyze` multipart/form-data
- `reference`: image/png or image/jpeg
- `suspect`: image/png or image/jpeg

Response
```json
{
  "ssim_score": 0.95,
  "boxes": [{"x":10,"y":20,"w":100,"h":80}],
  "overlay_b64": "...",
  "heatmap_b64": "...",
  "message": "ok"
}
```

## Notes & Limitations
- Images only in this MVP. PDFs are not accepted; to sanitize PDFs, rasterize to image (first page) before upload.
- Uploads are processed in memory and not persisted.
- Payload limit ~12MB; adjust in `app.py` if needed.
- For production, restrict CORS to your domain and add rate limiting at proxy.

## Development
Backend
```bash
cd backend
python -m pytest -q
uvicorn app:app --reload
```

Frontend
```bash
cd frontend
npm ci
npm run dev
```

## Future Enhancements
- Alignment via ORB + RANSAC homography
- PDF rasterization & multi-page selection
- Downloadable report (images + metrics)
- Simple auth if exposed externally


