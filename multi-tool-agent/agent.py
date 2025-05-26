import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

def get_weather(city: str) -> dict:
  """
  Args:
    city (str): The name of the city for which to retrieve the weather.

  Returns:
    dict: status and result or error message
  """

  if city.lower() == "kansas city":
    return {
      "status": "success",
      "report": (
      "The weather in Kansas City is currently sunny with a temperature of 75°F, humidity of 60%, wind speed of 10 mph, and wind direction of NW."
        )
    }
  else:
    return {
      "status": "error",
      "message": f"Weather data for {city} is not available."
    }

def get_current_time(city: str) -> dict:
  """
  Args:
    city (str): The name of the city for which to retrieve the current time.

  Returns:
    dict: status and result or error message
  """

  if city.lower() == "kansas city":
    tz_identifier = "America/Chicago"
    return {
      "status": "success",
      "time": datetime.datetime.now(ZoneInfo(tz_identifier)).strftime("%Y-%m-%d %H:%M:%S")
    }
  else:
    return {
      "status": "error",
      "message": f"Time data for {city} is not available."
    }

root_agent = Agent(
  name="weather_time_agent",
  description="Agent that provides weather and time information for Kansas City.",
  model="gemini-2.5-flash-preview-05-20",
  instruction="You are an AI assistant that provides weather and time information",
  tools=[get_weather, get_current_time]
)
