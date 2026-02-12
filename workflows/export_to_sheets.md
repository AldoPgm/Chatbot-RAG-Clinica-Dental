---
description: How to export data and deliverables to Google Sheets
---

# Export Data to Google Sheets

## Objective  
Export conversation logs, analytics, or any processed data to Google Sheets for easy access and sharing.

## Required Inputs
- `credentials.json` (Google OAuth) in project root
- Target spreadsheet ID
- Data to export (as list of lists)

## Steps

1. **Set up Google credentials** (first time only)  
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a project and enable the Google Sheets API
   - Create OAuth 2.0 credentials and download `credentials.json`
   - Place it in the project root

2. **Authenticate** (first time only)  
   - Run: `python -c "from tools.google_sheets import read_sheet; read_sheet('test', 'A1')"`
   - A browser window will open for OAuth consent
   - After approval, `token.json` is created automatically

3. **Export data**  
   - Use `tools/google_sheets.py`:
     ```python
     from tools.google_sheets import write_sheet

     data = [
         ["Fecha", "Número", "Mensaje", "Respuesta"],
         ["2026-02-12", "+5491123456789", "Hola", "¡Bienvenido!"]
     ]

     result = write_sheet("your_spreadsheet_id", "Sheet1!A1", data)
     ```

4. **Verify in Google Sheets**  
   - Open the spreadsheet in your browser
   - Confirm the data appears correctly

## Edge Cases
- **Token expired**: Delete `token.json` and re-authenticate
- **Permission denied**: Ensure the Google account has edit access to the spreadsheet
- **Quota exceeded**: Google Sheets API has a limit of 100 requests per 100 seconds

## Tools Used
- `tools/google_sheets.py`
