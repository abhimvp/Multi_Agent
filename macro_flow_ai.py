# Note: Replace **<YOUR_APPLICATION_TOKEN>** with your actual Application token
from dotenv import load_dotenv
import os
from typing import Optional
import requests

# Load environment variables from .env file
load_dotenv()
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "6945a660-e525-49db-ab71-5c48bb87ff6b"
APPLICATION_TOKEN = os.getenv("APPLICATION_TOKEN") # get it from the flows API pop windown -> generate token
# print(APPLICATION_TOKEN)

# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
def get_macros(profile,goals):
    TWEAKS = {
    "TextInput-phuqp": {
        "input_value": goals
    },
    "TextInput-P2MWN": {
        "input_value": profile
    }
    }
    return run_flow("",tweaks=TWEAKS,application_token=APPLICATION_TOKEN)

def run_flow(message: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  application_token: Optional[str] = None) -> dict:
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
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]

result = get_macros("name: Abhishek , age:26,weight:129kg,183cm", "I want to lose weight")
print(result)