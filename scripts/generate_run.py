import json
import time
import math
from pathlib import Path

import pandas as pd

def main():
    run_id = time.strftime("%Y%m%d_%H%M%S")
    run_dir = Path("runs") / "milestones" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    run_meta = {
        "run_id": run_id,
        "schema_version": 1,
        "model": "rover",
        "seed": 1,
        "dt_s": 0.1,
        "steps": 120,
        "cmd_v_mps": 0.1,
        "cmd_omega_rps": 0.05,
        "start_pose": {"x_m": 0.0, "y_m": 0.0, "yaw_rad": 0.0},
        "goal": {"x_m": 1.2, "y_m": 0}
    }
    (run_dir / "run.json").write_text(json.dumps(run_meta, indent=2))

    dt = 0.1
    steps = 120
    cmd_v = 0.1
    cmd_omega = 0.05

    rows = []
    x, y, yaw = 0.0, 0.0, 0.0

    event_list = []

    def event_logger(event):
        event_list.append(event)
    
    event_logger({"t_s": 0.0, "type": "run_started"})

    for k in range(steps):
        t = k * dt

        rows.append({"t_s": t, "x_m": x, "y_m": y, "yaw_rad": yaw})

        x = x + (cmd_v * math.cos(yaw) * dt)
        y = y + (cmd_v * math.sin(yaw) * dt)
        yaw = yaw + (cmd_omega * dt)
    
    time_ended = (steps - 1) * dt
    event_logger({"t_s": time_ended, "type": "run_finished"})

    (run_dir / "events.json").write_text(json.dumps(event_list, indent=2))

    df = pd.DataFrame(rows)
    print("rows:", len(df))
    print("cols:", list(df.columns))
    print(df.head(3))
    print(df.tail(3))

    df.to_parquet(run_dir / "telemetry.parquet", index=False)
    print("Saved:", run_dir / "telemetry.parquet")

if __name__ == "__main__":
    main()