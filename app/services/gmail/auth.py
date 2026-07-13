import json
import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify"
]

BASE_DIR = Path(__file__).resolve().parents[3]

TOKEN_FILE = BASE_DIR / "token.json"
CREDENTIALS_FILE = BASE_DIR / "credentials.json"


def authenticate():

    creds = None

    # ---------------------------------------------------
    # Production (Render)
    # ---------------------------------------------------

    is_render = os.getenv("RENDER") is not None

    if is_render:

        token_json = os.getenv("GOOGLE_TOKEN_JSON")
        credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")

        if token_json and credentials_json:

            creds = Credentials.from_authorized_user_info(
                json.loads(token_json),
                SCOPES,
            )

            if creds.expired and creds.refresh_token:
                creds.refresh(Request())

            return creds

        raise Exception(
            "GOOGLE_TOKEN_JSON or GOOGLE_CREDENTIALS_JSON not configured on Render."
        )

    # ---------------------------------------------------
    # Local Development
    # ---------------------------------------------------

    if TOKEN_FILE.exists():

        creds = Credentials.from_authorized_user_file(
            str(TOKEN_FILE),
            SCOPES,
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE),
                SCOPES,
            )

            creds = flow.run_local_server(
                port=0,
                authorization_prompt_message="",
                success_message=(
                    "Authentication successful. "
                    "You can close this window."
                ),
                open_browser=True,
            )

        with open(TOKEN_FILE, "w") as token:

            token.write(creds.to_json())

    return creds