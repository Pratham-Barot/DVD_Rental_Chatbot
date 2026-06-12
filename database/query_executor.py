from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()


def execute_sql(sql_query):

    try:

        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        cursor = conn.cursor()

        cursor.execute(
            sql_query
        )

        data = cursor.fetchall()

        conn.close()

        return {
            "success": True,
            "data": data
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }