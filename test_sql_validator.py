from guardrails.sql_validator import (
    validate_sql
)

queries = [
    "SELECT email FROM staff;",
    "SELECT password FROM staff;",
    "SELECT first_name FROM actor;"
]

for query in queries:

    print("\n" + "=" * 50)
    print(query)
    print("=" * 50)

    try:

        result = validate_sql(
            query
        )

        print(
            "PASSED:",
            result
        )

    except Exception as e:

        print(
            "BLOCKED:",
            e
        )