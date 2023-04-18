import re
from typing import Dict
import pandas as pd

def remove_blank_dfs(df: pd.DataFrame) -> pd.DataFrame:
    return df


def extract_identifiers(df, identifier_type):
    
    """
    Extracts all identifiers of the specified type from the given dataframe and moves them to a new column.

    Parameters:
    df (pandas.DataFrame): The dataframe to extract identifiers from.
    identifier_type (str): The type of identifier to extract. Valid options are 'phone', 'email', and 'passport'.

    Returns:
    pandas.DataFrame: The dataframe with a new column containing all extracted identifiers of the specified type.
    """

    # Define the regular expression pattern to match identifiers of the specified type
    if identifier_type == 'phone':
        pattern = r'\b(\d{3}[-.\s]??\d{3}[-.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-.\s]??\d{4}|\d{10})\b'
    elif identifier_type == 'email':
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    elif identifier_type == 'passport':
        pattern = r'\b([A-Z]{2}[0-9]{7}|[0-9]{7}[A-Z]{2})\b'
    else:
        raise ValueError("Invalid identifier type. Valid options are 'phone', 'email', and 'passport'.")

    # Create a new column to hold the extracted identifiers
    column_name = f"my_{identifier_type}s"
    df[column_name] = ""

    # Loop through each row in the dataframe and extract identifiers of the specified type
    for i, row in df.iterrows():
        # Join all row values together into a single string for matching
        row_str = " ".join([str(val) for val in row.values])

        # Use regular expression matching to find all identifiers of the specified type
        identifiers = re.findall(pattern, row_str)

        # If any identifiers were found, concatenate them into a comma-separated string
        if identifiers:
            identifier_str = ",".join(identifiers)
            df.at[i, column_name] = identifier_str

    return df

def process_offset_dataframe(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    if any(df.columns == ''):
      # Find the row with the column names
      col_row = None
      for i, row in df.iterrows():
          if not row.isna().any():
              col_row = i
              break
      if col_row is None:
          # No column names found, return the original dataframe
          return df
      # Extract the column names from the column names row
      cols = df.iloc[col_row].tolist()
      # Remove the column names row and any blank rows above it
      df = df.iloc[col_row+1:]
      df.columns = cols
    return df