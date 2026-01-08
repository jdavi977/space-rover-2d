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

    for row in range(n):
        time = first_run["t_s"].iloc[row]

        xA = first_run["x_m"].to_numpy()
        xB = second_run["x_m"].to_numpy()

        yA = first_run["y_m"].to_numpy()
        yB = second_run["y_m"].to_numpy()

        dist = math.sqrt((xA[row] - xB[row])**2 + (yA[row] - yB[row])**2)

        if dist > dist_threshold:
            print(f"Index: {row}")
            print(f"Time: {time}")
            print(f"Distance: {dist}")
            print(f"Distance threshold: {dist_threshold}")
            break
    else:
        print("No divergence")

if __name__ == "__main__":
    main()