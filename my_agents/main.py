from dotenv import load_dotenv
import os
from agents import Agent, AsyncOpenAI,Runner , OpenAIChatCompletionsModel,RunConfig

load_dotenv()
gemini_api_key=os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

faq_responses = {
    "what is your name?": "I am FAQBot, your helpful assistant.",
    "who created you?": "I was created using the OpenAI Agent SDK.",
    "what can you do?": "I can answer simple predefined FAQ questions.",
    "how are you?": "I'm just code, but I'm running smoothly!",
    "bye": "Goodbye! Have a great day!"
}


agent = Agent(
    name="FAQBot",
    instructions="You are a helpful FAQ bot. Only answer from the predefined FAQ list."
)


def handle_message(message: str):
    normalized = message.lower().strip()
    return faq_responses.get(normalized, "Sorry, I don’t know the answer to that.")


if __name__ == "__main__":
    print("FAQBot is running. Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        response = handle_message(user_input)
        print("Bot:", response)
        if user_input.lower().strip() == "bye":
            break