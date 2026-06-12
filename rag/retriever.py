from dotenv import load_dotenv
import os

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings
)

from langchain_chroma import Chroma

load_dotenv()


def get_relevant_schema(
    question,
    k=3
):

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-2",
        google_api_key=os.getenv(
            "GEMINI_API_KEY"
        )
    )

    vector_store = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    results = vector_store.similarity_search(
        question,
        k=k
    )

    return results