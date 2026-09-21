import common
import seaborn as sns

df, _, _ = common.setup()

summary = (
    df.groupby("article_type")
    .agg(
        記事数=("article_type", "count"),
        合計Like数=("authenticated_liked_count", "sum"),
        平均Like数=("authenticated_liked_count", "mean"),
        合計ブックマーク数=("bookmark_count", "sum"),
        平均ブックマーク数=("bookmark_count", "mean"),
    )
    .reset_index()
)

summary["記事数割合(%)"] = (summary["記事数"] / summary["記事数"].sum() * 100).round(1)
summary["平均Like数"] = summary["平均Like数"].round(2)
summary["平均ブックマーク数"] = summary["平均ブックマーク数"].round(2)

columns_order = [
    "article_type",
    "記事数",
    "記事数割合(%)",
    "合計Like数",
    "平均Like数",
    "合計ブックマーク数",
    "平均ブックマーク数",
]
summary = summary[columns_order]

summary = summary.sort_values(by="article_type", ascending=False).reset_index(drop=True)
summary = summary.rename(columns={"article_type": "カテゴリー"})

print(summary.to_markdown(index=False))

df, fig, ax = common.setup()

aggregated = (
    df.groupby(["month", "article_type"])
    .agg(
        投稿数=("authenticated_liked_count", "count"),
        Like数=("authenticated_liked_count", "sum"),
        平均Like数=("authenticated_liked_count", "mean"),
    )
    .reset_index()
    .rename(columns={"article_type": "Type"})
)

sns.lineplot(
    data=aggregated,
    x="month",
    y="投稿数",
    hue="Type",
    marker="o",
    ax=ax,
)

ax.set_xlabel("月", fontsize=11, labelpad=8)
ax.set_ylabel("投稿数", fontsize=11, labelpad=8)

common.save("article_count_by_type.webp")

df, fig, ax = common.setup()

aggregated = (
    df.groupby(["month", "article_type"])
    .agg(
        投稿数=("authenticated_liked_count", "count"),
        Like数=("authenticated_liked_count", "sum"),
        平均Like数=("authenticated_liked_count", "mean"),
    )
    .reset_index()
    .rename(columns={"article_type": "Type"})
)

sns.lineplot(
    data=aggregated,
    x="month",
    y="平均Like数",
    hue="Type",
    marker="o",
    ax=ax,
)

ax.set_xlabel("月", fontsize=11, labelpad=8)
ax.set_ylabel("平均Like数", fontsize=11, labelpad=8)

common.save("article_like_count_by_type.webp")

aggregated["平均Like数"] = aggregated["平均Like数"].round(2)

res = aggregated.pivot(index="month", columns="Type", values=["投稿数", "平均Like数"])
res.columns = [f"{col[1]} {col[0]}" for col in res.columns]
res = res.rename_axis("月")
print(res.to_markdown())
