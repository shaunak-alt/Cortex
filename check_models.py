import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

print("--- Checking available Google AI Models ---")

try:
    # Configure the API key
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    print("Successfully configured API key. Fetching models...\n")

    # List all available models
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model found: {m.name}")

    print("\n--- Check complete ---")
    print("Please copy the best available model name (e.g., 'models/gemini-pro') and we will use that one.")

except Exception as e:
    print(f"\nAn error occurred: {e}")
    print("Please double-check that your GOOGLE_API_KEY in the .env file is correct and has been enabled for the Generative AI API.")