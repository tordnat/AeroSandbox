import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from typing import Tuple, Dict, Union, Callable, List
from scipy import interpolate
from aerosandbox.tools.string_formatting import eng_string
import seaborn as sns


def pie(
        values: Union[np.ndarray, List[float]],
        names: List[str],
        colors: Union[np.ndarray, List[str]] = None,
        label_format: Callable[[str, float, float], str] = lambda name, value, percentage: name,
        startangle: float = 0.,
        center_text: str = None,
        x_labels: float = 1.25,
        y_max_labels: float = 1.3,
        arm_length=20,
        arm_radius=5,
):
    # TODO docs
    ax = plt.gca()
    n_wedges = len(values)

    ### Set defaults
    if colors is None:
        colors = sns.color_palette("husl", n_colors=n_wedges)

    ### Check inputs
    if not len(names) == n_wedges:
        raise ValueError()  # TODO

    ### Compute percentages
    values = np.array(values).astype(float)
    total = np.sum(values)
    percentages = 100 * values / total

    wedges, texts = ax.pie(
        x=values,
        colors=colors,
        startangle=startangle,
        wedgeprops=dict(
            width=0.3
        )
    )

    for w in wedges:
        w.theta_mid = (w.theta1 + w.theta2) / 2
        w.x_pie = np.cos(np.deg2rad(w.theta_mid))
        w.y_pie = np.sin(np.deg2rad(w.theta_mid))
        w.is_right = w.x_pie > 0

    left_wedges = [w for w in wedges if not w.is_right]
    right_wedges = [w for w in wedges if w.is_right]

    y_texts_left = y_max_labels * np.linspace(-1, 1, len(left_wedges))
    y_texts_right = y_max_labels * np.linspace(-1, 1, len(right_wedges))

    if len(left_wedges) == 1:
        y_texts_left = [w.y_pie for w in left_wedges]
    if len(right_wedges) == 1:
        y_texts_right = [w.y_pie for w in right_wedges]

    left_wedge_order = np.argsort([w.y_pie for w in left_wedges])
    for i, w in enumerate(np.array(left_wedges, "O")[left_wedge_order]):
        w.y_text = y_texts_left[i]

    right_wedge_order = np.argsort([w.y_pie for w in right_wedges])
    for i, w in enumerate(np.array(right_wedges, "O")[right_wedge_order]):
        w.y_text = y_texts_right[i]

    for i, w in enumerate(wedges):
        x_text = x_labels * np.sign(w.x_pie)
        ax.annotate(
            text=label_format(names[i], values[i], percentages[i]),
            xy=(w.x_pie, w.y_pie),
            xytext=(x_text, w.y_text),
            horizontalalignment="left" if w.is_right else "right",
            arrowprops=dict(
                arrowstyle="-",
                color="k",
                connectionstyle=f"arc,angleA={180 if w.is_right else 0},angleB={w.theta_mid},armA={arm_length},armB={arm_length},rad={arm_radius}",
                relpos=(
                    0 if w.is_right else 1,
                    0.5
                )
            ),
            va="center",
        )

    if center_text is not None:
        plt.text(
            x=0,
            y=0,
            s=center_text,
            ha="center",
            va="center",
            fontsize=16,
        )


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import aerosandbox.tools.pretty_plots as p

    data = {
        "USA"               : 336997624,
        "Mexico"            : 126705138,
        "Canada"            : 38115012,
        "Guatemala"         : 17608483,
        "Haiti"             : 11447569,
        "Cuba"              : 11256372,
        "Dominican Republic": 11117873,
        "Honduras"          : 10278345,
        "Nicaragua"         : 6850540,
        "El Salvador"       : 6314167,
        "Costa Rica"        : 5153957,
        "Panama"            : 4351267,
    }
    data["Other"] = 597678511 - np.sum(np.array(list(data.values())))

    fig, ax = plt.subplots(figsize=(9, 5))
    pie(
        values=list(data.values()),
        names=list(data.keys()),
        colors=[
            p.palettes["categorical"][0] if s in ["USA"] else "gray"
            for s in data.keys()
        ],
        label_format=lambda name, value, percentage: f"{name}, {eng_string(value)} ({percentage:.0f}%)",
        startangle=40,
        center_text="Majority of North\nAmerica's Population\nlives in USA"
    )
    p.show_plot(

    )
