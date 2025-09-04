import os
from langchain_openai import ChatOpenAI

def get_hackclub_ai():
    api_key = "none-thanks-to-hackclub"

    llm = ChatOpenAI(
        api_key=api_key,
        base_url="https://ai.hackclub.com",
        model="qwen/qwen3-32b",
        temperature=1.0
    )

    return llm
