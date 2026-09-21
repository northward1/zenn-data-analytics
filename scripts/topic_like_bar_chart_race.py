import common
import bar_chart_race as bcr
import pandas as pd
import matplotlib.pyplot as plt

df, _, _ = common.setup(dpi=144)

plt.close("all")

fig, ax = plt.subplots(figsize=(9, 6), dpi=144)

fig.subplots_adjust(
    top=0.975,
    bottom=0.075,
    left=0.125,
    right=0.975,
)

df_exploded = df.explode("topics").reset_index(drop=True)

result_df = pd.crosstab(
    index=df_exploded["month"],
    columns=df_exploded["topics"],
    values=df_exploded["authenticated_liked_count"],
    aggfunc="sum",
)
result_df.index = pd.date_range(start="2024-01-01", periods=len(result_df), freq="MS")

bcr.bar_chart_race(
    df=result_df,
    filename="images/topic_like_bar_chart_race.webp",
    n_bars=15,
    period_fmt="%b",
    steps_per_period=16,
    period_length=2000,
    fig=fig,
    filter_column_colors=True,
)
