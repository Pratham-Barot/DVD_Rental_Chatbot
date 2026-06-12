from rag.retriever import (
    get_relevant_schema
)

from ai.sql_generator import (
    generate_sql
)

from guardrails.sql_validator import (
    validate_sql
)

from database.query_executor import (
    execute_sql
)

from ai.sql_fixer import (
    fix_sql
)

from ai.llm import (
    get_response
)

from utils.error_handler import (
    get_friendly_error
)

def router_node(state):

    messages = state.get(
        "messages",
        []
    )

    prompt = f"""
    Classify the user question.

    Return ONLY one of:

    SQL
    CHAT
    SCHEMA

    SCHEMA:
    - Questions about tables
    - Questions about columns
    - Questions about database structure
    - Questions about schema

    SQL:
    - Questions requiring database data

    CHAT:
    - General conversation

    Question:
    {state["question"]}
    """

    route = get_response(
        prompt,
        messages
    ).strip().upper()

    state["route"] = route

    return state


def chat_node(state):

    messages = state.get(
        "messages",
        []
    )

    answer = get_response(
        state["question"],
        messages
    )

    state["answer"] = answer

    state["messages"] = [
    {
        "role": "user",
        "content": state["question"]
    },
    {
        "role": "assistant",
        "content": answer
    }
]

    return state


def retrieve_schema_node(state):

    schema_docs = get_relevant_schema(
        state["question"]
    )

    schema_text = "\n\n".join(
        doc.page_content
        for doc in schema_docs
    )

    state["schema"] = schema_text

    return state


def generate_sql_node(state):

    state["retry_count"] = 0

    state["sql_error"] = ""

    state["sql_result"] = []

    state["visualization_data"] = []

    sql_query = generate_sql(
        state["question"],
        state["schema"],
        state.get(
            "messages",
            []
        )
    )

    if sql_query == "SCHEMA_NOT_FOUND":

        state["sql_error"] = (
            "Requested information "
            "does not exist in schema"
        )

        state["answer"] = (
            "The requested information "
            "is not available in the database schema."
        )

        return state

    state["sql_query"] = sql_query

    return state


def validate_sql_node(state):

    try:

        validated_sql = validate_sql(
            state["sql_query"]
        )

        state["sql_query"] = validated_sql

        state["sql_error"] = ""

    except Exception as e:

        state["sql_error"] = str(e)

        state["sql_result"] = []

        state["visualization_data"] = []

        if not state["sql_query"].strip().upper().startswith(
            "SELECT"
        ):

            state["answer"] = state[
                "sql_query"
            ]

    return state

def execute_sql_node(state):

    result = execute_sql(
        state["sql_query"]
    )

    if result["success"]:

        state["sql_result"] = result[
            "data"
        ]

        state["visualization_data"] = result[
            "data"
        ]

        state["sql_error"] = ""

    else:

        state["sql_result"] = []

        state["visualization_data"] = []

        state["sql_error"] = result[
            "error"
        ]

    return state

def fix_sql_node(state):

    fixed_sql = fix_sql(
        question=state["question"],
        schema=state["schema"],
        failed_sql=state["sql_query"],
        error_message=state["sql_error"]
    )

    state["sql_query"] = fixed_sql

    state["retry_count"] = (
        state.get(
            "retry_count",
            0
        ) + 1
    )

    state["sql_error"] = ""

    return state


def generate_answer_node(state):

    messages = state.get(
        "messages",
        []
    )

    if state.get(
        "sql_error",
        ""
    ):

        if state.get(
            "answer",
            ""
        ):

            answer = state[
                "answer"
            ]

        else:

            answer = get_friendly_error(
                state["sql_error"]
            )

    else:

        if not state["sql_result"]:

            answer = (
                "No matching records were found."
            )

        else:

            prompt = f"""
            User Question:
            {state["question"]}

            SQL Query:
            {state["sql_query"]}

            Database Result:
            {str(state["sql_result"])}

            Explain the database result in simple and readable language.

            Do not explain SQL.
            """

            answer = get_response(
                prompt,
                messages
            )

    state["answer"] = answer

    state["messages"] = [
        {
            "role": "user",
            "content": state["question"]
        },
        {
            "role": "assistant",
            "content": answer
        }
    ]

    return state


def schema_chat_node(state):

    messages = state.get(
        "messages",
        []
    )

    prompt = f"""
    Database Schema:

    {state["schema"]}

    User Question:

    {state["question"]}

    Answer ONLY using the schema.

    If the answer is not present in the schema,
    say that the information is not available.
    """

    answer = get_response(
        prompt,
        messages
    )

    state["answer"] = answer

    state["messages"] = [
        {
            "role": "user",
            "content": state["question"]
        },
        {
            "role": "assistant",
            "content": answer
        }
    ]

    return state