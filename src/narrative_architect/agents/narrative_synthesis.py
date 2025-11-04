from __future__ import annotations

from typing import Dict, Iterable, List, Sequence, Tuple

from narrative_architect.agents.base import BaseAgent
from narrative_architect.models import (
    AssetType,
    CaptionArtifact,
    IngestedAsset,
    NarrativeDraft,
    NarrativeSegment,
)


class NarrativeSynthesisAgent(
    BaseAgent[Tuple[Sequence[IngestedAsset], Iterable[CaptionArtifact]], NarrativeDraft]
):
    """Compose a structured narrative drafts from captions and texts."""

    def __init__(self) -> None:
        super().__init__(name="narrative_synthesis")

    def run(
        self,
        payload: Tuple[Sequence[IngestedAsset], Iterable[CaptionArtifact]],
    ) -> NarrativeDraft:
        assets, captions = payload
        asset_lookup: Dict[str, IngestedAsset] = {asset.asset_id: asset for asset in assets}

        segments: List[NarrativeSegment] = []
        used_assets = set()

        for caption in captions:
            ingested = asset_lookup.get(caption.asset_id)
            if not ingested:
                continue

            supporting_lines: List[str] = [caption.caption]

            context_note = ingested.metadata.get("context")
            if context_note:
                supporting_lines.append(f"Context clue: {context_note}.")

            segments.append(
                NarrativeSegment(
                    heading=ingested.title,
                    body=" ".join(supporting_lines),
                    source_assets=[ingested.asset_id],
                )
            )
            used_assets.add(ingested.asset_id)

        for asset in assets:
            if asset.type != AssetType.text:
                continue
            if not asset.content:
                continue

            segments.append(
                NarrativeSegment(
                    heading=asset.title,
                    body=asset.content.strip(),
                    source_assets=[asset.asset_id],
                )
            )
            used_assets.add(asset.asset_id)

        synopsis = self._build_synopsis(segments, used_assets, len(assets))

        return NarrativeDraft(synopsis=synopsis, segments=segments)

    def _build_synopsis(
        self, segments: Sequence[NarrativeSegment], referenced_assets: Iterable[str], total_assets: int
    ) -> str:
        if not segments:
            return "No narrative content could be synthesized from the uploaded bundle."

        referenced_count = len(set(referenced_assets))
        theme = segments[0].heading if segments else "the collection"
        return (
            f"A cohesive storyline emerges around {theme}, drawing from {referenced_count} of the "
            f"{total_assets} supplied assets."
        )

