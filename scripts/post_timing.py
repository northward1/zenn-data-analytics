import common
import seaborn as sns
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


def get_lcb(group, confidence=0.80, min_posts=2):
    n = len(group)
    # 最小件数未満、またはデータなしの場合は評価不能(0またはNaN)とする
    if n < min_posts:
        return np.nan

    mean = group.mean()
    std = group.std(ddof=1)

    if std == 0 or np.isnan(std):
        return mean

    sem = std / np.sqrt(n)
    # 両側80%信頼区間の下限値
    lcb = mean - stats.t.ppf((1 + confidence) / 2, df=n - 1) * sem
    return max(0, lcb)


df, fig, ax = common.setup()

days_map = {0: "月", 1: "火", 2: "水", 3: "木", 4: "金", 5: "土", 6: "日"}
days_order = ["月", "火", "水", "木", "金", "土", "日"]

df["day_of_week"] = df["published_at"].dt.dayofweek.map(days_map)
df["hour"] = df["published_at"].dt.hour

pivot_lcb = (
    df.groupby(["day_of_week", "hour"])["authenticated_liked_count"]
    .apply(get_lcb)
    .unstack()
    .reindex(days_order)
)

sns.heatmap(
    pivot_lcb,
    annot=True,
    fmt=".1f",
    cmap="YlGnBu",
    linewidths=0.5,
    cbar_kws={"label": "期待Like数の下限"},
)

plt.xlabel("時間(時)")
plt.ylabel("曜日")

common.save("liked_count_heatmap.webp")
