from langflow.load import run_flow_from_json
from dotenv import load_dotenv
import uuid  # Add this import

load_dotenv()
# Generate a unique session ID
session_id = str(uuid.uuid4())

TWEAKS = {
    "TextInput-b36kr": {
        "input_value": "75kg , male , 175 cm , very active , work out a lot"
    },
    "TextInput-25WFJ": {"input_value": "what is the best back routine for me"},
}

try:
    result = run_flow_from_json(
        flow="AskAI.json",
        input_value="message",
        env_file=".env",
        session_id=session_id,
        fallback_to_env_vars=True,
        tweaks=TWEAKS,
    )
    print(result)
except Exception as e:
    print(f"Error occurred: {str(e)}")
