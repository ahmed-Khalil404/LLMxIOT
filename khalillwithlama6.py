import requests
import json
import time

url = "http://localhost:11434/api/generate"
command_url = "http://localhost:1880/output"
headers = {'Content-Type': 'application/json'}

conversation_history = []

def generate_response(prompt):
    conversation_history.append(prompt)
    full_prompt = "\n".join(conversation_history)

    try:
        data = {
            "model": "modelkhalilx9:latest",
            "stream": False,
            "prompt": full_prompt,
        }
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=60)

        if response.status_code == 200:
            response_text = response.text
            data = json.loads(response_text)
            actual_response = data["response"]
            conversation_history.append(actual_response)

            print(actual_response)

            command_data = json.dumps({"response": actual_response})
            node_red_response = requests.post(command_url, headers=headers, data=command_data, timeout=60)

            if node_red_response.status_code != 200:
                print("Node-RED server response error:", node_red_response.status_code)

        else:
            print("AI model server response error:", response.status_code)

    except Exception as e:
        print("An error occurred:", e)

while True:
    user_input = input("Enter your command: ")
    if user_input.lower() == "exit":
        break
    generate_response(user_input)