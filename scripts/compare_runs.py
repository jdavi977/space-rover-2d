import json
import sys
from pathlib import Path

import math
import pandas as pd

def main():
    if len(sys.argv) < 3:
        print("Usage: uv run scripts/compare_runs.py runs/milestones/<run_id1> runs/milestones/<run_id2>")
        raise SystemExit(1)
    
    first_dir = Path(sys.argv[1])
    first_run = pd.read_parquet(first_dir / "telemetry.parquet")

    second_dir = Path(sys.argv[2])
    second_run = pd.read_parquet(second_dir / "telemetry.parquet")

    first_dir_name = str(first_dir).split("/")[2]
    second_dir_name = str(second_dir).split("/")[2]

    run_dir = Path("runs") / "comparisons" / f"{first_dir_name}__{second_dir_name}"
    run_dir.mkdir(parents=True, exist_ok=True)

    dist_threshold = 0.1

    n = min(len(first_run), len(second_run))

    first_divergence = {}
    max_dist = 0
    final_dist = 0
    max = {}
    final = {}

    for row in range(n):
        time = first_run["t_s"].iloc[row]

        xA = first_run["x_m"].to_numpy()
        xB = second_run["x_m"].to_numpy()

        yA = first_run["y_m"].to_numpy()
        yB = second_run["y_m"].to_numpy()

        dist = math.sqrt((xA[row] - xB[row])**2 + (yA[row] - yB[row])**2)

        if dist > dist_threshold and not first_divergence:
            first_divergence = {
                "Type": "First Divergence",
                "Index": row,
                "t_s": time,
                "dist_m": dist
            }
            print(f"Distance threshold {dist_threshold}")
            print(first_divergence)
        
        if dist >= max_dist:
            max_dist = dist
            max = {
                "Type": "Max Distance",
                "Index": row,
                "t_s": time,
                "dist_m": dist
            }

        if dist > dist_threshold and row == (n - 1):
            final_dist = dist
            final = {
                "Type": "Final Distance",
                "t_s": time,
                "dist_m": dist
            }
            print(max)
            print(final)
            break
    else:
        print("No divergence")

    comparison_meta = {
        "run_id": f"{first_dir_name}__{second_dir_name}",
        "dist_threshold": dist_threshold,
        "first_divergence": {},
        "max_distance": max,
        "final_distance": final,
    }

    if first_divergence:
        comparison_meta["first_divergence"] = first_divergence
        
    (run_dir / "comparison.json").write_text(json.dumps(comparison_meta, indent=2))


if __name__ == "__main__":
    main()