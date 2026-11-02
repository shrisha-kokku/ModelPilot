from langchain_groq import ChatGroq
from agent.config import GROQ_API_KEY, MODEL_NAME


def get_llm() -> ChatGroq:
    return ChatGroq(groq_api_key=GROQ_API_KEY, model=MODEL_NAME, temperature=0)