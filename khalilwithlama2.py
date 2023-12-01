import requests
import json

def send_request(prompt, history):
    # Combine the history with the new prompt
    full_prompt = history + "\n" + prompt
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "modelkhalil:latest",
        "prompt": full_prompt
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=headers, stream=True)
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return None

    response_text = ""
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            json_data = json.loads(decoded_line)
            print(json_data["response"], end='', flush=True)
            response_text += json_data["response"]
            if json_data["done"]:
                break

    return response_text

if __name__ == "__main__":
    history = ""
    while True:
        prompt = input("Enter your prompt: ")
        response = send_request(prompt, history)
        if response:
            history += "\n" + prompt + "\n" + response
            print("\n")
