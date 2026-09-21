import common

TOP_N = 10

df, fig, ax = common.setup()

df = df.explode("topics")

summary = df.groupby(["month", "topics"]).size().reset_index(name="投稿数")

summary = summary.sort_values(by=["month", "投稿数"], ascending=[True, False])

top_summary = summary.groupby("month").head(TOP_N)

top_summary["rank"] = top_summary.groupby("month").cumcount() + 1

pivoted = top_summary.pivot(index="month", columns="rank", values=["topics", "投稿数"])

pivoted = pivoted.reorder_levels([1, 0], axis=1).sort_index(axis=1)


def col_name(val, rank):
    if val == "topics":
        return f"{rank}位"
    else:
        return f"投稿数"


pivoted.columns = [col_name(val, rank) for rank, val in pivoted.columns]

result = pivoted.reset_index()
result = result.rename(columns={"month": "月"})

print(result.to_markdown(index=False))

# Like数

df, fig, ax = common.setup()

df = df.explode("topics")

summary = (
    df.groupby(["month", "topics"])["authenticated_liked_count"]
    .sum()
    .reset_index(name="Like数")
)

summary = summary.sort_values(by=["month", "Like数"], ascending=[True, False])

top_summary = summary.groupby("month").head(TOP_N)

top_summary["rank"] = top_summary.groupby("month").cumcount() + 1

pivoted = top_summary.pivot(index="month", columns="rank", values=["topics", "Like数"])

pivoted = pivoted.reorder_levels([1, 0], axis=1)
ranks = sorted(top_summary["rank"].unique())
pivoted = pivoted[[(rank, val) for rank in ranks for val in ["topics", "Like数"]]]


def col_name(val, rank):
    if val == "topics":
        return f"{rank}位"
    else:
        return f"Like数"


pivoted.columns = [col_name(val, rank) for rank, val in pivoted.columns]

result = pivoted.reset_index()
result = result.rename(columns={"month": "月"})

print(result.to_markdown(index=False))
