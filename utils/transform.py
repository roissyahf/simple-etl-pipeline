import pandas as pd

def transform_to_DataFrame(data):
    """
        Transform to DataFrame
    """
    try:
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"Error transforming data to DataFrame: {e}")
        return None


def transform_data(df):
    """Transforms the input DataFrame."""
    if df.empty:
        print("Input DataFrame is empty. Returning empty DataFrame.")
        return df
    
    try:
        # Combine filtering conditions for conciseness
        df_clean = df[~df.apply(lambda row: row["Title"] == "Unknown Product" or
                                      row["Rating"] in ["Invalid Rating / 5", "Not Rated"] or
                                      row["Price"] == "Price Unavailable", axis=1)]

        df_clean = df_clean.drop_duplicates().dropna()

        # Simplify price transformation
        df_clean.loc[:, "Price"] = df_clean.loc[:, "Price"].str.replace('$', '', regex=False).astype(float) * 16000
        
        # Type conversion and error handling
        if 'Price' in df.columns:
            df_clean.loc[:, 'Price'] = pd.to_numeric(df_clean.loc[:, 'Price']).astype(float)
        if 'Rating' in df.columns:
            df_clean.loc[:, 'Rating'] = pd.to_numeric(df_clean.loc[:, 'Rating']).astype(float)
        if 'Colors' in df.columns:
            df_clean.loc[:, 'Colors'] = pd.to_numeric(df_clean.loc[:, 'Colors']).astype('int64')
        if 'Timestamp' in df.columns:
            df_clean.loc[:, 'Timestamp'] = pd.to_datetime(df_clean.loc[:, 'Timestamp']).astype('datetime64[ns]')

        for col in ['Title', 'Size', 'Gender']:
            df_clean.loc[:, col] = df_clean.loc[:, col].astype(str)

        return df_clean
    
    except KeyError as e:
        print(f"Error: Column '{e}' not found in DataFrame. Check your column names.")
        return None
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None