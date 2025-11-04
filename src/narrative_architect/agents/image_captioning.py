from __future__ import annotations

from typing import Iterable, List

from PIL import Image

from narrative_architect.agents.base import BaseAgent
from narrative_architect.models import CaptionArtifact, IngestedAsset


class ImageCaptioningAgent(BaseAgent[Iterable[IngestedAsset], List[CaptionArtifact]]):
    """Generate lightweight captions for ingested images."""

    def __init__(self) -> None:
        super().__init__(name="image_captioning")

    def run(self, payload: Iterable[IngestedAsset]) -> List[CaptionArtifact]:
        captions: List[CaptionArtifact] = []
        for asset in payload:
            if asset.type != asset.type.image:
                continue

            path = asset.metadata.get("path")
            if not path:
                continue

            width = height = None
            try:
                with Image.open(path) as image:
                    width, height = image.size
            except Exception:
                pass

            resolution_text = (
                f" The frame measures approximately {width}x{height} pixels."
                if width and height
                else ""
            )

            caption = (
                f"{asset.title} features visible elements that connect to the surrounding "
                f"story context.{resolution_text}"
            )

            captions.append(
                CaptionArtifact(
                    asset_id=asset.asset_id,
                    caption=caption,
                    details={
                        "width": width,
                        "height": height,
                        "source_path": path,
                    },
                )
            )

        return captions

