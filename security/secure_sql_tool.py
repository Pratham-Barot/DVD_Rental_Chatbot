from guardrails.sql_validator import (
    validate_sql
)

from database.query_executor import (
    execute_sql
)


def secure_execute_sql(sql_query):

    try:

        validated_sql = validate_sql(
            sql_query
        )

        result = execute_sql(
            validated_sql
        )

        return result

    except Exception as e:

        raise ValueError(
            f"Security Error: {e}"
        )