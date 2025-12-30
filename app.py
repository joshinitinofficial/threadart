import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from math import gcd

# ==========================
# STREAMLIT PAGE CONFIG
# ==========================
st.set_page_config(
    page_title="Thread Art – Modular Multiplication",
    layout="centered"
)

st.title("🧵 Thread Art – Modular Multiplication Visualizer")
st.markdown(
    "Visualizing **end = (i × k) mod N** with predicted focal loops using **gcd(N, k−1)**"
)

# ==========================
# USER INPUTS
# ==========================
st.sidebar.header("Parameters")

N = st.sidebar.slider("Total Nodes (N)", 20, 200, 60, step=1)
k = st.sidebar.slider("Multiplier (k)", 2, 50, 7, step=1)

show_numbers = st.sidebar.checkbox("Show Node Numbers", True)
show_active_line = st.sidebar.checkbox("Highlight Active Line", True)

# ==========================
# MATH
# ==========================
cycles = gcd(N, k - 1)

# ==========================
# PLOT FUNCTION
# ==========================
def draw_thread_art():
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")
    ax.set_aspect("equal")
    ax.axis("off")

    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.4, 1.4)

    angles = np.linspace(0, 2*np.pi, N, endpoint=False)
    x = np.cos(angles)
    y = np.sin(angles)

    # Nodes
    ax.scatter(x, y, s=25, color="cyan", zorder=3)

    if show_numbers:
        for i in range(N):
            ax.text(
                x[i]*1.1, y[i]*1.1,
                str(i),
                color="white",
                fontsize=7,
                ha="center", va="center"
            )

    # Draw threads
    for i in range(N):
        start = i
        end = (i * k) % N

        ax.plot(
            [x[start], x[end]],
            [y[start], y[end]],
            color="#e91e63",
            linewidth=0.8,
            alpha=0.9,
            zorder=2
        )

    # Optional highlight first mapping
    if show_active_line:
        ax.plot(
            [x[1], x[(1 * k) % N]],
            [y[1], y[(1 * k) % N]],
            color="yellow",
            linewidth=2.5,
            zorder=4
        )
        ax.scatter(x[1], y[1], s=90, color="lime", zorder=5)
        ax.scatter(
            x[(1 * k) % N], y[(1 * k) % N],
            s=90, color="red", zorder=5
        )

    # Math text
    ax.text(
        -1.35, 1.25,
        f"Rule:\n"
        f"  end = (i × k) mod N\n\n"
        f"Parameters:\n"
        f"  N = {N},  k = {k}\n\n"
        f"Final Structure:\n"
        f"  focal loops = gcd(N, k − 1)\n"
        f"  gcd({N}, {k-1}) = {cycles}",
        color="white",
        fontsize=10,
        ha="left",
        va="top",
        family="monospace"
    )

    return fig

# ==========================
# RENDER
# ==========================
fig = draw_thread_art()
st.pyplot(fig)

# ==========================
# FOOTER
# ==========================
st.markdown("---")
st.markdown(
    "📐 **Math Insight:** The number of distinct focal loops is fully determined by "
    "**gcd(N, k − 1)** — visible even before drawing begins."
)
