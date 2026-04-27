"""FastAPI wrapper around the pipeline.

Endpoints:
- POST /ask  body: {"concept": "..."}  -> {"mp4": "/videos/...", "session": "...", "attempts": N}
- GET  /health -> {"status": "ok"}
- GET  /videos/...      static files served from videos/sessions/

Run:
    uvicorn src.api:app --reload --port 8000

CLI test:
    curl -X POST http://localhost:8000/ask \\
         -H 'content-type: application/json' \\
         -d '{"concept": "Draw a unit circle."}'
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.pipeline import SESSIONS_DIR, ask

app = FastAPI(title="MathMentor pipeline API")

VIDEOS_ROOT = Path("videos")
VIDEOS_ROOT.mkdir(exist_ok=True)
app.mount("/videos", StaticFiles(directory=VIDEOS_ROOT), name="videos")


class AskRequest(BaseModel):
    concept: str
    model: str | None = None


class AskResponse(BaseModel):
    mp4: str
    session: str
    attempts: int


def _count_attempts(session_dir: Path) -> int:
    return len(list(session_dir.glob("attempt_*_scene.py")))


def _latest_session() -> Path:
    return max(SESSIONS_DIR.iterdir(), key=lambda p: p.stat().st_mtime)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask_endpoint(req: AskRequest) -> AskResponse:
    try:
        mp4_path = ask(req.concept, model=req.model) if req.model else ask(req.concept)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)[:500]) from exc

    session = _latest_session()
    return AskResponse(
        mp4=f"/{mp4_path.as_posix()}",
        session=session.name,
        attempts=_count_attempts(session),
    )
