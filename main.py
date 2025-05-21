from utils.extract import scrape_fashion_data
from utils.transform import transform_to_DataFrame, transform_data
from utils.load import store_to_csv, store_to_googlesheet, store_to_postgre
from dotenv import load_dotenv
import os

load_dotenv()

def main():
  """
  Main function for the whole scraping process, until storing it
  """
  BASE_URL = "https://fashion-studio.dicoding.dev/" # Base URL for the fashion studio website

  # Extract the data via scraping
  all_fashion_data = scrape_fashion_data(BASE_URL)

  if all_fashion_data:
    try:
      # Transform the scrapped result to DataFrame
      DataFrame = transform_to_DataFrame(all_fashion_data)

      # Transform the data
      DataFrame = transform_data(DataFrame)
      print("Data has been successfully transformed")
      print(DataFrame)

      # Load to csv
      store_to_csv(DataFrame)
      print("Data has been successfully stored to CSV")

      # Load to Google Sheet
      SERVICE_ACCOUNT_FILE = './google-sheets-api.json'
      SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
      if SPREADSHEET_ID is None:
        raise ValueError("SPREADSHEET_ID environment variable not set")
      WORKSHEET_NAME = 'Sheet1'

      store_to_googlesheet(DataFrame, SERVICE_ACCOUNT_FILE, SPREADSHEET_ID, WORKSHEET_NAME)
      print("Data has been successfully stored to Google Sheets")

      # Load to PostgreSQL
      DATABASE_URL = os.getenv('DATABASE_URL')
      if DATABASE_URL is None:
        raise ValueError("DATABASE_URL environment variable not set")
      
      store_to_postgre(DataFrame, DATABASE_URL)
      print("Data has been successfully stored to PostgreSQL")

    except Exception as e:
      print(f"An error occurred during the transformation or loading process: {e}")

  else:
    print("No all_fashion_data found")


if __name__ == '__main__':
    main()