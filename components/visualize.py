import numpy as np
import plotly.graph_objects as go
from PIL import Image, ImageDraw


def draw_2d_welds_overlay(base_img, df):
    if base_img is None:
        base_img = Image.new("RGB", (1100, 650), color=(245, 245, 245))

    img = base_img.copy().convert("RGB")
    d = ImageDraw.Draw(img)

    for _, r in df.iterrows():
        if str(r.get("Status", "OK")) == "Delete":
            continue

        x1, y1, x2, y2 = int(r["x1"]), int(r["y1"]), int(r["x2"]), int(r["y2"])
        weld_index = str(r["Weld_Index"])

        d.rectangle([x1, y1, x2, y2], outline=(0, 0, 0), width=3)
        d.text((x1, max(0, y1 - 18)), weld_index, fill=(0, 0, 0))

    return img


def pil_to_plotly_figure(pil_img, height: int = 420):
    arr = np.array(pil_img.convert("RGB"))
    fig = go.Figure(go.Image(z=arr))
    fig.update_layout(
        height=height,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    fig.update_xaxes(showticklabels=False, visible=False)
    fig.update_yaxes(showticklabels=False, visible=False, scaleanchor="x")
    return fig


def render_3d_welds_plot(df, height: int = 420):
    df2 = df[df["Status"] != "Delete"].copy()

    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=df2["x"].astype(float),
                y=df2["y"].astype(float),
                z=df2["z"].astype(float),
                mode="markers",
                marker=dict(size=5),
                text=df2["Weld_Index"].astype(str)
            )
        ]
    )
    fig.update_layout(
        height=height,
        scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Z"),
        margin=dict(l=0, r=0, t=10, b=0)
    )
    return fig
