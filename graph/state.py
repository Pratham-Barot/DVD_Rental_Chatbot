from typing import TypedDict


class GraphState(TypedDict):

    question: str

    route: str

    schema: str

    sql_query: str

    sql_result: str

    visualization_data: list

    sql_error: str

    retry_count: int

    answer: str

    messages: list