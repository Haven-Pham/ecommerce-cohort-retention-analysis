"""Consistent chart styling and figure export."""

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns

NAVY = "#0A1C33"
BLUE = "#1D6AE5"
SKY = "#38BDF8"
GREY = "#8BA5C6"
RED = "#E5484D"
GREEN = "#10B981"


def set_style() -> None:
    sns.set_theme(style="whitegrid", font_scale=1.0)
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.titleweight": "bold",
        "axes.titlesize": 13,
        "axes.titlelocation": "left",
        "axes.edgecolor": "#D0D7E2",
        "grid.color": "#E8EDF4",
        "savefig.dpi": 160,
        "savefig.bbox": "tight",
    })


def percent_axis(ax, axis: str = "y", decimals: int = 0) -> None:
    formatter = mtick.PercentFormatter(1.0, decimals=decimals)
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(formatter)


def save(fig, figures_dir: Path, name: str) -> Path:
    figures_dir = Path(figures_dir)
    figures_dir.mkdir(parents=True, exist_ok=True)
    path = figures_dir / f"{name}.png"
    fig.savefig(path)
    return path
