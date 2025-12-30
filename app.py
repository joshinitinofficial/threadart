import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import time
from math import gcd

# ==========================
# STREAMLIT CONFIG
# ==========================
st.set_page_config(
    page_title="Thread Art – Teaching Tool",
    layout="centered"
)

st.title("🧵 Thread Art – Modular Multiplication (Teaching Mode)")
st.markdown("**Rule:** `end = (i × k) mod N`")

# ==========================
# SIDEBAR INPUTS
# ==========================
st.sidebar.header("Parameters")

N = st.sidebar.slider("Total Nodes (N)", 20, 120, 72)
k = st.sidebar.slider("Multiplier (k)", 2, 50, 8)
interval = st.sidebar.slider("Animation Interval (ms)", 50, 500, 200)

show_numbers = st.sidebar.checkbox("Show Node Numbers", True)

# ==========================
# BUTTONS
# ==========================
col1, col2, col3 = st.columns(3)

with col1:
    start_anim = st.button("▶ Start Animation")

with col2:
    prev_frame = st.button("⏮ Previous")

with col3:
    next_frame = st.button("⏭ Next")

# ==========================
# SESSION STATE (IMPORTANT)
# ==========================
if "frame" not in st.session_state:
    st.session_state.frame = 0

# ==========================
# MATH
# ==========================
cycles = gcd(N, k - 1)

# ==========================
# NODE SETUP
# ==========================
angles = np.linspace(0, 2*np.pi, N, endpoint=False)
x = np.cos(angles)
y = np.sin(angles)

# ==========================
# DRAW FUNCTION
# ==========================
def draw_frame(i):
    fig, ax = plt.subplots(figsize=(5.5, 5.5))  # 👈 SMALLER SIZE
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
                x[idx]*1.08,
                y[idx]*1.08,
                str(idx),
                color="white",
                fontsize=7,
                ha="center",
                va="center"
            )

    # Draw completed threads
    for j in range(i):
        ax.plot(
            [x[j], x[(j * k) % N]],
            [y[j], y[(j * k) % N]],
            color="#e91e63",
            linewidth=0.8,
            alpha=0.9
        )

    # Active line
    start = i % N
    end = (i * k) % N

    ax.plot(
        [x[start], x[end]],
        [y[start], y[end]],
        color="yellow",
        linewidth=2.2
    )

    ax.scatter(x[start], y[start], s=70, color="lime", zorder=4)
    ax.scatter(x[end], y[end], s=70, color="red", zorder=4)

    # Math text
    ax.text(
        -1.30, 1.20,
        f"Rule:\n"
        f"  end = (i × k) mod N\n\n"
        f"Current step:\n"
        f"  i = {i}\n"
        f"  end = {end}\n\n"
        f"Final structure:\n"
        f"  focal loops = gcd(N, k − 1)\n"
        f"  gcd({N}, {k-1}) = {cycles}",
        color="white",
        fontsize=9,
        ha="left",
        va="top",
        family="monospace"
    )

    return fig

# ==========================
# FRAME CONTROL LOGIC
# ==========================
if next_frame:
    st.session_state.frame = min(st.session_state.frame + 1, N - 1)

if prev_frame:
    st.session_state.frame = max(st.session_state.frame - 1, 0)

# ==========================
# ANIMATION MODE
# ==========================
if start_anim:
    for i in range(st.session_state.frame, N):
        st.session_state.frame = i
        fig = draw_frame(i)
        st.pyplot(fig)
        time.sleep(interval / 1000)

# ==========================
# STEP MODE DISPLAY
# ==========================
fig = draw_frame(st.session_state.frame)
st.pyplot(fig)

# ==========================
# FOOTER
# ==========================
st.markdown(
    f"**Teaching Tip:** Pause at any step and explain why "
    f"`{st.session_state.frame} × {k} mod {N} = {(st.session_state.frame * k) % N}`"
)
