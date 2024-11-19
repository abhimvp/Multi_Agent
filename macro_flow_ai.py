# Note: Replace **<YOUR_APPLICATION_TOKEN>** with your actual Application token
from langflow.load import run_flow_from_json
from dotenv import load_dotenv
import os
from typing import Optional
import requests
import json

# Load environment variables from .env file
load_dotenv()
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "6945a660-e525-49db-ab71-5c48bb87ff6b"
APPLICATION_TOKEN = os.getenv(
    "APPLICATION_TOKEN"
)  # get it from the flows API pop windown -> generate token
# print(APPLICATION_TOKEN)
LANGFLOW_ID_ASK_AI = "6945a660-e525-49db-ab71-5c48bb87ff6b"
APPLICATION_TOKEN_ASK_AI = os.getenv("APPLICATION_TOKEN_ASK_AI")


def dict_to_string(obj, level=0):
    strings = []
    indent = "  " * level  # Indentation for nested levels

    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                nested_string = dict_to_string(value, level + 1)
                strings.append(f"{indent}{key}: {nested_string}")
            else:
                strings.append(f"{indent}{key}: {value}")
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            nested_string = dict_to_string(item, level + 1)
            strings.append(f"{indent}Item {idx + 1}: {nested_string}")
    else:
        strings.append(f"{indent}{obj}")

    return ", ".join(strings)


# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
def get_macros(profile, goals):
    TWEAKS = {
        "TextInput-phuqp": {
            "input_value": ", ".join(
                goals
            )  # goals converted to a string rather than a python list
        },
        "TextInput-P2MWN": {"input_value": dict_to_string(profile)},
    }
    return run_flow("", tweaks=TWEAKS, application_token=APPLICATION_TOKEN)


def ask_ai(profile, question):
    TWEAKS = {
        "TextInput-25WFJ": {"input_value": question},
        "TextInput-b36kr": {"input_value": dict_to_string(profile)},
    }

    return run_flow_ask_ai(
        "", tweaks=TWEAKS, application_token=APPLICATION_TOKEN_ASK_AI
    )


def run_flow_ask_ai(
    message: str,
    output_type: str = "chat",
    input_type: str = "chat",
    tweaks: Optional[dict] = None,
    application_token: Optional[str] = None,
) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    print("ENtered into ask_ai function call")
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID_ASK_AI}/api/v1/run/ask-ai-v1"

    print(api_url)
    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {
            "Authorization": "Bearer " + application_token,
            "Content-Type": "application/json",
        }
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        print(response)
        return response.json()
    except Exception as e:
        print(e)


def run_flow(
    message: str,
    output_type: str = "chat",
    input_type: str = "chat",
    tweaks: Optional[dict] = None,
    application_token: Optional[str] = None,
) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/macros"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {
            "Authorization": "Bearer " + application_token,
            "Content-Type": "application/json",
        }
    response = requests.post(api_url, json=payload, headers=headers)
    return json.loads(
        response.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]
    )  # convert the string to python dictionary


result = get_macros(
    "name: Abhishek , age:26,weight:129kg,183cm", "I want to lose weight"
)
print(result)
