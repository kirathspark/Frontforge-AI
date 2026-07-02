from langchain_ollama import ChatOllama

llm = ChatOllama(model="qwen3:4b", temperature=0.3)
response = llm.invoke("Say 'connection successful' and nothing else.")
print(response.content)

