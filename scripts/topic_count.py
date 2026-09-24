import common
import numpy as np
import seaborn as sns

df, fig, ax = common.setup()

df["topic_count"] = df["topics"].str.len()

summary = df.groupby("topic_count").agg(
    投稿数=("authenticated_liked_count", "count"),
    Like数=("authenticated_liked_count", "sum"),
    平均Like数=("authenticated_liked_count", "mean"),
    Like数の標準偏差=("authenticated_liked_count", "std"),
)

print(summary.to_markdown())

df["log_liked"] = np.log1p(df["authenticated_liked_count"])

sns.violinplot(
    df,
    x="topic_count",
    y="log_liked",
    inner="quartile",
    cut=0,
    bw_adjust=2.5,
    split=True,
)

ax.set_xlabel("設定したトピックの数")
ax.set_ylabel("Like数(対数スケール)")

ax.set_ylim(bottom=0)

ticks = [0, 1, 5, 10, 50, 100, 250]
ax.set_yticks(np.log1p(ticks))
ax.set_yticklabels(ticks)

common.save("like_count_vio_plot_with_topic_count.webp")
