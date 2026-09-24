import common
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

TOPIC_LANG = sorted(
    [
        "python",
        "javascript",
        "go",
        "rust",
        "swift",
        "bash",
        "java",
        "php",
        "csharp",
    ]
)

df, fig, ax = common.setup()
df = df.explode("topics")
df = df[df["topics"].isin(TOPIC_LANG)]

summary = (
    df.groupby(["month", "topics"])
    .agg(
        投稿数=("article_type", "count"),
        平均Like数=("authenticated_liked_count", "mean"),
        平均ブックマーク数=("bookmark_count", "mean"),
    )
    .reset_index()
)

sns.lineplot(
    data=summary,
    x="month",
    y="投稿数",
    hue="topics",
    marker="o",
    ax=ax,
)

plt.xlabel("月")
plt.ylabel("投稿数")

common.save("article_count_lang.webp")

df, fig, ax = common.setup()

summary_all = (
    df.groupby("month")
    .agg(
        平均Like数=("authenticated_liked_count", "mean"),
    )
    .reset_index()
)

summary_all["topics"] = "all"

df = df.explode("topics")
df = df[df["topics"].isin(TOPIC_LANG)]

summary = (
    df.groupby(["month", "topics"])
    .agg(
        投稿数=("article_type", "count"),
        平均Like数=("authenticated_liked_count", "mean"),
        平均ブックマーク数=("bookmark_count", "mean"),
    )
    .reset_index()
)

sns.lineplot(
    data=pd.concat([summary, summary_all]),
    x="month",
    y="平均Like数",
    hue="topics",
    marker="o",
    ax=ax,
)

plt.xlabel("月")
plt.ylabel("平均Like数")

common.save("article_like_count_lang.webp")

TOPIC_AI = sorted(
    [
        "claudecode",
        "codex",
        "chatgpt",
        "openai",
        "gemini",
        "qwen",
        "deepseek",
        "claude",
    ]
)

df, fig, ax = common.setup()
df = df.explode("topics")
df = df[df["topics"].isin(TOPIC_AI)]

summary = (
    df.groupby(["month", "topics"])
    .agg(
        投稿数=("article_type", "count"),
        平均Like数=("authenticated_liked_count", "mean"),
        平均ブックマーク数=("bookmark_count", "mean"),
    )
    .reset_index()
)

sns.lineplot(
    data=summary,
    x="month",
    y="投稿数",
    hue="topics",
    marker="o",
    ax=ax,
)

plt.xlabel("月")
plt.ylabel("投稿数")

common.save("article_count_ai.webp")

df, fig, ax = common.setup()

summary_all = (
    df.groupby("month")
    .agg(
        平均Like数=("authenticated_liked_count", "mean"),
    )
    .reset_index()
)

summary_all["topics"] = "all"

df = df.explode("topics")
df = df[df["topics"].isin(TOPIC_AI)]

summary = (
    df.groupby(["month", "topics"])
    .agg(
        投稿数=("article_type", "count"),
        平均Like数=("authenticated_liked_count", "mean"),
        平均ブックマーク数=("bookmark_count", "mean"),
    )
    .reset_index()
)

sns.lineplot(
    data=pd.concat([summary, summary_all]),
    x="month",
    y="平均Like数",
    hue="topics",
    marker="o",
    ax=ax,
)

plt.xlabel("月")
plt.ylabel("平均Like数")

common.save("article_like_count_ai.webp")

df, fig, ax = common.setup()

df = df.explode("topics")
df = df[df["topics"].isin(TOPIC_LANG)]

summary = (
    df.groupby(["month", "topics"])
    .agg(
        投稿数=("article_type", "count"),
        合計Like数=("authenticated_liked_count", "sum"),
        平均ブックマーク数=("bookmark_count", "mean"),
    )
    .reset_index()
)

sns.lineplot(
    data=summary,
    x="month",
    y="合計Like数",
    hue="topics",
    marker="o",
    ax=ax,
)

plt.xlabel("月")
plt.ylabel("合計Like数")

common.save("article_like_countsum_lang.webp")
