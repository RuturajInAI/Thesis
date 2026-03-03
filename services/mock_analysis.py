import pandas as pd
import numpy as np


def mock_analyze_joints(mode: str, n: int = 10) -> pd.DataFrame:
    rng = np.random.default_rng(10)

    parts = ["Sheet A", "Sheet B", "Sheet C", "Sheet D", "Sheet E"]
    weld_types = ["Fillet", "Double-Sided Fillet", "Butt"]

    weld_side = ["single-sided", "double-sided"]
    weld_size = ["a3", "a4", "a6", None]
    weld_length = [None, None, None, 120, 180, 240]

    rows = []
    for i in range(n):
        a = rng.choice(parts)
        b = rng.choice([p for p in parts if p != a])

        if mode == "2D":
            x1 = int(rng.integers(80, 900))
            y1 = int(rng.integers(80, 500))
            w = int(rng.integers(50, 140))
            h = int(rng.integers(40, 120))
            x2 = min(1100, x1 + w)
            y2 = min(650, y1 + h)

            rows.append({
                "Preview": "⟂",
                "Part_Index": int(rng.integers(1, 4)),
                "Weld_Type_2D": rng.choice(["Bevel_Groove", "Fillet"]),
                "Weld_Side": rng.choice(weld_side),
                "Weld_Size": rng.choice(weld_size),
                "Weld_Length": rng.choice(weld_length),

                "Weld_Index": i + 1,
                "Part_A": a,
                "Part_B": b,
                "Weld_Type": rng.choice(weld_types),
                "Status": "OK",
                "Done": False,
                "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                "x": float(rng.uniform(-1, 1)),
                "y": float(rng.uniform(-1, 1)),
                "z": float(rng.uniform(-1, 1)),
            })
        else:
            rows.append({
                "Weld_Index": i + 1,
                "Part_A": a,
                "Part_B": b,
                "Weld_Type": rng.choice(weld_types),
                "Status": "OK",
                "Done": False,
                "x1": 0, "y1": 0, "x2": 0, "y2": 0,
                "x": float(rng.uniform(-10, 10)),
                "y": float(rng.uniform(-10, 10)),
                "z": float(rng.uniform(-10, 10)),
            })

    return pd.DataFrame(rows)