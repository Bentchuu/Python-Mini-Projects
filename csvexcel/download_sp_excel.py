# download_sharepoint_excel.py

import requests
from requests_ntlm import HttpNtlmAuth
from io import BytesIO
import pandas as pd
from openpyxl import load_workbook
from config import SHAREPOINT_USERNAME, SHAREPOINT_PASSWORD


def download_excel_from_sharepoint(sharepoint_url, file_path):

    """
    Download an Excel file from SharePoint using NTLM authentication.
    """
    # SharePoint authentication
    auth = HttpNtlmAuth(SHAREPOINT_USERNAME, SHAREPOINT_PASSWORD)

    # Construct the full file URL
    full_url = sharepoint_url + file_path

    # Download the Excel file
    response = requests.get(full_url, auth=auth)

    # Check if the request was successful
    if response.status_code == 200:
        print(f'Downloaded {file_path} successfully.')
        return BytesIO(response.content)
    else:
        print(f'Failed to download {file_path}. Status code: {response.status_code}')
        return None


def convert_excel_to_csv(excel_bytes_io, output_csv_file):
    """
    Convert Excel file (as BytesIO object) to CSV and save to output_csv_file.
    """
    try:
        # Load Excel workbook from BytesIO object
        wb = load_workbook(filename=excel_bytes_io)

        # Assume the first sheet is the one to convert
        sheet = wb.active

        # Load sheet into DataFrame
        df = pd.DataFrame(sheet.values)

        # Save DataFrame to CSV
        df.to_csv(output_csv_file, index=False)

        print(f'Converted Excel to CSV: {output_csv_file}')
    except Exception as e:
        print(f'Failed to convert Excel to CSV: {str(e)}')


def main():
    # SharePoint credentials and file URL
    sharepoint_url = 'https://ayalapropertyph.sharepoint.com'
    file_path = ('Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FRegCom2024%2FShared%20Documents%2FRegCom%20'
                 'Data%2FBASELINES%2F00%20-%20MASTERRegCom Data - 2 BASELINE (Lite).xlsx')

    # Output CSV file path
    output_csv_file = 'regconverted_file.csv'

    # Download Excel file from SharePoint
    excel_bytes_io = download_excel_from_sharepoint(sharepoint_url, file_path)

    if excel_bytes_io:
        # Convert Excel to CSV
        convert_excel_to_csv(excel_bytes_io, output_csv_file)


if __name__ == "__main__":
    main()
