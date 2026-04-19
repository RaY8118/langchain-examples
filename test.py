from langchain_ollama import OllamaLLM
from langchain_openrouter import ChatOpenRouter
import httpx
client = httpx.Client(verify=False)
llm = OllamaLLM(
    model="llama3.2:1b",
    http_client=client
)

response = llm.invoke("Hi")

print(response)

llm = ChatOpenRouter(
    model="openai/gpt-oss-120b:free",
)

response = llm.invoke("Hi")

print(response)
