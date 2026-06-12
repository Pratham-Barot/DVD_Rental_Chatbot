from database.schema_reader import (
    get_tables,
    get_columns
)


def get_schema_documents():

    documents = []

    tables = get_tables()

    for table in tables:

        columns = get_columns(table)

        document = f"""
Table: {table}

Columns:
{", ".join(columns)}

Description:
This table stores information about {table}.
"""

        documents.append(document)

    return documents