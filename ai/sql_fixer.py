from ai.llm import get_response


def fix_sql(
    question,
    schema,
    failed_sql,
    error_message
):

    prompt = f"""
    You are a PostgreSQL expert.

    Database Schema:

    {schema}

    User Question:

    {question}

    Failed SQL:

    {failed_sql}

    PostgreSQL Error:

    {error_message}

    Fix the SQL query.

    Rules:
    - Return ONLY SQL.
    - Do not explain anything.
    - Do not use markdown.
    - Use PostgreSQL syntax.
    """

    fixed_sql = get_response(
        prompt,
        []
    )

    return fixed_sql.strip()