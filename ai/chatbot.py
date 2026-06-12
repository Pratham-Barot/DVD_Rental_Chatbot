from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)

from ai.langchain_llm import llm
from ai.prompts import SYSTEM_PROMPT


def get_response(user_prompt, chat_history):

    messages = []

    # System Prompt
    messages.append(
        SystemMessage(
            content=SYSTEM_PROMPT
        )
    )

    # Previous Conversation
    for msg in chat_history:

        if msg["role"] == "user":

            messages.append(
                HumanMessage(
                    content=msg["content"]
                )
            )

        elif msg["role"] == "assistant":

            messages.append(
                AIMessage(
                    content=msg["content"]
                )
            )

    # Current User Message
    messages.append(
        HumanMessage(
            content=user_prompt
        )
    )

    response = llm.invoke(messages)

    return response.content