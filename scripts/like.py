import common
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def calc_gini(array):
    array = np.array(array, dtype=np.float64)
    if np.all(array == 0) or len(array) == 0:
        return 0.0
    array = np.sort(array)
    n = len(array)
    index = np.arange(1, n + 1)
    return ((2 * np.sum(index * array)) / (n * np.sum(array))) - (n + 1) / n


df, fig, ax = common.setup()

df_zero = df[df["authenticated_liked_count"] == 0]

summary_zero = df_zero.groupby("month").agg(
    Likeなしの記事数=("authenticated_liked_count", "count")
)


summary = df.groupby("month").agg(
    投稿数=("authenticated_liked_count", "count"),
    Like数=("authenticated_liked_count", "sum"),
    平均Like数=("authenticated_liked_count", "mean"),
    非ログインLike数=("anonymous_liked_count", "sum"),
    平均非ログインLike数=("anonymous_liked_count", "mean"),
    ブックマーク数=("bookmark_count", "sum"),
    平均ブックマーク数=("bookmark_count", "mean"),
)

summary["平均Like数"] = summary["平均Like数"].round(2)
summary["平均非ログインLike数"] = summary["平均非ログインLike数"].round(2)
summary["平均ブックマーク数"] = summary["平均ブックマーク数"].round(2)
summary = summary.rename_axis("月")

print(summary.to_markdown())

print(
    pd.concat([summary_zero, summary["投稿数"]], axis=1)
    .assign(割合=lambda df: (df["Likeなしの記事数"] / df["投稿数"] * 100).round(2))
    .rename_axis("月")
    .to_markdown()
)

sns.lineplot(
    data=summary,
    x="月",
    y="平均Like数",
    marker="o",
    ax=ax,
)


ax.set_ylabel("平均Like数", fontsize=11, labelpad=8)

common.save("article_like_count.webp")

df, fig, ax = common.setup()

summary = df.groupby("month").agg(
    投稿数=("authenticated_liked_count", "count"),
    Like数=("authenticated_liked_count", "sum"),
    平均Like数=("authenticated_liked_count", "mean"),
    非ログインLike数=("anonymous_liked_count", "sum"),
    平均非ログインLike数=("anonymous_liked_count", "mean"),
    ブックマーク数=("bookmark_count", "sum"),
    平均ブックマーク数=("bookmark_count", "mean"),
)

summary["平均Like数"] = summary["平均Like数"].round(2)
summary["平均非ログインLike数"] = summary["平均非ログインLike数"].round(2)
summary["平均ブックマーク数"] = summary["平均ブックマーク数"].round(2)
summary = summary.rename_axis("月")

print(summary.to_markdown())

sns.lineplot(
    data=summary,
    x="月",
    y="投稿数",
    marker="o",
    ax=ax,
)


ax.set_ylabel("投稿数", fontsize=11, labelpad=8)

common.save("article_count.webp")

df, fig, ax = common.setup()

gini_monthly = (
    df.groupby("month")["authenticated_liked_count"].apply(calc_gini).round(2)
)

gini_monthly = gini_monthly.rename_axis("月")
gini_monthly = gini_monthly.rename("ジニ係数")

print(gini_monthly.to_markdown())


for ym, group in df.groupby("month"):
    vals = np.sort(group["authenticated_liked_count"].values, descending=True)

    n = len(vals)

    cum_articles = np.linspace(0, 1, n + 1)

    cum_likes = np.insert(np.cumsum(vals) / np.sum(vals), 0, 0)

    gini_val = calc_gini(vals)
    ax.plot(
        cum_articles * 100,
        cum_likes * 100,
        label=str(ym) + "月",
    )

ax.set_xlabel("上位記事数の割合", fontsize=11, labelpad=8)
ax.set_ylabel("獲得Like数の累積割合", fontsize=11, labelpad=8)

ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.grid(True, linestyle=":", alpha=0.6)

ax.plot(
    [0, 100],
    [0, 100],
    color="#555555",
    linestyle="--",
    linewidth=1.5,
    alpha=0.7,
    label="完全均等線",
)


ax.legend(title="月", bbox_to_anchor=(1.02, 1), loc="upper left", frameon=False)

common.save("like_count_by_month_lorenz_curve.webp")

df, fig, ax = common.setup()

fig = sns.histplot(df, x="authenticated_liked_count")

common.save("like_hist.webp")

df, fig, ax = common.setup()

df["log_liked"] = np.log1p(df["authenticated_liked_count"])

sns.violinplot(
    df,
    x="month",
    y="log_liked",
    inner="quartile",
    cut=0,
    bw_adjust=2.5,
    split=True,
)

ax.set_xlabel("月")
ax.set_ylabel("Like数(対数スケール)")

ax.set_ylim(bottom=0)

ticks = [0, 1, 5, 10, 50, 100, 250]
ax.set_yticks(np.log1p(ticks))
ax.set_yticklabels(ticks)

common.save("like_count_vio_plot.webp")
