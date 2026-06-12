from dotenv import load_dotenv
import os

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings
)

from langchain_chroma import Chroma

from rag.schema_documents import (
    get_schema_documents
)

load_dotenv()


def create_vector_store():

    documents = get_schema_documents()

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-2",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    vector_store = Chroma.from_texts(
        texts=documents,
        embedding=embeddings,
        persist_directory="chroma_db"
    )

    return vector_store