import sqlglot
from sqlglot import exp

from guardrails.config import (
    ALLOWED_TABLES,
    DEFAULT_LIMIT
)

from guardrails.sensitive_columns import (
    BLOCKED_COLUMNS
)


ALLOWED_QUERY_TYPES = (
    exp.Select,
)


def validate_sql(sql_query):

    try:

        parsed_query = sqlglot.parse_one(
            sql_query,
            dialect="postgres"
        )

    except Exception as e:

        raise ValueError(
            f"Invalid SQL: {e}"
        )

    # Allow only SELECT

    if not isinstance(
        parsed_query,
        ALLOWED_QUERY_TYPES
    ):

        raise ValueError(
            f"Blocked Query Type: {type(parsed_query).__name__}"
        )

    # Table Whitelist

    tables = {
        table.name.lower()
        for table in parsed_query.find_all(exp.Table)
    }

    unauthorized_tables = (
        tables - ALLOWED_TABLES
    )

    # Block SELECT *

    if any(
        isinstance(node, exp.Star)
        for node in parsed_query.find_all(exp.Star)
    ):

        raise ValueError(
            "SELECT * is not allowed."
        )

    # ADD HERE 👇

    columns = {
        col.name.lower()
        for col in parsed_query.find_all(exp.Column)
    }

    blocked = columns & BLOCKED_COLUMNS

    if blocked:

        raise ValueError(
            f"Sensitive columns blocked: {blocked}"
        )

    # LIMIT Enforcement

    if not parsed_query.args.get("limit"):

        parsed_query.set(
            "limit",
            exp.Limit(
                expression=exp.Literal.number(
                    DEFAULT_LIMIT
                )
            )
        )

    return parsed_query.sql(
        dialect="postgres"
    )