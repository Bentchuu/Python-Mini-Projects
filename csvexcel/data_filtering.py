# data_filtering.py

import os
import pandas as pd


def load_data(file_path):
    """
    Load CSV data from file_path into a DataFrame and drop specified columns.
    """
    df = pd.read_csv(file_path)

    # List of columns to delete
    columns_to_delete = ['maximo.BaselineName', 'maximo.SiteID', 'maximo.PropertyName',
                         'maximo.PermitType', 'helper', 'Unnamed: 26', 'Unnamed: 27', 'Unnamed: 29']

    # Drop the columns
    df = df.drop(columns=columns_to_delete, errors='ignore')

    return df


def filter_data(df):
    """
    Filter DataFrame for rows where 'Applicable' column contains '1',
    and apply SBU-specific filters saving results to separate CSV files in folders.
    """
    # Columns to check for "1" values
    columns_to_check = ['Applicable']

    # Filter rows where any of the specified columns contain "1"
    filtered_df = df[df[columns_to_check].isin([1]).any(axis=1)]

    # List of filter conditions and corresponding output file names
    sbu_filters = [
        {'value': 'MOG', 'output_folder': 'filtered_data/MOG', 'output_file': 'filtered_MOG.csv'},
        {'value': 'RBG', 'output_folder': 'filtered_data/RBG', 'output_file': 'filtered_RBG.csv',
         'brand_values': ['ALP', 'AVIDA', 'ALVEO', 'AMAIA']},
        {'value': 'EMG', 'output_folder': 'filtered_data/EMG', 'output_file': 'filtered_EMG.csv'},
        {'value': 'VMG-MOG', 'output_folder': 'filtered_data/VMG-MOG', 'output_file': 'filtered_VMG-MOG.csv'},
        {'value': 'VMG-RBG', 'output_folder': 'filtered_data/VMG-RBG', 'output_file': 'filtered_VMG-RBG.csv'},
        {'value': 'VMG-EMG', 'output_folder': 'filtered_data/VMG-EMG', 'output_file': 'filtered_VMG-EMG.csv'}
    ]

    # Apply each filter and save to separate CSV files in respective folders
    for filter_item in sbu_filters:
        value = filter_item['value']
        output_folder = filter_item['output_folder']
        output_file = filter_item['output_file']

        # Create output folder if it does not exist
        os.makedirs(output_folder, exist_ok=True)

        # Filter the DataFrame based on 'SBU' values
        filtered_sbu_df = filtered_df[filtered_df['SBU'] == value]

        # If the SBU value is 'RBG', apply additional filtering on 'BRAND'
        if value == 'RBG':
            brand_values = filter_item.get('brand_values', [])
            for brand in brand_values:
                # Filter the DataFrame based on 'BRAND' values
                filtered_brand_df = filtered_sbu_df[filtered_sbu_df['Brand'] == brand]
                # Save the filtered DataFrame to a new CSV file named by brand in output_folder
                brand_output_file = f'{output_folder}/filtered_RBG_{brand}.csv'
                filtered_brand_df.to_csv(brand_output_file, index=False)
        else:
            # Save the further filtered DataFrame to a new CSV file in output_folder
            output_file_path = f'{output_folder}/{output_file}'
            filtered_sbu_df.to_csv(output_file_path, index=False)

    print('Data filtering and CSV creation completed.')


# Optionally, define a main function to orchestrate data processing if needed
def main(file_path):
    df = load_data(file_path)
    filter_data(df)

# Uncomment the line below if you want to execute the script directly
# main('regcomdata.csv')
