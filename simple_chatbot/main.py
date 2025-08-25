import chainlit as cl
import os
from  dotenv import load_dotenv
from typing import cast
from agents import Agent,OpenAIChatCompletionsModel, Runner, AsyncOpenAI
from agents.run import RunConfig

# Load the environment variables from the .env file
load_dotenv()
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("BASE_URL")
model = os.getenv("MODEL_NAME")

if not openrouter_api_key:
    raise ValueError("YOUR OPENROUTER_API_KEY IS NOT VALID PLEASE CHEAK YOUR .env FILE!")

@cl.on_chat_start
async def start():
    
   external_client = AsyncOpenAI(
      api_key = openrouter_api_key,
      base_url = model
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

   # Set up the chat session when a user connects.

   # Initialize an empty chat history in the session.

   cl.user_session.set("chat_history", [])
   cl.user_session.set("config",config)

   agent = Agent(
      name = "Assistant",
      instructions = "Your Are Helpful assistant",
      model=model
   )

   cl.user_session.set("agent",agent)
   await cl.Message(
      content="Welcome to the Panaversity AI Assistant! How can I help you today?"
   ).send()

   @cl.on_message
   async def main(message:cl.Message):
      msg = cl.Message(content="Thinking...")
      await msg.send()
  
      agent: Agent = cast(Agent, cl.user_session.get("agent"))
      config: RunConfig = cast(RunConfig, cl.user_session.get("config"))
      history = cl.user_session.get("chat_history") or []
      history.append({"role": "user", "content": message.content})

      try:
         print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
         Result = Runner.run_sync(
            starting_agent= agent,
            input= history,
            run_config= config
         )

         response_content = Result.final_output
         msg.content = response_content
         await msg.update()

         cl.user_session.set("chat_history", Result.to_input_list())
         print(f"User: {message.content}")
         print(f"Assistant: {response_content}")

      except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")





