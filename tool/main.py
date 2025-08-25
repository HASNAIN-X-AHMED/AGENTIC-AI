import os
from agents import OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
from openai import AsyncOpenAI


load_dotenv()
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("BASE_URL")
model = os.getenv("MODEL_NAME")

if not openrouter_api_key:
    raise ValueError("YOUR OPENROUTER_API_KEY IS NOT VALID PLEASE CHEAK YOUR .env FILE!")
    
external_client = AsyncOpenAI(
      api_key = openrouter_api_key,
      base_url = base_url
   )

model = OpenAIChatCompletionsModel(
      model = model,
      openai_client = external_client
   )

config = RunConfig(
      model=model,
      model_provider = external_client,
      tracing_disabled= True 
   )