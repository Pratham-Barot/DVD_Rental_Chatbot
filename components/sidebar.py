import streamlit as st


def render_sidebar():

    with st.sidebar:

        st.title(
            "AI Database Assistant"
        )

        st.markdown(
            """
            Ask questions about:

            - Database tables
            - SQL queries
            - Machine Learning
            - General concepts
            """
        )

        if st.button(
            "Clear Chat"
        ):

            st.session_state.messages = []

            st.session_state.thread_id = "user_1"

            st.rerun()