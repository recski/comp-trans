import json

import matplotlib.pyplot as plt
import numpy as np


def plot_gunning(to_plot):
    plt.rcParams['figure.figsize'] = [10, 7.5]
    x = np.linspace(0, 25, 25)  # values of avg sentence length
    thresholds = list(range(0, 20, 2))
    for p in thresholds:
        y = p / 0.4 - x
        plt.plot(x, y, color="black")
        if p >= 6 and p <= 12:
            plt.text(x[p], y[p], f"F={p}")
        elif p == 4:
            plt.text(9, 1, f"F={p}")
        elif p == 14:
            plt.text(21.5, 13.5, f"F={p}")
        elif p == 16:
            plt.text(24, 16, f"F={p}")

    colors = {"1984": "y", "ted3": "r", "fgm": "g", "DC567": "b"}

    sample_labels = {
        "1984": (21, 6.5),
        "ted3": (14.5, 6.5),
        "fgm": (7, 3.5),
        "DC567": (22.5, 18.5),
    }

    labels = {
        "en_orig": 'E',
        "hu_human": 'H',
        "hu_deepl": 'M'
    }

    for prefix, stats in to_plot.items():
        for stat, point in stats.items():
            plt.plot(*point, marker=f'${labels[stat]}$', ls='none', color=colors[prefix])
            # plt.plot(*point, marker='.', ls='none', color=colors[prefix])
            # plt.annotate(labels[stat], point, color=colors[prefix])

        plt.text(*sample_labels[prefix], prefix.upper(), color=colors[prefix])

    # plt.plot(14.99, 14.94, marker="$W$", ls="none", color='green')
    # plt.text(15, 15, 'webcorpus', color='green')

    plt.xlim([5, 25])
    plt.ylim([0, 20])
    plt.xlabel("words / sentence", color="#1C2833")
    plt.ylabel("% of complex words", color="#1C2833")
    plt.grid()
    plt.savefig('gunning.png')
    plt.show()


def get_stats():
    with open("stats.json") as f:
        all_stats = json.load(f)

    to_plot = {}
    for prefix, versions in all_stats.items():
        to_plot[prefix] = {}
        for version, stats in versions.items():
            to_plot[prefix][version] = (
                stats["words per sen"],
                100 * stats["complex word ratio"],
            )

    return to_plot


def main():
    to_plot = get_stats()
    plot_gunning(to_plot)


if __name__ == "__main__":
    main()
