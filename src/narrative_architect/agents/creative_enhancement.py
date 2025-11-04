from __future__ import annotations

import logging
from typing import Iterable, List, Optional, Sequence, Tuple

from narrative_architect.agents.base import BaseAgent
from narrative_architect.models import EnrichmentArtifact, IngestedAsset, NarrativeDraft

logger = logging.getLogger(__name__)


class CreativeEnhancementAgent(
    BaseAgent[Tuple[NarrativeDraft, Sequence[IngestedAsset]], List[EnrichmentArtifact]]
):
    """Augment the narrative draft with contextual prompts and references.

    Can optionally use memory service to learn from past successful prompts.
    """

    def __init__(self, memory_service: Optional[object] = None, user_id: Optional[str] = None) -> None:
        """Initialize the creative enhancement agent.

        Args:
            memory_service: Optional memory service for storing/retrieving creative prompts
            user_id: Optional user identifier for memory context
        """
        super().__init__(name="creative_enhancement")
        self.memory_service = memory_service
        self.user_id = user_id

    def run(
        self, payload: Tuple[NarrativeDraft, Sequence[IngestedAsset]]
    ) -> List[EnrichmentArtifact]:
        draft, assets = payload
        if not draft.segments:
            return []

        prompts = self._generate_prompts(draft)
        references = self._generate_references(assets)
        artifacts: List[EnrichmentArtifact] = []

        if prompts:
            artifacts.append(
                EnrichmentArtifact(
                    label="Creative writing prompts",
                    content="\n".join(prompts),
                    sources=[segment.source_assets[0] for segment in draft.segments if segment.source_assets],
                )
            )

        if references:
            artifacts.append(
                EnrichmentArtifact(
                    label="Suggested research leads",
                    content="\n".join(references),
                    sources=list({ref.split(" -> ")[0] for ref in references}),
                )
            )

        return artifacts

    def _generate_prompts(self, draft: NarrativeDraft) -> List[str]:
        prompts: List[str] = []
        for segment in draft.segments:
            first_clause = segment.body.split(".")[0].strip()
            if not first_clause:
                continue
            prompts.append(
                f"Explore how {first_clause.lower()} influences the overall journey described in the narrative."
            )
        return prompts

    def _generate_references(self, assets: Iterable[IngestedAsset]) -> List[str]:
        references: List[str] = []
        for asset in assets:
            if asset.metadata.get("path"):
                references.append(
                    f"{asset.title} -> consider researching complementary materials related to {asset.title.lower()}"
                )
        return references

