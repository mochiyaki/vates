from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ProjectStatus(str, Enum):
    queued = "queued"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class AssetType(str, Enum):
    image = "image"
    text = "text"


class IngestedAsset(BaseModel):
    asset_id: str
    type: AssetType
    title: str
    content: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CaptionArtifact(BaseModel):
    asset_id: str
    caption: str
    details: Dict[str, Any] = Field(default_factory=dict)


class NarrativeSegment(BaseModel):
    heading: str
    body: str
    source_assets: List[str] = Field(default_factory=list)


class NarrativeDraft(BaseModel):
    synopsis: str
    segments: List[NarrativeSegment]


class EnrichmentArtifact(BaseModel):
    label: str
    content: str
    sources: List[str] = Field(default_factory=list)


class Project(BaseModel):
    id: UUID
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime
    user_id: Optional[str] = None
    narrative: Optional[str] = None
    draft: Optional[NarrativeDraft] = None
    enrichments: List[EnrichmentArtifact] = Field(default_factory=list)
    error_message: Optional[str] = None


class ProjectCreateResponse(BaseModel):
    project_id: UUID
    status: ProjectStatus


class ProjectDetailResponse(BaseModel):
    id: UUID
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime
    user_id: Optional[str] = None
    narrative: Optional[str] = None
    draft: Optional[NarrativeDraft] = None
    enrichments: List[EnrichmentArtifact] = Field(default_factory=list)
    error_message: Optional[str] = None

