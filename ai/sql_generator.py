from ai.llm import get_response


def generate_sql(
    question,
    schema,
    messages
):

    prompt = f"""
    You are a PostgreSQL expert.

    Database Schema:

    {schema}

    Rules:
    - Return ONLY SQL.
    - Do not explain anything.
    - Do not use markdown.
    - Use PostgreSQL syntax.

    Question:
    {question}
    """

    sql_query = get_response(
        prompt,
        messages
    )

    return sql_query.strip()