from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
TABLES = ROOT / "reports" / "tables"
FIGURES = ROOT / "assets" / "figures"

for folder in (PROCESSED, TABLES, FIGURES):
    folder.mkdir(parents=True, exist_ok=True)
