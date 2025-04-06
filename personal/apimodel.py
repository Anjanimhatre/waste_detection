import google.generativeai as genai

genai.configure(api_key="AIzaSyCC9Q07JTA-Kc0xCFZltYHQGrYsiSjDePk")  # Replace with your API key

# List available models
models = genai.list_models()
for model in models:
    print(model.name)
