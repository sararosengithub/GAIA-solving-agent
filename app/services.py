from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from typing import Optional
from logging import getLogger


load_dotenv() 
log = getLogger(__name__)

_chat_llm: Optional[ChatOpenAI] = None
_routing_llm: Optional[ChatOpenAI] = None


def initalize_llms():
    global _chat_llm, _routing_llm
    if _chat_llm is None:
        try:
            _chat_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
            _routing_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0) # For classification
            print("LLM services initialized.")
        except Exception as e:
            print(f"CRITICAL: Failed to initialize LLMs: {e}. Check API keys and .env setup.")
            raise


def get_chat_llm() -> ChatOpenAI:
    if _chat_llm is None:
        raise RuntimeError("Chat LLM not initialized. Call initialize_llms() first.")
    return _chat_llm


def get_routing_llm() -> ChatOpenAI:
    if _routing_llm is None:
        raise RuntimeError("Routing LLM not initialized. Call initialize_llms() first.")
    return _routing_llm