import pandas as pd


def get_date_range_filename(df, bank_short_code="SBI"):
    """
    Generate a filename based on the date range of transactions in the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing transaction data.
        bank_short_code (str, optional): Short code for the bank. Defaults to "SBI".

    Returns:
        str: Filename string in the format "{bank_short_code}-Statement-from-{oldest_date}-to-{newest_date}.csv"
    """
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
    oldest_date = df["Date"].min().strftime("%d-%m-%y")
    newest_date = df["Date"].max().strftime("%d-%m-%y")
    return f"{bank_short_code}-Statement-from-{oldest_date}-to-{newest_date}.csv"


def sort_and_reindex_df(df):
    """
    Sort the DataFrame by date, reindex it, and add a 'No.' column.

    Args:
        df (pd.DataFrame): DataFrame containing transaction data.

    Returns:
        pd.DataFrame: Sorted and reindexed DataFrame with a new 'No.' column.
    """
    # Convert 'Date' to datetime and sort
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
    df = df.sort_values("Date")

    # Convert 'Date' back to string format
    df["Date"] = df["Date"].dt.strftime("%d/%m/%Y")

    # Reset index and add 'No.' column
    df = df.reset_index(drop=True)
    df.insert(0, "No.", range(1, len(df) + 1))

    return df
