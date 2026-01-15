import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button

def main():
    if len(sys.argv) < 2:
        print("Usage: uv run scripts/view_run.py runs/milestones/<run_id>")
        raise SystemExit(1)
    
    run_dir = Path(sys.argv[1])
    df = pd.read_parquet(run_dir / "telemetry.parquet")
    x = df["x_m"].to_numpy()
    y = df["y_m"].to_numpy()

    fig, ax = plt.subplots()

    fig.subplots_adjust(bottom=0.25)

    margin = 0.5

    ax.set_xlim(min(x)-margin, max(x)+margin)
    ax.set_ylim(min(y)-margin, max(y)+margin)
    ax.set_aspect("equal")

    line, = ax.plot([], [])
    dot, = ax.plot([], [], marker="o")
    
    axfreq = fig.add_axes([0.25, 0.1, 0.65, 0.03])
    freq_slider = Slider(
        ax=axfreq,
        label='Slider',
        valmin=0,
        valmax=len(x) - 1,
        valinit=0
    )

    ax_button = fig.add_axes([0.8, 0.025, 0.1, 0.04])
    button = Button(ax_button, "Play")

    is_program = False

    def update(i):
        nonlocal is_program
        is_program = True
        line.set_data(x[:i+1], y[:i+1])
        dot.set_data([x[i]], [y[i]])
        freq_slider.set_val(i)
        is_program = False
        return line, dot
        
    def changed_slider(i):
        if is_program == True:
            return
        else:
            anim.pause()
            i = int(i)
            line.set_data(x[:i+1], y[:i+1])
            dot.set_data([x[i]], [y[i]])
            anim.frame_seq = iter(range(i, len(x)))

    anim = animation.FuncAnimation(
        fig,
        update,
        frames=120,
        interval=50,
    )

    freq_slider.on_changed(changed_slider)

    def unpause(event):
        anim.resume()
    button.on_clicked(unpause)

    writer = animation.PillowWriter(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    anim.save(run_dir / "animation.gif", writer=writer)

    plt.show()



if __name__ == "__main__":
    main()