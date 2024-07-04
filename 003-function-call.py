from litellm import completion

messages = [{"role": "user", "content": "Como está o clima em Joinville? Em Fahrenheit"}]


def get_current_weather(location, unit="celsius"):
    temperature = 25
    if unit == "fahrenheit":
        temperature = temperature * 9 / 5 + 32
    
    if location == "Joinville, SC":
        return f"A temperatura atual é de {temperature} graus celsius."


functions = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
            "required": ["location"],
        },
    }
]


response = completion(model="gpt-4o", messages=messages, functions=functions)

print(response)
function_call_data = response.choices[0].message.function_call


import json

function_name = function_call_data.name
function_args = json.loads(function_call_data.arguments)


if function_name == "get_current_weather":
    result = get_current_weather(**function_args)
    print(result)
