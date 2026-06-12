from dotenv import load_dotenv
import os

from google import genai

from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_exponential

from ai.prompts import SYSTEM_PROMPT

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(
        multiplier=1,
        min=2,
        max=10
    ),
    reraise=True
)
def get_response(user_prompt, chat_history):

    conversation = ""

    for msg in chat_history:

        conversation += (
            f"{msg['role']} : {msg['content']}\n"
        )

    full_prompt = f"""
    {SYSTEM_PROMPT}

    Previous Conversation:

    {conversation}

    IMPORTANT INSTRUCTIONS:

    - Use the previous conversation history when answering.
    - If the user asks follow-up questions using words like:
    it, this, that, they, them, those, example, explain more
    then resolve the reference from the conversation history.
    - Do not ask the user to repeat information if it exists in the conversation history.
    - Treat the conversation as continuous.

    Current User Question:

    {user_prompt}
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=full_prompt
    )

    return response.text