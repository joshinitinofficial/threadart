import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import time
from math import gcd

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(
    page_title="Thread Art – Teaching Tool",
    layout="centered"
)

st.title("🧵 Thread Art – Modular Multiplication")
st.markdown("**Rule:** `end = (i × k) mod N`")

# ==========================
# SIDEBAR CONTROLS
# ==========================
st.sidebar.header("Parameters")

N = st.sidebar.slider("Total Nodes (N)", 20, 120, 72)
k = st.sidebar.slider("Multiplier (k)", 2, 50, 8)
interval = st.sidebar.slider("Auto Animation Interval (ms)", 50, 500, 200)

show_numbers = st.sidebar.checkbox("Show Node Numbers", True)

# ==========================
# CONTROL BUTTONS
# ==========================
c1, c2, c3 = st.columns(3)

with c1:
    prev_btn = st.button("⏮ Previous")

with c2:
    next_btn = st.button("⏭ Next")

with c3:
    auto_btn = st.button("▶ Auto Animate")

# ==========================
# SESSION STATE
# ==========================
if "frame" not in st.session_state:
    st.session_state.frame = 0

# ==========================
# MATH
# ==========================
cycles = gcd(N, k - 1)

# ==========================
# PRECOMPUTE NODES
# ==========================
angles = np.linspace(0, 2*np.pi, N, endpoint=False)
x = np.cos(angles)
y = np.sin(angles)

# ==========================
# DRAW FUNCTION (ONE FRAME)
# ==========================
def draw_frame(i):
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")
    ax.set_aspect("equal")
    ax.axis("off")

    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.35, 1.35)

    # Nodes
    ax.scatter(x, y, s=20, color="cyan", zorder=3)

    if show_numbers:
        for idx in range(N):
            ax.text(
                x[idx]*1.08, y[idx]*1.08,
                str(idx),
                color="white",
                fontsize=7,
                ha="center",
                va="center"
            )

    # Completed threads
    for j in range(i):
        ax.plot(
            [x[j], x[(j * k) % N]],
            [y[j], y[(j * k) % N]],
            color="#e91e63",
            linewidth=0.8
        )

    # Active thread
    start = i
    end = (i * k) % N

    ax.plot(
        [x[start], x[end]],
        [y[start], y[end]],
        color="yellow",
        linewidth=2.2
    )

    ax.scatter(x[start], y[start], s=70, color="lime", zorder=4)
    ax.scatter(x[end], y[end], s=70, color="red", zorder=4)

    # Info text
    ax.text(
        -1.30, 1.20,
        f"Rule:\n"
        f"  end = (i × k) mod N\n\n"
        f"Step:\n"
        f"  i = {i}\n"
        f"  end = {end}\n\n"
        f"Final loops = gcd(N, k − 1)\n"
        f"gcd({N}, {k-1}) = {cycles}",
        color="white",
        fontsize=9,
        ha="left",
        va="top",
        family="monospace"
    )

    return fig

# ==========================
# FRAME CONTROL
# ==========================
if next_btn:
    st.session_state.frame = min(st.session_state.frame + 1, N - 1)

if prev_btn:
    st.session_state.frame = max(st.session_state.frame - 1, 0)

# ==========================
# CANVAS (SINGLE!)
# ==========================
canvas = st.empty()

# ==========================
# AUTO ANIMATION
# ==========================
if auto_btn:
    for i in range(st.session_state.frame, N):
        st.session_state.frame = i
        fig = draw_frame(i)
        canvas.pyplot(fig)
        time.sleep(interval / 1000)

# ==========================
# MANUAL FRAME DISPLAY
# ==========================
fig = draw_frame(st.session_state.frame)
canvas.pyplot(fig)
