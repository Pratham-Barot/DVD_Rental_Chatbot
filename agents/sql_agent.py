from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_community.utilities import SQLDatabase

from langchain_community.agent_toolkits import (
    SQLDatabaseToolkit
)

from langchain_community.agent_toolkits import (
    create_sql_agent
)

load_dotenv()


DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)


llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    google_api_key=os.getenv(
        "GEMINI_API_KEY"
    ),
    temperature=0
)


db = SQLDatabase.from_uri(
    DATABASE_URL
)


toolkit = SQLDatabaseToolkit(
    db=db,
    llm=llm
)


agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True
)


def ask_sql_agent(question):

    response = agent.invoke(
        {"input": question}
    )

    return response["output"]