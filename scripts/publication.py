import common
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df, _, _ = common.setup()

df_free_pro = df[df["publication_plan"].isin(["free", "pro"])].copy()
df_free_pro["publication_plan"] = "free+pro"

summary = (
    pd.concat([df, df_free_pro])
    .groupby("publication_plan")
    .agg(
        投稿数=("article_type", "count"),
        合計Like数=("authenticated_liked_count", "sum"),
        平均Like数=("authenticated_liked_count", "mean"),
        合計ブックマーク数=("bookmark_count", "sum"),
        平均ブックマーク数=("bookmark_count", "mean"),
    )
    .reset_index()
    .rename(columns={"publication_plan": "Publication"})
)

avg_cols = ["平均Like数", "平均ブックマーク数"]
summary[avg_cols] = summary[avg_cols].round(2)

custom_order = ["free", "pro", "free+pro", "none"]

summary["Publication"] = pd.Categorical(
    summary["Publication"], categories=custom_order, ordered=True
)
summary = summary.sort_values("Publication").reset_index(drop=True)

print(summary.to_markdown(index=False))

df, fig, ax = common.setup()

df_free_pro = df[df["publication_plan"].isin(["free", "pro"])].copy()
df_free_pro["publication_plan"] = "free+pro"

summary = (
    pd.concat([df, df_free_pro])
    .groupby(["month", "publication_plan"])
    .agg(
        投稿数=("article_type", "count"),
        平均Like数=("authenticated_liked_count", "mean"),
        平均ブックマーク数=("bookmark_count", "mean"),
    )
    .reset_index()
    .rename(columns={"publication_plan": "Publication"})
)

avg_cols = ["平均Like数", "平均ブックマーク数"]
summary[avg_cols] = summary[avg_cols].round(2)

sns.lineplot(
    data=summary,
    x="month",
    y="投稿数",
    hue="Publication",
    marker="o",
    ax=ax,
)

ax.set_xlabel("月", fontsize=11, labelpad=8)
ax.set_ylabel("投稿数", fontsize=11, labelpad=8)

common.save("article_count_by_publication.webp")

df, fig, ax = common.setup()

df_free_pro = df[df["publication_plan"].isin(["free", "pro"])].copy()
df_free_pro["publication_plan"] = "free+pro"

summary = (
    pd.concat([df, df_free_pro])
    .groupby(["month", "publication_plan"])
    .agg(
        投稿数=("article_type", "count"),
        平均Like数=("authenticated_liked_count", "mean"),
        平均ブックマーク数=("bookmark_count", "mean"),
    )
    .reset_index()
    .rename(columns={"publication_plan": "Publication"})
)

avg_cols = ["平均Like数", "平均ブックマーク数"]
summary[avg_cols] = summary[avg_cols].round(2)

sns.lineplot(
    data=summary,
    x="month",
    y="平均Like数",
    hue="Publication",
    marker="o",
    ax=ax,
)

ax.set_xlabel("月", fontsize=11, labelpad=8)
ax.set_ylabel("平均Like数", fontsize=11, labelpad=8)

common.save("article_like_count_by_publication.webp")

df, fig, ax = common.setup()

df_free_pro = df[df["publication_plan"].isin(["free", "pro"])].copy()
df_free_pro["publication_plan"] = "free+pro"

summary = (
    pd.concat([df, df_free_pro])
    .groupby(["month", "publication_plan"])
    .agg(
        投稿数=("article_type", "count"),
        平均Like数=("authenticated_liked_count", "mean"),
        平均ブックマーク数=("bookmark_count", "mean"),
    )
    .reset_index()
    .rename(columns={"publication_plan": "Publication"})
)

avg_cols = ["平均Like数", "平均ブックマーク数"]
summary[avg_cols] = summary[avg_cols].round(2)

summary["Publication"] = pd.Categorical(
    summary["Publication"],
    categories=["pro", "free", "free+pro", "none"],
    ordered=True,
)

all_summary = summary.pivot(
    index="month",
    columns="Publication",
    values=["投稿数", "平均Like数"],
)

all_summary.columns = [f"{col[1]} {col[0]}" for col in all_summary.columns]
all_summary = all_summary.reset_index()
all_summary = all_summary.rename(columns={"month": "月"})

print(all_summary.to_markdown(index=False))

# Publicationありのジニ係数など


def calc_gini(array):
    array = np.array(array, dtype=np.float64)
    if np.all(array == 0) or len(array) == 0:
        return 0.0
    array = np.sort(array)
    n = len(array)
    index = np.arange(1, n + 1)
    return ((2 * np.sum(index * array)) / (n * np.sum(array))) - (n + 1) / n


df, fig, ax = common.setup()
df_free_pro = df[df["publication_plan"].isin(["free", "pro"])].copy()
df_free_pro["publication_plan"] = "free+pro"
df = df_free_pro[df_free_pro["publication_plan"] == "free+pro"]


gini_monthly = (
    df.groupby("month")["authenticated_liked_count"].apply(calc_gini).round(2)
)

gini_monthly = gini_monthly.rename_axis("月")
gini_monthly = gini_monthly.rename("ジニ係数")

gini_publication = gini_monthly.copy().rename("free+pro")

# print(gini_monthly.to_markdown())


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

common.save("like_count_on_publication_by_month_lorenz_curve.webp")

# Publicationなしのジニ係数など

df, fig, ax = common.setup()
df = df[df["publication_plan"] == "none"]

gini_monthly = (
    df.groupby("month")["authenticated_liked_count"].apply(calc_gini).round(2)
)

gini_monthly = gini_monthly.rename_axis("月")
gini_monthly = gini_monthly.rename("none")


print(pd.concat([gini_publication, gini_monthly], axis=1).to_markdown())


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

common.save("like_count_on_non_publication_by_month_lorenz_curve.webp")

# 箱ひげ図

df, fig, ax = common.setup()
df_free_pro = df[df["publication_plan"].isin(["free", "pro"])].copy()
df_free_pro["publication_plan"] = "free+pro"
df = pd.concat(
    [
        df_free_pro[df_free_pro["publication_plan"] == "free+pro"],
        df[df["publication_plan"] == "none"],
    ]
)
df["log_liked"] = np.log1p(df["authenticated_liked_count"])

sns.violinplot(
    df,
    x="month",
    y="log_liked",
    hue="publication_plan",
    split=True,
    inner="quartile",
    cut=0,
    bw_adjust=2.5,
)

ax.set_xlabel("月")
ax.set_ylabel("Like数(対数スケール)")

ax.set_ylim(bottom=0)

ticks = [0, 1, 5, 10, 50, 100, 250]
ax.set_yticks(np.log1p(ticks))
ax.set_yticklabels(ticks)
plt.legend(title="Publication")

common.save("like_count_box_plot_publication.webp")
