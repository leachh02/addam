import ollama
import requests
import json
import os
import subprocess
import time

# Config
OLLAMA_URL = "http://localhost:11434/api"
MODEL_NAME = "deepseek-r1:8b" #"llama3"
MEMORY_FILE = "addam_memory.json"

# Load or create memory
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_memory(memory):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=4)

# Start Ollama server automatically
def start_ollama_server():
    print("Attempting to start Ollama server...")
    subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(5)  # Wait for server to boot

# Check if Ollama server is running
def check_ollama_running():
    try:
        response = requests.get(f"{OLLAMA_URL}/tags")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False

# Check if model is available
def check_model_loaded():
    try:
        response = requests.get(f"{OLLAMA_URL}/tags")
        response.raise_for_status()
        models = response.json().get("models", [])
        return any(model["name"] == MODEL_NAME for model in models)
    except requests.exceptions.RequestException:
        return False
    
# Chat with Ollama
def ask_addam(prompt, memory_context, verbose_thinking=True):

    if MODEL_NAME == "deepseek-r1:8b":
        messages = [
            {"role": "user", "content": f"You are ADDAM (Accurate Data Driven Artificial Mind), my personal AI assistant. Answer this prompt: {prompt}. Use this memory context: {memory_context}"},
        ]
    else:
        messages = [
            {"role": "system", "content": f"You are ADDAM, Harry's personal AI assistant. Use this memory context: {memory_context}"},
            {"role": "user", "content": f"{prompt}"},
        ]

    thinking_section = False
    speak_your_truth = False
    print("ADDAM: ", end='', flush=True)

    for part in ollama.chat(model=MODEL_NAME, messages=messages, stream=True):
        content = part['message']['content']

        if "<think>" in content:
            thinking_section = True
            if not verbose_thinking and not speak_your_truth:
                print("Thinking...")
                speak_your_truth = True
            continue

        if "</think>" in content:
            thinking_section = False
            continue

        if verbose_thinking or not thinking_section:
            print(content, end='', flush=True)
    print()

# Main loop
def main():
    print(f"ADDAM is starting up with {MODEL_NAME}...")

    if not check_ollama_running():
        start_ollama_server()

    while not check_ollama_running():
        print("Ollama server not detected. Please ensure it is running.")
        input("Press Enter once it's running...")

    while not check_model_loaded():
        print(f"The model '{MODEL_NAME}' is not loaded. Please run `ollama run {MODEL_NAME}`.")
        input("Press Enter once the model is running...")

    print("ADDAM is online. Type 'exit' to quit.")
    memory = load_memory()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'shutdown', 'goodbye']:
            print("Shutting down ADDAM.")
            break

        memory_context = json.dumps(memory)

        try:
            ask_addam(user_input, memory_context)

            if "remember that" in user_input.lower():
                try:
                    after_remember = user_input.lower().split("remember that", 1)[1].strip()
                    if " is " in after_remember:
                        key, value = after_remember.split(" is ", 1)
                        memory[key.strip()] = value.strip()
                        save_memory(memory)
                        print(f"Memory updated: {key.strip()} -> {value.strip()}")
                except Exception as e:
                    print("Could not parse memory instruction.")

        except Exception as e:
            print(f"Error communicating with Ollama: {e}")

if __name__ == "__main__":
    main()
