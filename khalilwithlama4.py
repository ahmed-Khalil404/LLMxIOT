import requests
import json
import re
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
            "model": "modelkhalil",
            "stream": False,
            "prompt": full_prompt,
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            response_text = response.text
            data = json.loads(response_text)
            actual_response = data["response"]
            conversation_history.append(actual_response)

            commands = re.findall(r'\{(.*?)\}', actual_response)
            if commands:
                command_data = json.dumps({"commands": commands})
                requests.post(command_url, headers=headers, data=command_data)

            # Print each character with a delay
            for char in actual_response:
                print(char, end='', flush=True)
            print()

        else:
            print("Error:", response.status_code, response.text)
    except Exception as e:
        print("An error occurred:", e)

while True:
    user_input = input("Enter your command: ")
    if user_input.lower() == "exit":
        break
    generate_response(user_input)
