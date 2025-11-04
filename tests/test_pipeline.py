from __future__ import annotations

import zipfile
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import pytest
from PIL import Image

from narrative_architect.agents import (
    CreativeEnhancementAgent,
    ImageCaptioningAgent,
    NarrativeSynthesisAgent,
)
from narrative_architect.models import Project, ProjectStatus
from narrative_architect.services import FileIngestionService, NarrativePipeline, ProjectRepository
from narrative_architect.services.memory_service import NarrativeMemoryService


@pytest.fixture
def sample_bundle(tmp_path: Path) -> Path:
    assets_dir = tmp_path / "bundle"
    assets_dir.mkdir()

    image_path = assets_dir / "sunset.png"
    image = Image.new("RGB", (64, 64), color=(255, 128, 0))
    image.save(image_path)

    text_path = assets_dir / "notes.txt"
    text_path.write_text("The evening sky glowed with warm amber tones.", encoding="utf-8")

    bundle_path = tmp_path / "bundle.zip"
    with zipfile.ZipFile(bundle_path, "w") as archive:
        archive.write(image_path, arcname="sunset.png")
        archive.write(text_path, arcname="notes.txt")

    return bundle_path


def test_pipeline_generates_narrative(sample_bundle: Path) -> None:
    repository = ProjectRepository()
    ingestion = FileIngestionService()
    memory_service = NarrativeMemoryService()
    pipeline = NarrativePipeline(
        repository=repository,
        ingestion_service=ingestion,
        caption_agent=ImageCaptioningAgent(),
        narrative_agent=NarrativeSynthesisAgent(),
        enhancement_agent=CreativeEnhancementAgent(),
        memory_service=memory_service,
    )

    project_id = uuid4()
    now = datetime.utcnow()
    project = Project(
        id=project_id,
        status=ProjectStatus.queued,
        created_at=now,
        updated_at=now,
    )
    repository.create(project)

    pipeline.run(project_id, sample_bundle)

    stored = repository.get(project_id)
    assert stored is not None
    assert stored.status == ProjectStatus.completed
    assert stored.narrative is not None and len(stored.narrative.splitlines()) > 0

