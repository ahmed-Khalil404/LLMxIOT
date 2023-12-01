import requests
import json

def send_request(prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "modelkhalil:latest",
        "prompt": prompt
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=headers, stream=True)

    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            json_data = json.loads(decoded_line)
            print(json_data["response"], end='', flush=True)  # Print each part of the response as it arrives
            if json_data["done"]:
                break

if __name__ == "__main__":
    while True:  # Infinite loop for continuous prompting
        prompt = input("Enter your prompt: ")
        send_request(prompt)
        print("\n")  # Print a newline for better readability
