from dotenv import load_dotenv
from agents import (
Agent,
InputGuardrailTripwireTriggered,
OpenAIChatCompletionsModel,
RunContextWrapper,
GuardrailFunctionOutput,
Runner,
TResponseInputItem,
input_guardrail,
)
import chainlit as cl
from openai import AsyncOpenAI
from agents.run import RunConfig
import os
from pydantic import BaseModel

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
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

class OutputMath(BaseModel):
    is_math_homework : bool
    reasponse : str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking you to do their math homework. Respond with `is_math_homework` (true/false) and `reasoning`.",
    model=model,
    output_type=OutputMath,
)

@input_guardrail
async def math_guardrail(
    ctx:RunContextWrapper[None], agent: Agent, input: str | list [TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input , context=ctx.context, run_config= config)

    print(result.final_output)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered= not result.final_output.is_math_homework  # ✅ fixed logic
    )

agent = Agent(
    name="Math agent",
    instructions="You are math agent. You respond only math related question",
    model= model,
    input_guardrails=[math_guardrail]
)

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="I'm ready to assit you").send()


@cl.on_message
async def on_message(message : cl.Message):
  try:
        result = await Runner.run(
            agent,
            input=message.content   
        )
        await cl.Message(content=result.final_output).send()
    
  except InputGuardrailTripwireTriggered :
    await cl.Message(content="please try math related quetion").send()
