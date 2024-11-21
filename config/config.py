"""Application configuration settings."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict


@dataclass
class Config:
    """Application configuration."""

    # Paths
    ROOT_DIR: Path = Path(__file__).parent.parent
    LOGS_DIR: Path = ROOT_DIR / "logs"
    ASSETS_DIR: Path = ROOT_DIR / "assets"
    DATA_DIR: Path = ROOT_DIR / "data"
    JIRA_DATA_PATH: str = os.getenv(
        "JIRA_DATA_PATH", str(DATA_DIR / "EFDDH-Jira-Data-All.csv")
    )

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Cache settings
    CACHE_TTL: int = 3600  # 1 hour
    CACHE_DIR: Path = ROOT_DIR / ".cache"

    # Chart defaults
    CHART_DEFAULTS: Dict[str, Any] = field(
        default_factory=lambda: {
            "height": 400,
            "margin": {"t": 50, "l": 25, "r": 25, "b": 25},
            "template": "plotly_white",
        }
    )

    # Data processing
    MAX_ROWS_PER_PAGE: int = 1000
    SAMPLE_SIZE: int = 10000

    # API settings
    API_TIMEOUT: int = 30
    API_RETRIES: int = 3

    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure required directories exist."""
        cls.LOGS_DIR.mkdir(exist_ok=True)
        cls.CACHE_DIR.mkdir(exist_ok=True)
