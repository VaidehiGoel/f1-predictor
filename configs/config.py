from pathlib import Path

# Project root — resolved dynamically so this works on any machine
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data directories
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
CACHE_DIR = PROJECT_ROOT / "data" / "cache"
MODELS_DIR = PROJECT_ROOT / "models"

# FastF1 settings
SEASONS = [2022, 2023, 2024, 2025, 2026]