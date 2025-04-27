import ollama

system = """
You are a very smart AI assistant who knows everything about Indian Army Regiments. You are very succinct and informative.
"""

ollama.create(model="indian_army", from_="llama3.2", system=system)
response = ollama.generate(model="indian_army", prompt="What is war cry of the mahar regiment?")
print("Generated Text:", response["response"])
      
ollama.delete(model="indian_army")
