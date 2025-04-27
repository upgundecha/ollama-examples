import requests
import json

url = "http://localhost:11434/api/generate"

data = {
    "model": "llama3.2",
    "prompt": "Tell me a shorty story about a cat.",
}

response = requests.post(url, json=data, stream=True)
if response.status_code == 200:
    print("Generated Text:", end="", flush=True)
    for line in response.iter_lines():
        if line:
            # Decode the line and parse it as JSON
            decoded_line = line.decode('utf-8')
            result = json.loads(decoded_line)
            generated_text = result.get("response", "")
            print(generated_text, end="", flush=True)
else:
    print("Error: ",response.status_code, " ", response.text)
