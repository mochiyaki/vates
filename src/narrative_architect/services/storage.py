from __future__ import annotations

import threading
from datetime import datetime
from typing import Dict, Optional
from uuid import UUID

from narrative_architect.models import Project, ProjectDetailResponse, ProjectStatus


class ProjectRepository:
    """Thread-safe in-memory repository for project state."""

    def __init__(self) -> None:
        self._projects: Dict[UUID, Project] = {}
        self._lock = threading.Lock()

    def create(self, project: Project) -> Project:
        with self._lock:
            self._projects[project.id] = project
        return project

    def get(self, project_id: UUID) -> Optional[Project]:
        with self._lock:
            return self._projects.get(project_id)

    def update_status(
        self,
        project_id: UUID,
        *,
        status: ProjectStatus,
        narrative: Optional[str] = None,
        draft=None,
        enrichments=None,
        error_message: Optional[str] = None,
    ) -> Optional[Project]:
        with self._lock:
            project = self._projects.get(project_id)
            if not project:
                return None

            project.status = status
            project.updated_at = datetime.utcnow()
            if narrative is not None:
                project.narrative = narrative
            if draft is not None:
                project.draft = draft
            if enrichments is not None:
                project.enrichments = list(enrichments)
            if error_message is not None:
                project.error_message = error_message
            self._projects[project_id] = project
            return project

    def to_response(self, project: Project) -> ProjectDetailResponse:
        return ProjectDetailResponse(**project.model_dump())

