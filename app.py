import streamlit as st

from pages.chat import render_chat
from components.sidebar import render_sidebar

st.set_page_config(
    page_title="AI Database Assistant",
    page_icon="🤖",
    layout="wide"
)

render_sidebar()

render_chat()