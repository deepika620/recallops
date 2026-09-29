import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

BANK_ID = "recallops"


def get_client():
    # New client per call so each Streamlit rerun gets its own session
    return Hindsight(
        base_url="https://api.hindsight.vectorize.io",
        api_key=os.getenv("HINDSIGHT_API_KEY"),
    )


def setup_memory():
    get_client().create_bank(
        bank_id=BANK_ID,
        name="RecallOps",
        mission=(
            "Remember production incidents, root causes, attempted fixes, "
            "successful resolutions, failed approaches, and lessons learned "
            "so future incidents can be handled more effectively."
        ),
    )


def remember(incident):
    get_client().retain(
        bank_id=BANK_ID,
        content=incident,
        context="Production incident and resolution",
    )


def recall(query):
    return get_client().recall(
        bank_id=BANK_ID,
        query=query,
        max_tokens=4096,
        budget="mid",
    )
def reflect(query):
    return get_client().reflect(bank_id=BANK_ID, query=query)