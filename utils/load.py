import gspread
from gspread_dataframe import set_with_dataframe
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials

from sqlalchemy import create_engine, text

def store_to_csv(df):
    """
      Store data to CSV
    """
    try:
      print("start writing data to CSV. . .")
      final_df = df.to_csv('fashion_product.csv', index=False)
      return final_df
    
    except Exception as e:
      print(f"Error writing data to CSV: {e}")
      return None

def store_to_googlesheet(df: pd.DataFrame, SERVICE_ACCOUNT_FILE: str, SPREADSHEET_ID: str, WORKSHEET_NAME: str):
    """Stores a Pandas DataFrame to a Google Sheet"""
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    try:
        credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=credentials)
        service.spreadsheets().values().clear(spreadsheetId=SPREADSHEET_ID, range=WORKSHEET_NAME).execute()

        sheet = service.spreadsheets()
        clean_df = df.copy()

        for col in clean_df.columns:
            clean_df[col] = clean_df[col].astype(str)

        values = clean_df.values.tolist()
        body = {"values": values}

        range_label = f"{WORKSHEET_NAME}!A2"

        result = (
            sheet.values()
            .update(
                spreadsheetId=SPREADSHEET_ID,
                range=range_label,
                valueInputOption="RAW",
                body=body,
            )
            .execute()
        )

        print(f"DataFrame successfully written to '{WORKSHEET_NAME}' in spreadsheet '{SPREADSHEET_ID}'")
        return result

    except FileNotFoundError:
        print(f"Error: Service account file '{SERVICE_ACCOUNT_FILE}' not found.")
        return None
    
    except HttpError as error:
        print(f"An HTTP error occurred: {error}")
        return None
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def store_to_postgre(data, db_url):
    """Stores data to PostgreSQL."""
    try:
        engine = create_engine(db_url)
        with engine.connect() as con:
            print("Successfully connected to database")
            create_table_query = text("""
                CREATE TABLE IF NOT EXISTS fashion_product (
                    id SERIAL PRIMARY KEY,
                    "Title" TEXT NOT NULL,
                    "Price" NUMERIC(10, 2) NOT NULL,
                    "Rating" REAL NOT NULL,
                    "Colors" INTEGER NOT NULL,
                    "Size" TEXT NOT NULL,
                    "Gender" TEXT NOT NULL,
                    "Timestamp" TIMESTAMP NOT NULL
                );""")
            con.execute(create_table_query)
            print("Successfully created table fashion_product")

            required_columns = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp']
            if not all(col in data.columns for col in required_columns):
                raise ValueError("Columns in DataFrame do not match PostgreSQL table.")
            
            print("Starting to write data to PostgreSQL...")
            print("Data to be inserted:")
            print(data)
            data.to_sql('fashion_product', con=con, if_exists='append', index=False)
            con.commit()
            print("Data successfully written to PostgreSQL.")
            return True # Indicate success
    except Exception as e:
        print(f"Error writing data to PostgreSQL: {e}")
        return False # Indicate failure