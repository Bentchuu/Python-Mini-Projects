import os
import smartsheet
import pandas as pd
from smartsheet import Smartsheet

# Insert your Smartsheet API access token here
SMARTSHEET_ACCESS_TOKEN = ''


def get_or_create_sheet(ss_client, sheet_name):
    try:
        # Attempt to get the sheet if it exists
        sheets = ss_client.Sheets.list_sheets(include_all=True).data
        sheet = next((s for s in sheets if s.name == sheet_name), None)
        if sheet is not None:
            sheet = ss_client.Sheets.get_sheet(sheet.id)
            print(f'Using existing sheet: {sheet_name}')
        else:
            raise smartsheet.exceptions.ApiError({'message': f'Sheet "{sheet_name}" not found.', 'error_code': 1006})
    except smartsheet.exceptions.ApiError as ex:
        print(f'Failed to retrieve sheet "{sheet_name}": {ex.message}')
        return None
    return sheet


def update_or_add_rows(sheet, df, ss_client, batch_size=500):
    existing_rows = {row.row_number: row for row in sheet.rows}

    update_rows = []
    new_rows = []

    # Iterate over CSV rows
    for index, csv_row in df.iterrows():
        row_number = index + 1  # CSV is 0-indexed, rows in Smartsheet are 1-indexed
        row_values = [str(value) for value in csv_row.values]
        cells = [{'column_id': col.id, 'value': row_values[i]} for i, col in enumerate(sheet.columns)]

        if row_number in existing_rows:
            # Update existing row
            row = smartsheet.models.Row()
            row.id = existing_rows[row_number].id
            row.cells = cells
            update_rows.append(row)
        else:
            # Add new row
            new_row = smartsheet.models.Row()
            new_row.to_bottom = True
            new_row.cells = cells
            new_rows.append(new_row)

        # Process in batches
        if len(update_rows) == batch_size:
            try:
                response = ss_client.Sheets.update_rows(sheet.id, update_rows)
                if response.message == 'SUCCESS':
                    print(f'Updated {len(response.result)} rows in Smartsheet.')
                else:
                    print(f'Failed to update rows: {response.message}')
            except smartsheet.exceptions.ApiError as ex:
                print(f'Failed to update rows: {ex.message}')
            update_rows = []

        if len(new_rows) == batch_size:
            try:
                response = ss_client.Sheets.add_rows(sheet.id, new_rows)
                if response.message == 'SUCCESS':
                    print(f'Added {len(response.result)} rows to Smartsheet.')
                else:
                    print(f'Failed to add rows: {response.message}')
            except smartsheet.exceptions.ApiError as ex:
                print(f'Failed to add rows: {ex.message}')
            new_rows = []

    # Process any remaining rows
    if update_rows:
        try:
            response = ss_client.Sheets.update_rows(sheet.id, update_rows)
            if response.message == 'SUCCESS':
                print(f'Updated {len(response.result)} rows in Smartsheet.')
            else:
                print(f'Failed to update rows: {response.message}')
        except smartsheet.exceptions.ApiError as ex:
            print(f'Failed to update rows: {ex.message}')

    if new_rows:
        try:
            response = ss_client.Sheets.add_rows(sheet.id, new_rows)
            if response.message == 'SUCCESS':
                print(f'Added {len(response.result)} rows to Smartsheet.')
            else:
                print(f'Failed to add rows: {response.message}')
        except smartsheet.exceptions.ApiError as ex:
            print(f'Failed to add rows: {ex.message}')


def upload_csv_to_smartsheet(folder_path, base_sheet_name):
    # Initialize Smartsheet API client with access token
    ss_client = Smartsheet(SMARTSHEET_ACCESS_TOKEN)

    # Iterate through files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            csv_file_path = os.path.join(folder_path, filename)
            print(f'Processing file: {csv_file_path}')

            # Read CSV into DataFrame
            df = pd.read_csv(csv_file_path)

            # Group by SBU column (adjust the column name as per your CSV)
            for sbu, sbu_data in df.groupby('SBU'):
                # Construct sheet name
                sheet_name = f'{base_sheet_name} - {sbu}'

                # Get or create the sheet
                sheet = get_or_create_sheet(ss_client, sheet_name)

                if isinstance(sheet, smartsheet.models.Sheet):  # Check if sheet is a valid Sheet object
                    print(f'Uploading data for SBU: {sbu} to sheet: {sheet_name}')
                    update_or_add_rows(sheet, sbu_data, ss_client)
                else:
                    print(f'Failed to retrieve or create sheet "{sheet_name}". Check API access or configuration.')


def main():
    # Path to the folder containing CSV files
    folder_path = r'C:\Users\martinez.kenneth\turtol\csvexcel\filtered_data'

    # Base sheet name in Smartsheet
    base_sheet_name = 'SBU Data'

    # Upload CSV files from folder to Smartsheet
    upload_csv_to_smartsheet(folder_path, base_sheet_name)


if __name__ == "__main__":
    main()
