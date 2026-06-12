from langgraph.checkpoint.memory import (
    MemorySaver
)

from langgraph.graph import (
    StateGraph,
    END
)

from graph.state import (
    GraphState
)

from graph.nodes import (
    router_node,
    chat_node,
    schema_chat_node,
    retrieve_schema_node,
    generate_sql_node,
    validate_sql_node,
    execute_sql_node,
    fix_sql_node,
    generate_answer_node
)

workflow = StateGraph(
    GraphState
)

workflow.add_node(
    "router",
    router_node
)

workflow.add_node(
    "chat",
    chat_node
)

workflow.add_node(
    "schema_chat",
    schema_chat_node
)

workflow.add_node(
    "retrieve_schema",
    retrieve_schema_node
)

workflow.add_node(
    "generate_sql",
    generate_sql_node
)

workflow.add_node(
    "validate_sql",
    validate_sql_node
)

workflow.add_node(
    "execute_sql",
    execute_sql_node
)

workflow.add_node(
    "fix_sql",
    fix_sql_node
)

workflow.add_node(
    "generate_answer",
    generate_answer_node
)

workflow.set_entry_point(
    "router"
)


def route_decision(state):

    if state["route"] == "SQL":
        return "retrieve_schema"

    if state["route"] == "SCHEMA":
        return "retrieve_schema"

    return "chat"


def validation_decision(state):

    if state.get(
        "sql_error",
        ""
    ):

        return "failed"

    return "valid"


def schema_decision(state):

    if state["route"] == "SCHEMA":
        return "schema_chat"

    return "generate_sql"


def sql_execution_decision(state):

    if state["sql_error"] == "":
        return "success"

    if state.get(
        "retry_count",
        0
    ) >= 1:
        return "failed"

    return "retry"


workflow.add_conditional_edges(
    "router",
    route_decision,
    {
        "retrieve_schema": "retrieve_schema",
        "chat": "chat"
    }
)

workflow.add_conditional_edges(
    "retrieve_schema",
    schema_decision,
    {
        "schema_chat": "schema_chat",
        "generate_sql": "generate_sql"
    }
)

workflow.add_edge(
    "generate_sql",
    "validate_sql"
)

workflow.add_conditional_edges(
    "validate_sql",
    validation_decision,
    {
        "valid": "execute_sql",
        "failed": "generate_answer"
    }
)

workflow.add_conditional_edges(
    "execute_sql",
    sql_execution_decision,
    {
        "success": "generate_answer",
        "retry": "fix_sql",
        "failed": "generate_answer"
    }
)

workflow.add_edge(
    "fix_sql",
    "validate_sql"
)

workflow.add_edge(
    "generate_answer",
    END
)

workflow.add_edge(
    "schema_chat",
    END
)

workflow.add_edge(
    "chat",
    END
)

memory = MemorySaver()

app = workflow.compile(
    checkpointer=memory
)