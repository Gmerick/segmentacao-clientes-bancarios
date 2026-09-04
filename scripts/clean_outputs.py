from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "data" / "raw" / "customers.csv",
    ROOT / "data" / "raw" / "monthly_activity.csv",
    ROOT / "data" / "processed" / "customer_segments.csv",
    ROOT / "data" / "processed" / "segment_profiles.csv",
    ROOT / "data" / "processed" / "monthly_segment_activity.csv",
    ROOT / "data" / "processed" / "model_selection.csv",
    ROOT / "reports" / "dashboard_preview.png",
    ROOT / "reports" / "metrics.json",
]

for target in TARGETS:
    if target.exists():
        target.unlink()
        print(f"Removido: {target.relative_to(ROOT)}")
