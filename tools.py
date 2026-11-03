import requests
import json
from datetime import datetime
from zoneinfo import ZoneInfo
from Utilities.utilities import log

def get_current_time(timezone="Asia/Kolkata"):
    try:
        return datetime.now(ZoneInfo(timezone)).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return f"unknown timezone: {timezone}.use IANA name like Asia/tokyo."

def get_city_weather(city):
    url=f"https://wttr.in/{city}?format=3"
    resp=requests.get(url,timeout=10)
    #if resp has an error then it is raised checking the status
    resp.raise_for_status()
    return resp.text

def get_user_city():
    return "Jaipur"

Tools=[
    {
        "type":"function",
        "function":{
            "name": "get_current_time",
            "description":"Returns the current date and time as a formatted string",
            "parameters":{
                "type":"object",
                "properties":{
                    "timezone":{
                        "type":"string",
                        "description":"IANA timezone name, e.g. Asia/Tokyo, America/New_York, Asia/Kolkata"
                    }
                }
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"get_city_weather",
            "description":"Returns the name of the city alongwith the current temperature.",
            "parameters":{
                "type":"object",
                "properties":{
                    "city":{
                        "type":"string",
                        "description":"city to get the weather of"
                    }
                },
                "required":["city"]
            }
        }
    },
    {
            "type":"function",
            "function":{
                "name": "get_user_city",
                "description":"""MUST be called whenever the user asks about their
                    own city, current location, home city, or weather
                    in their city.

                    Returns the user's city. This function requires
                    no arguments. Never ask the user for their city
                    when this tool is available.""",
                "parameters":{"type":"object","properties":{}}
            }
        }
]

function_name_to_map={
    "get_current_time":get_current_time,
    "get_city_weather":get_city_weather,
    "get_user_city":get_user_city
}

def run_tool(tool_call):

    function_name=tool_call.function.name  
    func_args={} 
    try:
        func_args=json.loads(tool_call.function.arguments or "{}")
        log(f"  {function_name}({func_args})")
        fn=function_name_to_map[function_name]
        result=fn(**func_args)

    except Exception as e:
        result=f"error while running {function_name}:{e}"

    log(f"  {result}")
    return result