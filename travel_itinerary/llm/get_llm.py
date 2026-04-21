from langchain_openrouter import ChatOpenRouter
from langchain_ollama import ChatOllama

local_llm = ChatOllama(model="llama3.2:1b")
openrouter_llm = ChatOpenRouter(model="openai/gpt-oss-120b:free")
