from graph.workflow import app

from guardrails.input_guardrail import (
    validate_user_input
)


def ask_assistant(question):

    try:

        validate_user_input(
            question
        )

        result = app.invoke(
            {
                "question": question
            }
        )

        return result["answer"]

    except Exception as e:

        return str(e)