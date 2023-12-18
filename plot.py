import pandas as pd
import matplotlib.pyplot as plt
from utils import pareto_front
import numpy as np

SMALL_SIZE = 14
MEDIUM_SIZE = 22
BIGGER_SIZE = 26

plt.rc("font", size=SMALL_SIZE)  # controls default text sizes
plt.rc("axes", titlesize=MEDIUM_SIZE)  # fontsize of the axes title
plt.rc(
    "axes", labelsize=MEDIUM_SIZE
)  # fontsize of the x and y labels for the small plots
plt.rc("xtick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc("ytick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc("legend", fontsize=MEDIUM_SIZE)  # legend fontsize
plt.rc("figure", titlesize=BIGGER_SIZE)  # fontsize of the figure title
plt.rc(
    "figure", labelsize=BIGGER_SIZE
)  # fontsize of the x and y labels for the big plots

df = pd.read_csv("glove_experiment.txt")

df["method"] = df["method"].str.split("_").str[0]

grouped_data = df.groupby(["filter_width", "method"])

num_plots = len(df["filter_width"].unique())
num_cols = 4
num_rows = (num_plots + num_cols - 1) // num_cols
plot_scaler = 6

fig, axes = plt.subplots(
    num_rows,
    num_cols,
    figsize=(plot_scaler * num_cols, plot_scaler * num_rows),
    tight_layout=True,
)
axes = axes.reshape(-1)

for (filter_width, method), group in grouped_data:
    ax = axes[df["filter_width"].unique().tolist().index(filter_width)]
    sorted_group = group.sort_values(by="recall", ascending=False)

    x, y = pareto_front(
        np.array(sorted_group["recall"]), np.array(sorted_group["average_time"])
    )

    if len(x) == 1:
        ax.plot(x, y, label=method, markersize=20, marker="x")
    else:
        ax.plot(x, y, label=method)
    ax.set_title(f"Filter Width: {filter_width}")

fig.supxlabel("Recall")
fig.supylabel("Average Latency")
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, 0.98), ncol=3)


plt.tight_layout()
plt.savefig("glove_experiment.png", bbox_inches="tight")