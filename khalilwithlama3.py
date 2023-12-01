import requests
import json

def send_request(prompt, history):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "modelkhalil:latest",
        "prompt": prompt,
        "history": history  # Include the conversation history in the request
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=headers, stream=True)
    full_response = ""

    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return None

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            json_data = json.loads(decoded_line)
            print(json_data["response"], end='', flush=True)
            full_response += json_data["response"]
            if json_data["done"]:
                break

    print("\n")
    return full_response

if __name__ == "__main__":
    history = []

    while True:
        prompt = input("Enter your prompt: ")
        response = send_request(prompt, history)
        if response is not None:
            history.append((prompt, response))
