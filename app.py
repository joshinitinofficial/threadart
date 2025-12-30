import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import time
from math import gcd

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(
    page_title="Thread Art – Modular Multiplication",
    layout="centered"
)

# ==========================
# SESSION STATE INIT
# ==========================
if "frame" not in st.session_state:
    st.session_state.frame = 0

if "auto_play" not in st.session_state:
    st.session_state.auto_play = False

# ==========================
# TITLE (KEEP TOP)
# ==========================
st.title("🧵 Thread Art – Modular Multiplication")
st.markdown("**Rule:** `end = (i × k) mod N`")

# ==========================
# SIDEBAR CONTROLS
# ==========================
st.sidebar.header("Parameters")

N = st.sidebar.slider("Total Nodes (N)", 20, 120, 37)
k = st.sidebar.slider("Multiplier (k)", 2, 50, 9)
interval = st.sidebar.slider("Auto Animation Interval (ms)", 50, 500, 250)
show_numbers = st.sidebar.checkbox("Show Node Numbers", True)

# 🔴 Clamp frame when N changes
st.session_state.frame = min(st.session_state.frame, N - 1)

# ==========================
# BUTTON ROW (FIXED POSITION)
# ==========================
b1, b2, b3, b4 = st.columns(4)

with b1:
    prev_btn = st.button("⏮ Previous", use_container_width=True)

with b2:
    next_btn = st.button("⏭ Next", use_container_width=True)

with b3:
    auto_btn = st.button("▶ Auto Animate", use_container_width=True)

with b4:
    stop_btn = st.button("⏸ Stop", use_container_width=True)

# ==========================
# BUTTON LOGIC
# ==========================
if prev_btn:
    st.session_state.auto_play = False
    st.session_state.frame = max(st.session_state.frame - 1, 0)

if next_btn:
    st.session_state.auto_play = False
    st.session_state.frame = min(st.session_state.frame + 1, N - 1)

if auto_btn:
    st.session_state.auto_play = True

if stop_btn:
    st.session_state.auto_play = False

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
# DRAW FRAME FUNCTION
# ==========================
def draw_frame(i):
    fig, ax = plt.subplots(figsize=(5.2, 5.2))
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")
    ax.set_aspect("equal")
    ax.axis("off")

    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)

    # Nodes
    ax.scatter(x, y, s=22, color="cyan", zorder=3)

    if show_numbers:
        for idx in range(N):
            ax.text(
                x[idx] * 1.08,
                y[idx] * 1.08,
                str(idx),
                color="white",
                fontsize=7,
                ha="center",
                va="center"
            )

    # Completed threads
    for j in range(i):
        end_j = (j * k) % N
        ax.plot(
            [x[j], x[end_j]],
            [y[j], y[end_j]],
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
        -1.28, 1.18,
        f"Rule:\n"
        f"  end = (i × k) mod N\n\n"
        f"Step:\n"
        f"  i = {i}\n"
        f"  end = {end}\n\n"
        f"Final loops:\n"
        f"  gcd(N, k − 1) = {cycles}",
        color="white",
        fontsize=9,
        ha="left",
        va="top",
        family="monospace"
    )

    return fig

# ==========================
# CANVAS (PINNED, NO SCROLL)
# ==========================
canvas = st.container()
with canvas:
    fig = draw_frame(st.session_state.frame)
    st.pyplot(fig)

# ==========================
# AUTO PLAY LOOP (SAFE)
# ==========================
if st.session_state.auto_play:
    time.sleep(interval / 1000)
    st.session_state.frame += 1

    if st.session_state.frame >= N:
        st.session_state.auto_play = False
        st.session_state.frame = N - 1

    st.experimental_rerun()
