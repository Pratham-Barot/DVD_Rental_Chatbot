from ai.sql_generator import generate_sql
from database.query_executor import execute_sql
from ai.llm import get_response

from guardrails.sql_validator import validate_sql

from langsmith import traceable


@traceable(name="Generate SQL")
def traced_generate_sql(question):
    return generate_sql(question)


@traceable(name="Validate SQL")
def traced_validate_sql(sql_query):
    return validate_sql(sql_query)


@traceable(name="Execute SQL")
def traced_execute_sql(sql_query):
    return execute_sql(sql_query)


@traceable(name="Generate Answer")
def traced_generate_answer(
    question,
    sql_query,
    result
):

    prompt = f"""
    User Question:
    {question}

    SQL Query:
    {sql_query}

    Database Result:
    {result}

    Explain the database result in simple and readable language.

    Do not explain SQL.
    """

    return get_response(
        prompt,
        []
    )


@traceable(name="Database Assistant")
def ask_database(question):

    try:

        sql_query = traced_generate_sql(
            question
        )

        validated_sql = traced_validate_sql(
            sql_query
        )

        result = traced_execute_sql(
            validated_sql
        )

        answer = traced_generate_answer(
            question,
            validated_sql,
            result
        )

        return answer

    except Exception as e:

        print(f"Error: {e}")

        return (
            "I could not process your request safely."
        )