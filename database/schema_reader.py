from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def get_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)

    tables = [row[0] for row in cursor.fetchall()]

    conn.close()

    return tables


def get_columns(table_name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = %s
        ORDER BY ordinal_position;
    """, (table_name,))

    columns = [row[0] for row in cursor.fetchall()]

    conn.close()

    return columns


def get_database_schema():

    schema_text = ""

    tables = get_tables()

    for table in tables:

        columns = get_columns(table)

        schema_text += f"\n{table}(\n"

        for column in columns:
            schema_text += f"    {column},\n"

        schema_text += ")\n"

    return schema_text