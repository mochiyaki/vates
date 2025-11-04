from __future__ import annotations

import zipfile
from pathlib import Path
from typing import BinaryIO, List
from uuid import UUID, uuid5

from narrative_architect import config
from narrative_architect.models import AssetType, IngestedAsset

NAMESPACE_ASSET = UUID("6d0fe502-0857-4694-9bc4-67edc8b29752")


class FileIngestionService:
    """Handle unpacking uploaded bundles and turning them into asset records."""

    def unpack_bundle(self, bundle_bytes: BinaryIO, project_id: UUID) -> Path:
        target_dir = config.UPLOAD_ROOT / str(project_id)
        target_dir.mkdir(parents=True, exist_ok=True)

        if hasattr(bundle_bytes, "seek"):
            bundle_bytes.seek(0)

        with zipfile.ZipFile(bundle_bytes) as archive:
            for member in archive.infolist():
                self._guard_zip_member(member)
                archive.extract(member, path=target_dir)

        return target_dir

    def collect_assets(self, root: Path) -> List[IngestedAsset]:
        assets: List[IngestedAsset] = []
        for path in root.rglob("*"):
            if path.is_dir():
                continue

            suffix = path.suffix.lower()
            if suffix in config.settings.ingestion_supported_images:
                assets.append(self._build_image_asset(path))
            elif suffix in config.settings.ingestion_supported_text:
                assets.append(self._build_text_asset(path))

        return assets

    def _build_image_asset(self, path: Path) -> IngestedAsset:
        asset_id = self._derive_asset_id(path)
        return IngestedAsset(
            asset_id=str(asset_id),
            type=AssetType.image,
            title=path.stem.replace("_", " ").title(),
            metadata={
                "path": str(path),
                "filename": path.name,
            },
        )

    def _build_text_asset(self, path: Path) -> IngestedAsset:
        asset_id = self._derive_asset_id(path)
        content = path.read_text(encoding="utf-8", errors="ignore")
        return IngestedAsset(
            asset_id=str(asset_id),
            type=AssetType.text,
            title=path.stem.replace("_", " ").title(),
            content=content,
            metadata={
                "path": str(path),
                "filename": path.name,
            },
        )

    def _derive_asset_id(self, path: Path) -> UUID:
        return uuid5(NAMESPACE_ASSET, str(path))

    def _guard_zip_member(self, member: zipfile.ZipInfo) -> None:
        if member.is_dir():
            return
        extracted_path = Path(member.filename)
        if extracted_path.is_absolute() or ".." in extracted_path.parts:
            raise ValueError("Archive contains unsupported path traversal entries")

