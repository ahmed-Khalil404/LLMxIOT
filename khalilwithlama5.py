import requests
import json
import gradio as gr
import threading
import time  # Import the time module

url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type': 'application/json',
}

conversation_history = []

def generate_response(prompt):
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

        # Print each character with a delay
        for char in actual_response:
            print(char, end='', flush=True)
            time.sleep(0.05)  # Adjust the delay as needed
        print()  # Move to a new line after the message
        
        return actual_response
    else:
        error_message = "Error: " + str(response.status_code) + " " + response.text
        print(error_message)
        return error_message

def run_gradio():
    iface = gr.Interface(
        fn=generate_response,
        inputs=gr.Textbox(lines=2, placeholder="Enter your prompt here..."), 
        outputs="text"
    )
    iface.launch()

thread = threading.Thread(target=run_gradio)
thread.start()

while True:
    user_input = input("Enter your command: ")
    if user_input.lower() == "exit":  
        break
    generate_response(user_input)
