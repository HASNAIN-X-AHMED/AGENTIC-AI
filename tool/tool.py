from agents import Agent , Runner, function_tool
from main import config



@function_tool
def plus(n1,n2):
    print("Plus tool ")
    return f"your answer is {n1+n2}"

@function_tool
def subtract(n1,n2):
    print("Subtract tool")
    return f"your answer is {n1-n2}"

agent = Agent(
    name = "General Agent",
    instructions="You are helpful general agent . Your task is to help the user their queries",
    tools=[plus,subtract]
    
)

result = Runner.run_sync(
    agent,
    "67+7",
    run_config= config,

)

print(result.final_output)