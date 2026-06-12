from dotenv import load_dotenv
import os 

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    google_api_key = os.getenv("GEMINI_API_KEY")
)