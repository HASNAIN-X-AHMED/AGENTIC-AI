from agents import Agent , Runner, function_tool
from main import config
import os 
from dotenv import load_dotenv
import requests



load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")


@function_tool
def plus(n1,n2):
    print("Plus tool ")
    return f"your answer is {n1+n2}"

@function_tool
def get_weather(city : str) ->str:
    response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}")
    data = response.json()
    return f"The current weather in {city} is {data['current']['temp_c']} C with {data['current']['condition']['text']}. "


agent = Agent(
    name = "General Agent",
    instructions="You are helpful general agent . Your task is to help the user their queries",
    tools=[get_weather,plus]
    
)

result = Runner.run_sync(
    agent,
    input=input("Enter Your Question :"),
    run_config= config,

)

print(result.final_output)