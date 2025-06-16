
# 1) Install Ollama (https://www.ollama.com/)

# 2) Install the Python client
# >> pip install ollama

# 3) Download models (stored the system's default Ollama directory:)
# (Linux: ~/.ollama) (Win: C:\Users\<YourUsername>\.ollama)
# >> ollama pull qwen3:0.6b 
# 
# Select optional different path
# >> set OLLAMA_MODELS=D:\OllamaModels (CMD)
# >> export OLLAMA_MODELS=/mnt/ssd/models (Linux)   

# Run ollama in CMD
# >> ollama run qwen3:0.6b
# >> ollama run deepseek-r1:1.5b
# >> ollama run llama3.2:1b
# >> ollama run falcon3:1b

##############################################################
# The chat assistance using "ollama.chat" method
##############################################################
import ollama
from ollama import chat

## Choose model
# model_name = 'qwen3:0.6b'
model_name = 'deepseek-r1:1.5b'
# model_name = 'llama3.2:1b'
# model_name = 'falcon3:1b'
# model_name = 'granite3.1-moe:1b'
# model_name = 'falcon3:1b'



print("Type your prompts (type 'exit' to quit):")
try:
    while True:
        prompt = input("[User:] > ")
        if prompt.lower() == 'exit':
            break
        response = response = ollama.chat(
            model=model_name,
            messages=[{'role': 'user', 'content': prompt}] # /no_think for no reasoning
        )
        print("[Assistant:] > ", response['message']['content'])
        print()  # New line after response

except KeyboardInterrupt:
    print("\nExiting chat.")


