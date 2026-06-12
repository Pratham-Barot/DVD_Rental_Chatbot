import uuid
import pandas as pd
import streamlit as st

from graph.workflow import app

from guardrails.input_guardrail import (
    validate_user_input
)

from guardrails.output_guardrail import (
    validate_output
)


def render_chat():

    if "messages" not in st.session_state:

        st.session_state.messages = []

    if "thread_id" not in st.session_state:

        st.session_state.thread_id = str(
            uuid.uuid4()
        )

    if len(
        st.session_state.messages
    ) == 0:

        st.info(
            "Ask a database or general question."
        )

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

    question = st.chat_input(
        "Ask a question..."
    )

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message(
            "user"
        ):

            st.markdown(
                question
            )

        try:

            validate_user_input(
                question
            )

            config = {
                "configurable": {
                    "thread_id":
                    st.session_state.thread_id
                }
            }

            with st.spinner(
                "Thinking..."
            ):

                result = app.invoke(
                    {
                        "question": question
                    },
                    config=config
                )

            answer = result[
                "answer"
            ]

            data = result.get(
                "visualization_data",
                []
            )

            validate_output(
                answer
            )

        except Exception as e:

            answer = (
                f"Error: {str(e)}"
            )

            data = []

        with st.chat_message(
            "assistant"
        ):

            st.markdown(
                answer
            )

            if data:

                try:

                    df = pd.DataFrame(
                        data
                    )

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                    if len(df.columns) == 2:

                        numeric_cols = df.select_dtypes(
                            include="number"
                        ).columns

                        if len(numeric_cols) == 1:

                            st.bar_chart(
                                df.set_index(
                                    df.columns[0]
                                )
                            )

                except Exception:

                    pass

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )