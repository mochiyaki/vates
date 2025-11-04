from __future__ import annotations

import logging
from pathlib import Path
from typing import List
from uuid import UUID

from narrative_architect.agents import (
    CreativeEnhancementAgent,
    ImageCaptioningAgent,
    NarrativeSynthesisAgent,
)
from narrative_architect.models import EnrichmentArtifact, IngestedAsset, NarrativeDraft, ProjectStatus
from narrative_architect.services.file_ingestion import FileIngestionService
from narrative_architect.services.memory_service import NarrativeMemoryService
from narrative_architect.services.storage import ProjectRepository


logger = logging.getLogger(__name__)


class NarrativePipeline:
    """Coordinate the end-to-end agent pipeline."""

    def __init__(
        self,
        repository: ProjectRepository,
        ingestion_service: FileIngestionService,
        caption_agent: ImageCaptioningAgent,
        narrative_agent: NarrativeSynthesisAgent,
        enhancement_agent: CreativeEnhancementAgent,
        memory_service: NarrativeMemoryService,
    ) -> None:
        self.repository = repository
        self.ingestion_service = ingestion_service
        self.caption_agent = caption_agent
        self.narrative_agent = narrative_agent
        self.enhancement_agent = enhancement_agent
        self.memory_service = memory_service

    def run(self, project_id: UUID, bundle_path: Path) -> None:
        logger.info("Starting pipeline for project %s", project_id)
        self.repository.update_status(project_id, status=ProjectStatus.processing)

        try:
            # Get project to check for user_id
            project = self.repository.get(project_id)
            user_id = project.user_id if project else None

            # Retrieve user context from memory if available
            user_context = None
            if user_id and self.memory_service.is_available():
                user_context = self.memory_service.get_user_context(
                    user_id, query="What are this user's narrative preferences and past projects?"
                )
                if user_context:
                    logger.info("Retrieved user context for user %s", user_id)

            with bundle_path.open("rb") as fh:
                extracted_dir = self.ingestion_service.unpack_bundle(fh, project_id)

            assets = self.ingestion_service.collect_assets(extracted_dir)
            if not assets:
                raise ValueError("No supported assets found in uploaded bundle")

            captions = self.caption_agent.run(assets)
            draft = self.narrative_agent.run((assets, captions))
            enrichments = self.enhancement_agent.run((draft, assets))
            narrative = self._compose_final_narrative(draft, enrichments)

            # Extract themes for memory storage
            themes = self._extract_themes(draft)

            self.repository.update_status(
                project_id,
                status=ProjectStatus.completed,
                narrative=narrative,
                draft=draft,
                enrichments=enrichments,
            )

            # Store project completion in memory
            if user_id and self.memory_service.is_available():
                self.memory_service.store_project_completion(
                    project_id=project_id,
                    user_id=user_id,
                    narrative=narrative,
                    assets_used=[asset.asset_id for asset in assets],
                    themes=themes,
                )

            logger.info("Completed pipeline for project %s", project_id)
        except Exception as exc:  # pragma: no cover - defensive catch-all
            logger.exception("Pipeline failed for project %s", project_id)
            self.repository.update_status(
                project_id,
                status=ProjectStatus.failed,
                error_message=str(exc),
            )

    def _compose_final_narrative(
        self, draft: NarrativeDraft, enrichments: List[EnrichmentArtifact]
    ) -> str:
        lines: List[str] = [draft.synopsis, ""]
        for segment in draft.segments:
            lines.append(segment.heading)
            lines.append("-" * len(segment.heading))
            lines.append(segment.body)
            lines.append("")

        if enrichments:
            lines.append("Creative Enhancements")
            lines.append("----------------------")
            for artifact in enrichments:
                lines.append(f"{artifact.label}:")
                lines.append(artifact.content)
                lines.append("")

        return "\n".join(lines).strip()

    def _extract_themes(self, draft: NarrativeDraft) -> List[str]:
        """Extract themes from the narrative draft for memory storage.

        Args:
            draft: The narrative draft

        Returns:
            List of themes extracted from segment headings
        """
        themes = [segment.heading for segment in draft.segments if segment.heading]
        return themes[:5]  # Limit to first 5 themes

