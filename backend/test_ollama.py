from langchain_ollama import ChatOllama

# we needed to make sure your local model actually works.
llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

response = llm.invoke("Explain what a microservice is in one sentence.")

print(response.content)