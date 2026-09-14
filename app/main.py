"""FastAPI entrypoint for ProofPilot."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from .agent import run_with_strands
from .workflow import build_artifact


APP_DIR = Path(__file__).parent
app = FastAPI(title="ProofPilot", version="0.1.0")


class Intake(BaseModel):
    brief: str = Field(min_length=10, max_length=12000)
    project_context: str = Field(default="", max_length=12000)
    mode: Literal["demo", "aws"] = "demo"


@app.get("/")
def home() -> FileResponse:
    return FileResponse(APP_DIR / "static" / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "proofpilot"}


@app.post("/api/analyze")
def analyze(intake: Intake) -> dict:
    if intake.mode == "demo":
        return {
            "mode": "demo",
            "notice": "Local deterministic demo: no LLM or AWS service was invoked.",
            "artifact": build_artifact(intake.brief, intake.project_context),
        }
    try:
        return {
            "mode": "aws",
            "notice": "Strands Agent invocation requested using the configured AWS environment.",
            "agent_response": run_with_strands(intake.brief, intake.project_context),
        }
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"AWS/Strands run unavailable: {exc}") from exc
