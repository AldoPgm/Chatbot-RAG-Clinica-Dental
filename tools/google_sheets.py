"""
Tool: Google Sheets Integration
========================================
Read from and write to Google Sheets for storing deliverables and data.

Inputs:
    - spreadsheet_id (str): The Google Sheets spreadsheet ID
    - range_name (str): The A1 notation range (e.g., "Sheet1!A1:D10")
    - values (list[list]): Data to write (for write operations)

Outputs:
    - dict: { "success": bool, "data": list | None, "error": str | None }

Requirements:
    - credentials.json (Google OAuth) in project root
    - GOOGLE_CREDENTIALS_PATH in .env
"""

import os
from dotenv import load_dotenv

load_dotenv()


def read_sheet(spreadsheet_id: str, range_name: str) -> dict:
    """Read data from a Google Sheet."""
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        import pickle

        SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
        creds = _get_credentials(SCOPES)

        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()

        values = result.get("values", [])

        return {
            "success": True,
            "data": values,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


def write_sheet(spreadsheet_id: str, range_name: str, values: list[list]) -> dict:
    """Write data to a Google Sheet."""
    try:
        from googleapiclient.discovery import build

        SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = _get_credentials(SCOPES)

        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        body = {"values": values}
        result = sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()

        return {
            "success": True,
            "data": {"updated_cells": result.get("updatedCells", 0)},
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


def _get_credentials(scopes):
    """Get or refresh Google OAuth credentials."""
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import pickle

    creds = None
    token_path = "token.json"
    creds_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")

    if os.path.exists(token_path):
        import json
        creds = Credentials.from_authorized_user_file(token_path, scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, scopes)
            creds = flow.run_local_server(port=0)

        with open(token_path, "w") as token:
            token.write(creds.to_json())

    return creds
