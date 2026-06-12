def get_friendly_error(
    error_message
):

    error = error_message.lower()

    if "sensitive columns blocked" in error:

        return (
            "Access to sensitive information "
            "is restricted."
        )

    if "select * is not allowed" in error:

        return (
            "Selecting all columns is restricted. "
            "Please request specific information."
        )

    if "does not exist" in error:

        if "relation" in error:

            return (
                "I couldn't find the requested table "
                "in the database."
            )

        if "column" in error:

            return (
                "I couldn't find the requested column "
                "in the database."
            )

    if "syntax error" in error:

        return (
            "The generated SQL query contains "
            "a syntax error."
        )

    return (
        "The database query could not be executed."
    )