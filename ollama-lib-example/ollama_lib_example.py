import ollama

response = ollama.list()

print("Available models:")
# Print the list of models
for model in response.models:
    print(model['model'])

response = ollama.chat(
    model="llama3.2",
    messages=[
        {"role": "user", "content": "Tell me a short story about a cat."}
    ],
)
print("Chat response:", response["message"]["content"])

response = ollama.chat(
    model="llama3.2",
    messages=[
        {"role": "user", "content": "Why ocean is salty?"}
    ],
    stream=True,
)

for chunk in response:
    print(chunk["message"]["content"], end="", flush=True)
