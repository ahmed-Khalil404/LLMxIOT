import requests
import json
import gradio as gr
import threading
import time
import re 

url = "http://localhost:11434/api/generate"
command_url = "http://localhost:1880/output" 
headers = {'Content-Type': 'application/json'}
conversation_history = []

def generate_response(prompt, print_response=True):
    conversation_history.append(prompt)
    full_prompt = "\n".join(conversation_history)

    data = {
        "model": "modelkhalilx13:latest",
        "stream": False,
        "prompt": full_prompt,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["response"]
        conversation_history.append(actual_response)

        # Extract commands enclosed in braces
        commands = re.findall(r'\{(.*?)\}', actual_response)
        if commands:
            command_data = json.dumps({"commands": commands})
            requests.post(command_url, headers=headers, data=command_data)

        # Print response
        if print_response:
            print(actual_response)
        
        return actual_response
    else:
        error_message = "Error: " + str(response.status_code) + " " + response.text
        if print_response:
            print(error_message)
        return error_message

def run_gradio():
    iface = gr.Interface(
        fn=lambda prompt: generate_response(prompt, print_response=False),
        inputs=gr.Textbox(lines=2, placeholder="Enter your prompt here..."), 
        outputs="text"
    )
    iface.launch()

thread = threading.Thread(target=run_gradio)
thread.daemon = True
thread.start()

while True:
    user_input = input("Enter your command: ")
    if user_input.lower() == "exit":  
        break
    generate_response(user_input)
