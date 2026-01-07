import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run python scripts/plot_run.py runs/milestones/<run_id>")
        raise SystemExit(1)

    run_dir = Path(sys.argv[1])
    df = pd.read_parquet(run_dir / "telemetry.parquet")

    plt.figure()
    plt.plot(df["x_m"], df["y_m"])
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title(run_dir.name)
    plt.axis("equal")
    out = run_dir / "path.png"
    plt.savefig(out, dpi=150)

    print("Saved:", out)


if __name__ == "__main__":
    main()