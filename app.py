import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import time
from math import gcd

# Page config
st.set_page_config(page_title="Thread Art – Modular Multiplication", layout="wide")

# Session state
if "frame" not in st.session_state:
    st.session_state.frame = 0
if "auto_play" not in st.session_state:
    st.session_state.auto_play = False

# Sidebar inputs
st.sidebar.header("Parameters")
N = st.sidebar.slider("Total Nodes (N)", 20, 120, 72)
k = st.sidebar.slider("Multiplier (k)", 2, 50, 9)
interval = st.sidebar.slider("Auto Animation Interval (ms)", 50, 500, 250)
show_numbers = st.sidebar.checkbox("Show Node Numbers", True)

st.session_state.frame = min(st.session_state.frame, N - 1)

# Title
st.title("🧵 Thread Art – Modular Multiplication")
st.write("Rule: end = (i × k) mod N")

# Controls
c1, c2, c3, c4 = st.columns(4)
with c1:
    prev_btn = st.button("⏮ Previous")
with c2:
    next_btn = st.button("⏭ Next")
with c3:
    auto_btn = st.button("▶ Auto Animate")
with c4:
    stop_btn = st.button("⏸ Stop")

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

# Math
i = st.session_state.frame
end_val = (i * k) % N
cycles = gcd(N, k - 1)

# Layout
left, right = st.columns(2)

# Left: math explanation (student friendly)
with left:
    st.subheader("📐 Step-by-Step Calculation")

    st.write("**Given Parameters**")
    st.write(f"• Total Nodes (N) = {N}")
    st.write(f"• Multiplier (k) = {k}")
    st.write(f"• Current Index (i) = {i}")

    st.write("—" * 25)

    st.write("**Applying the Rule**")
    st.write("Rule: end = (i × k) mod N")
    st.write(f"end = ({i} × {k}) mod {N}")
    st.write(f"end = {end_val}")

    st.write("—" * 25)

    st.write("**Final Structure Insight**")
    st.write("Number of focal loops = gcd(N, k − 1)")
    st.write(f"gcd({N}, {k - 1}) = {cycles}")


# Right: animation
with right:
    angles = np.linspace(0, 2*np.pi, N, endpoint=False)
    x = np.cos(angles)
    y = np.sin(angles)

    fig, ax = plt.subplots(figsize=(4.5, 4.5))
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)

    ax.scatter(x, y, s=20, color="cyan")

    if show_numbers:
        for idx in range(N):
            ax.text(x[idx]*1.07, y[idx]*1.07, str(idx),
                    color="white", fontsize=6, ha="center", va="center")

    for j in range(i):
        ax.plot([x[j], x[(j*k) % N]],
                [y[j], y[(j*k) % N]],
                color="#e91e63", linewidth=0.7)

    ax.plot([x[i], x[end_val]], [y[i], y[end_val]],
            color="yellow", linewidth=2)

    ax.scatter(x[i], y[i], s=70, color="lime")
    ax.scatter(x[end_val], y[end_val], s=70, color="red")

    st.pyplot(fig, use_container_width=True)

# Auto animation (Streamlit-safe)
if st.session_state.auto_play:
    if st.session_state.frame < N - 1:
        time.sleep(interval / 1000)
        st.session_state.frame += 1
        st.rerun()
    else:
        st.session_state.auto_play = False


