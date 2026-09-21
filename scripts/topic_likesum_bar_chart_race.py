import common
import bar_chart_race as bcr
import pandas as pd
import matplotlib.pyplot as plt

DPI = 100

df, fig, ax = common.setup()

plt.close("all")

fig, ax = plt.subplots(figsize=(9, 6), dpi=DPI)

fig.subplots_adjust(
    top=0.975,
    bottom=0.075,
    left=0.125,
    right=0.975,
)

df_exploded = df.explode("topics").reset_index(drop=True)

result_df = pd.crosstab(
    index=df_exploded["date"],
    columns=df_exploded["topics"],
    values=df_exploded["authenticated_liked_count"],
    aggfunc="sum",
)
result_df.index.name = None

bcr.bar_chart_race(
    df=result_df.cumsum().copy(),
    filename="images/topic_likesum_bar_chart_race.webp",
    period_fmt="%m月 %d日",
    n_bars=15,
    steps_per_period=1,
    period_length=25,
    filter_column_colors=True,
    fig=fig,
    dpi=DPI,
)
