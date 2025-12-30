import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import time
from math import gcd

# ==========================
# STREAMLIT CONFIG
# ==========================
st.set_page_config(page_title="Thread Art Animation", layout="wide")

st.title("🧵 Thread Art – Live Modular Multiplication")
st.markdown("**Rule:** `end = (i × k) mod N`")

# ==========================
# SIDEBAR INPUTS
# ==========================
st.sidebar.header("Parameters")

N = st.sidebar.slider("Total Nodes (N)", 20, 150, 72)
k = st.sidebar.slider("Multiplier (k)", 2, 50, 8)
interval = st.sidebar.slider("Animation Interval (ms)", 50, 500, 250)

show_numbers = st.sidebar.checkbox("Show Node Numbers", True)
start_button = st.sidebar.button("▶ Start Animation")

# ==========================
# MATH
# ==========================
cycles = gcd(N, k - 1)

# ==========================
# PLACEHOLDER
# ==========================
plot_placeholder = st.empty()

# ==========================
# PRECOMPUTE NODES
# ==========================
angles = np.linspace(0, 2*np.pi, N, endpoint=False)
x = np.cos(angles)
y = np.sin(angles)

# ==========================
# START ANIMATION
# ==========================
if start_button:

    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")
    ax.set_aspect("equal")
    ax.axis("off")

    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.4, 1.4)

    # Draw nodes
    ax.scatter(x, y, s=25, color="cyan", zorder=3)

    if show_numbers:
        for i in range(N):
            ax.text(
                x[i]*1.1, y[i]*1.1,
                str(i),
                color="white",
                fontsize=7,
                ha="center",
                va="center"
            )

    # ✅ Create ONE persistent text object
    info_text = ax.text(
        -1.35, 1.25,
        "",
        color="white",
        fontsize=10,
        ha="left",
        va="top",
        family="monospace"
    )

    active_line = None
    start_dot = None
    end_dot = None

    for i in range(N):

        start = i
        end = (i * k) % N

        # Convert previous active line to permanent thread
        if active_line:
            active_line.set_color("#e91e63")
            active_line.set_linewidth(0.8)

        # Remove old markers
        if start_dot:
            start_dot.remove()
        if end_dot:
            end_dot.remove()

        # Draw active line
        active_line, = ax.plot(
            [x[start], x[end]],
            [y[start], y[end]],
            color="yellow",
            linewidth=2.5,
            zorder=2
        )

        start_dot = ax.scatter(x[start], y[start], s=90, color="lime", zorder=4)
        end_dot   = ax.scatter(x[end], y[end], s=90, color="red", zorder=4)

        # ✅ Update text safely
        info_text.set_text(
            f"Rule:\n"
            f"  end = (i × k) mod N\n\n"
            f"Current step:\n"
            f"  i = {i}\n"
            f"  k = {k}, N = {N}\n"
            f"  end = {end}\n\n"
            f"Final structure:\n"
            f"  focal loops = gcd(N, k − 1)\n"
            f"  gcd({N}, {k-1}) = {cycles}"
        )

        plot_placeholder.pyplot(fig)
        time.sleep(interval / 1000)

    st.success("Animation completed successfully!")

# ==========================
# FOOTER
# ==========================
st.markdown("---")
st.markdown(
    "**Math Insight:** The final number of focal loops depends only on "
    "`gcd(N, k − 1)` — independent of animation speed."
)
