from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Warning: GOOGLE_API_KEY is not set in the environment variables.")
    exit(1)

print(f"API Key found")

try:
    from langchain_google_genai import ChatGoogleGenerativeAI

    llm = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        temperature=0.7,
        api_key=api_key
    )

    response = llm.invoke("Say 'Hello from 2Giants CLI!' in a friendly way.")
    print(f"\nAI Response:\n{response.text}\n")
    print("Gemini LLM integration test passed successfully.")

except Exception as e:
    print(f"Error during Gemini LLM integration test: {e}")
    exit(1)