from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import UUID, uuid4

from fastapi import BackgroundTasks, Depends, FastAPI, File, Form, HTTPException, UploadFile

from narrative_architect import config
from narrative_architect.agents import (
    CreativeEnhancementAgent,
    ImageCaptioningAgent,
    NarrativeSynthesisAgent,
)
from narrative_architect.models import Project, ProjectCreateResponse, ProjectDetailResponse, ProjectStatus
from narrative_architect.services import FileIngestionService, NarrativePipeline, ProjectRepository
from narrative_architect.services.memory_service import NarrativeMemoryService


app = FastAPI(title="Multimodal Narrative Architect", version="0.1.0")


repository = ProjectRepository()
ingestion_service = FileIngestionService()
memory_service = NarrativeMemoryService()
pipeline = NarrativePipeline(
    repository=repository,
    ingestion_service=ingestion_service,
    caption_agent=ImageCaptioningAgent(),
    narrative_agent=NarrativeSynthesisAgent(),
    enhancement_agent=CreativeEnhancementAgent(),
    memory_service=memory_service,
)


def get_repository() -> ProjectRepository:
    return repository


def get_pipeline() -> NarrativePipeline:
    return pipeline


def get_memory_service() -> NarrativeMemoryService:
    return memory_service


@app.get("/healthz")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/projects", response_model=ProjectCreateResponse, status_code=202)
async def create_project(
    background_tasks: BackgroundTasks,
    bundle: UploadFile = File(...),
    user_id: Optional[str] = Form(None),
    project_repository: ProjectRepository = Depends(get_repository),
    narrative_pipeline: NarrativePipeline = Depends(get_pipeline),
) -> ProjectCreateResponse:
    """Create a new narrative project from a ZIP bundle of assets.

    Args:
        bundle: ZIP file containing images and text files
        user_id: Optional user identifier for memory persistence
        background_tasks: FastAPI background tasks
        project_repository: Project storage repository
        narrative_pipeline: Narrative generation pipeline

    Returns:
        Project creation response with project_id and status
    """
    allowed_content_types = {
        "application/zip",
        "application/x-zip-compressed",
        "application/octet-stream",
        "multipart/form-data",
    }
    if bundle.content_type not in allowed_content_types:
        raise HTTPException(status_code=400, detail="bundle must be a zip archive")

    project_id = uuid4()
    now = datetime.utcnow()
    project = Project(
        id=project_id,
        status=ProjectStatus.queued,
        created_at=now,
        updated_at=now,
        user_id=user_id,
    )
    project_repository.create(project)

    bundle_path = _persist_upload(bundle, project_id)

    background_tasks.add_task(narrative_pipeline.run, project_id, bundle_path)

    return ProjectCreateResponse(project_id=project_id, status=ProjectStatus.queued)


@app.get("/projects/{project_id}", response_model=ProjectDetailResponse)
def get_project(
    project_id: UUID,
    project_repository: ProjectRepository = Depends(get_repository),
) -> ProjectDetailResponse:
    project = project_repository.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_repository.to_response(project)


def _persist_upload(bundle: UploadFile, project_id: UUID) -> Path:
    destination = config.UPLOAD_ROOT / f"{project_id}.zip"
    if hasattr(bundle.file, "seek"):
        bundle.file.seek(0)
    with destination.open("wb") as target:
        shutil.copyfileobj(bundle.file, target)
    if hasattr(bundle.file, "close"):
        bundle.file.close()
    return destination

