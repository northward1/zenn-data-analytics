from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

DATA_PATH = Path("data.jsonl")
IMAGES_DIR = Path("images")


def setup(dpi=300):
    sns.set_theme(style="whitegrid")
    plt.rcParams["font.family"] = "Noto Sans CJK JP"

    df = pd.read_json(DATA_PATH, lines=True)
    df["published_at"] = pd.to_datetime(df["published_at"])

    df["date"] = df["published_at"].dt.normalize()

    df["year"] = df["published_at"].dt.strftime("%y")
    df = df[df["year"] == "26"]

    df["month"] = df["published_at"].dt.strftime("%m")
    df = df[df["month"] != "09"]
    df["month"] = df["month"].astype(int)

    fig, ax = plt.subplots(figsize=(10, 6), dpi=dpi)

    return df, fig, ax


def save(path="image.webp"):
    sns.despine()
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / path, dpi=300, bbox_inches="tight")
