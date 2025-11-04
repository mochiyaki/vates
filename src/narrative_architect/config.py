from __future__ import annotations

import os
from pathlib import Path
from typing import Final

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

APP_NAME: Final[str] = "multimodal-narrative-architect"
BASE_DIR: Final[Path] = Path(os.environ.get("NARRATIVE_ARCHITECT_BASE", "/home/yab/Vates"))
UPLOAD_ROOT: Final[Path] = BASE_DIR / "var" / "uploads"
UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)


class Settings:
    """Application settings container.

    This lightweight settings object keeps the service configurable while
    avoiding external dependencies beyond the standard library.
    """

    ingestion_supported_images = {".png", ".jpg", ".jpeg"}
    ingestion_supported_text = {".txt", ".md"}


settings = Settings()

