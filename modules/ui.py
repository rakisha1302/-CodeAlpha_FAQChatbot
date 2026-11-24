
"""Reusable UI helpers for NovaDesk AI."""
import html
from pathlib import Path

import streamlit as st

TYPING = """
<div class="row">
    <div class="avatar bot-avatar">N</div>
    <div class="bubble bot typing">
        <span></span><span></span><span></span>
    </div>
</div>
"""


def load_css(path):
    try:
        css = Path(path).read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except OSError:
        st.warning("Style file missing. Using the default theme.")


def _fmt(value) -> str:
    return html.escape(str(value)).replace("\n", "<br>")


def hero(title, subtitle):
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-eyebrow">
                <span class="hero-dot"></span>
                NOVADESK AI WORKSPACE
            </div>
            <h1>{_fmt(title)}</h1>
            <p>{_fmt(subtitle)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def bubble(msg):
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div class="row user">
                <div class="bubble user">{_fmt(msg["text"])}</div>
                <div class="avatar user-avatar">Y</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    chips = ""

    if msg.get("category"):
        chips += (
            f'<span class="chip">📂 {_fmt(msg["category"])}</span>'
            f'<span class="chip score-chip">'
            f'🎯 Match {msg.get("score", 0) * 100:.0f}%</span>'
        )
    elif msg.get("miss"):
        chips += '<span class="chip warn">⚠️ No confident match</span>'

    st.markdown(
        f"""
        <div class="row">
            <div class="avatar bot-avatar">N</div>
            <div class="bubble bot">
                <div class="bot-name">Nova Assistant</div>
                <div class="message-text">{_fmt(msg["text"])}</div>
                <div class="chips">{chips}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric(label, value, icon, hint=""):
    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-top">
                <div class="icon">{icon}</div>
                <div class="metric-indicator"></div>
            </div>
            <div class="value">{_fmt(value)}</div>
            <div class="label">{_fmt(label)}</div>
            <div class="hint">{_fmt(hint)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
