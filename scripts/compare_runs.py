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

    dist_threshold = 0.1

    n = min(len(first_run), len(second_run))

    first_divergence = {}
    max_dist = 0
    max = {}

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
                "Index": {row},
                "t_s": {time},
                "dist_m": {dist},
                "Distance threshold": {dist_threshold}
            }
            print(first_divergence)
        
        if dist >= max_dist:
            max_dist = dist
            max = {
                "Type": "Max Distance",
                "Index": {row},
                "t_s": {time},
                "dist_m": {dist}
            }

        if dist > dist_threshold and row == (n - 1):
            final = {
                "Type": "Final Distance",
                "t_s": {time},
                "dist_m": {dist}
            }
            print(max)
            print(final)
            break
    else:
        print("No divergence")

if __name__ == "__main__":
    main()