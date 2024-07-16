# src/llm_utils.py
import openai
from langchain_openai import ChatOpenAI

def initialize_llm(api_key):
    openai.api_key = api_key
    llm = ChatOpenAI(
        model="gpt-3.5-turbo-0125",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    return llm
