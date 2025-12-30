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
    layout="wide"
)

# ==========================
# SESSION STATE
# ==========================
if "frame" not in st.session_state:
    st.session_state.frame = 0

if "auto_play" not in st.session_state:
    st.session_state.auto_play = False

# ==========================
# SIDEBAR PARAMETERS
# ==========================
st.sidebar.header("Parameters")

N = st.sidebar.slider("Total Nodes (N)", 20, 120, 72)
k = st.sidebar.slider("Multiplier (k)", 2, 50, 9)
interval = st.sidebar.slider("Auto Animation Interval (ms)", 50, 500, 250)
show_numbers = st.sidebar.checkbox("Show Node Numbers", True)

# Clamp frame safely
st.session_state.frame = min(st.session_state.frame, N - 1)

# ==========================
# TOP TITLE
# ==========================
st.title("🧵 Thread Art – Modular Multiplication")
st.markdown("**Rule:** `end = (i × k) mod N`")

# ==========================
# CONTROL BUTTONS
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

# Button logic
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
i = st.session_state.frame
end_val = (i * k) % N
cycles = gcd(N, k - 1)

# ==========================
# TWO COLUMN LAYOUT
# ==========================
left_col, right_col = st.columns([1, 1])

# --------------------------
# LEFT: CALCULATION PANEL
# --------------------------
with left_col:
    st.subheader("📐 Calculation")

    st.markdown(
        f"""
**Rule**
