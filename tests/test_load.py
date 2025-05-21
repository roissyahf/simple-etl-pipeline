from dotenv import load_dotenv
import os
import sys
import unittest
from unittest.mock import patch, Mock, MagicMock, ANY
import pandas as pd
import datetime
from google.oauth2.service_account import Credentials
from sqlalchemy import create_engine, text

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.load import store_to_csv, store_to_googlesheet, store_to_postgre

load_dotenv()

SERVICE_ACCOUNT_FILE = './google-sheets-api.json'
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
WORKSHEET_NAME = 'Sheet1'
DATABASE_URL = os.getenv('DATABASE_URL')

class TestLoadToCSV(unittest.TestCase):

    def setUp(self):
        # Sample DataFrame for testing
        data = {
            'Title': ['Product X', 'Product Y'],
            'Price': [1800000.0, 4500000.0],
            'Rating': [4.0, 5.0],
            'Colors': [6, 3],
            'Size': ['XL', 'M'],
            'Gender': ['Male', 'Female'],
            'Timestamp': pd.to_datetime(['2025-05-02 10:00:00', '2025-05-02 11:00:00'])
        }
        self.sample_df = pd.DataFrame(data)

    @patch('pandas.DataFrame.to_csv')
    def test_store_to_csv(self, mock_to_csv):
        store_to_csv(self.sample_df)
        mock_to_csv.assert_called_once()

class TestLoadToGoogleSheets(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame(
            {
                "Title": ["Product X", "Product Y"],
                "Price": ["$11.99", "$17.99"],
                "Rating": ["4.5", "3.5"],
                "Colors": ["Red, Blue", "Green, Yellow"],
                "Size": ["XL, M, L", "M, S, XL"],
                "Gender": ["Women", "Men"],
                "Timestamp": [datetime.datetime.now(), datetime.datetime.now()],
            }
        )

        self.mock_creds = MagicMock(spec=Credentials)
        self.mock_service = MagicMock()
        self.mock_sheets = MagicMock()
        self.mock_values = MagicMock()
        self.mock_update = MagicMock()
        self.mock_execute = MagicMock()

        self.mock_service.spreadsheets.return_value = self.mock_sheets
        self.mock_sheets.values.return_value = self.mock_values
        self.mock_values.update.return_value = self.mock_update
        self.mock_update.execute.return_value = {"updatedCells": 14}

    @patch("utils.load.Credentials.from_service_account_file")
    @patch("utils.load.build")
    def test_successful_upload(self, mock_build, mock_creds):
        """Test successful upload to Google Sheets."""
        mock_creds.return_value = self.mock_creds
        mock_build.return_value = self.mock_service

        result = store_to_googlesheet(self.data, SERVICE_ACCOUNT_FILE, SPREADSHEET_ID, WORKSHEET_NAME)

        self.assertIsNotNone(result)
        self.assertEqual(result["updatedCells"], 14)
        mock_creds.assert_called_once_with(SERVICE_ACCOUNT_FILE, scopes=ANY)
        mock_build.assert_called_once_with("sheets", "v4", credentials=self.mock_creds)


class TestLoadToPostgre(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_url = DATABASE_URL
        cls.engine = create_engine(cls.db_url)    
        cls.sample_data = pd.DataFrame([
            {
                'Title': 'T-shirt 14',
                'Price': 3248800.0,
                'Rating': 3.8,
                'Colors': 3,
                'Size': 'XL',
                'Gender': 'Women',
                'Timestamp': '2025-05-02T12:00:00'
            }
        ])
        
        with cls.engine.connect() as con:
            con.execute(text("""
            CREATE TABLE IF NOT EXISTS fashion_product (
                id SERIAL PRIMARY KEY,
                "Title" TEXT NOT NULL,
                "Price" NUMERIC(10, 2) NOT NULL,
                "Rating" REAL NOT NULL, -- Changed to REAL for float compatibility
                "Colors" INTEGER NOT NULL,
                "Size" TEXT NOT NULL,
                "Gender" TEXT NOT NULL,
                "Timestamp" TIMESTAMP NOT NULL
            );
            """))
            print("Table fashion_product successfully created.")

    def test_load_to_postgres(self):
        try:
            store_to_postgre(self.sample_data, self.db_url)
        except Exception as e:
            self.fail(f"Error occured: {e}")

        with self.engine.connect() as con:
            result = con.execute(text('SELECT * FROM fashion_product WHERE "Title" = :title'),
                                 {'title': 'T-shirt 14'}).fetchone()
            
            if result:
                print(f"🔍 Query result: {result}")
                print(f"Rating from Database: {result.Rating}")

                # Convert the result to a Pandas Series to access .dtype
                rating_series = pd.Series([result.Rating])
                print(f"Data type of 'Rating' from database: {rating_series.dtype}")

                self.assertIsNotNone(result, "Data not found in the table.")
                self.assertEqual(result.Title, 'T-shirt 14')
                self.assertEqual(result.Price, 3248800.0)
                self.assertEqual(result.Rating, 3.8)
                self.assertEqual(result.Colors, 3)
                self.assertEqual(result.Size, 'XL')
                self.assertEqual(result.Gender, 'Women')
            else:
                print("No data found for the specified title.")
            return True

    @classmethod
    def tearDownClass(cls):
        with cls.engine.connect() as con:
            con.execute(text('DELETE FROM fashion_product WHERE "Title" = :title'),
                        {'title': 'T-shirt 14'})


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)