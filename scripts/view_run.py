import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def main():
    if len(sys.argv) < 2:
        print("Usage: uv run scripts/view_run.py runs/milestones/<run_id>")
        raise SystemExit(1)
    
    run_dir = Path(sys.argv[1])
    df = pd.read_parquet(run_dir / "telemetry.parquet")
    x = df["x_m"].to_numpy()
    y = df["y_m"].to_numpy()

    fig, ax = plt.subplots()

    margin = 2

    ax.set_xlim(min(x)-margin, max(x)+margin)
    ax.set_ylim(min(y)-margin, max(y)+margin)
    ax.set_aspect("equal")

    line, = ax.plot([], [])
    dot, = ax.plot([], [], marker="o")

    def update(i):
        line.set_data(x[:i+1], y[:i+1])
        dot.set_data([x[i]], [y[i]])
        return line, dot
    
    anim = animation.FuncAnimation(
        fig,
        update,
        frames=120,
        interval=50,
    )

    writer = animation.PillowWriter(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    anim.save(run_dir / "animation.gif", writer=writer)

    plt.show()



if __name__ == "__main__":
    main()