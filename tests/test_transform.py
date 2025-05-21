import os
import sys
import unittest
import pandas as pd
import numpy as np
from io import StringIO

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.transform import transform_to_DataFrame, transform_data

class TestTransformFunctions(unittest.TestCase):

    def test_transform_to_dataframe(self):
        data = {'col1': [1, 2], 'col2': [3, 4]}
        df = transform_to_DataFrame(data)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertEqual(list(df.columns), ['col1', 'col2'])

    def test_transform_data_empty_df(self):
      # Test with an empty DataFrame
      empty_df = pd.DataFrame()
      transformed_df = transform_data(empty_df)
      self.assertTrue(transformed_df.empty)

    def test_transform_data_inconsistent_values(self): # <<<
        # Create a DataFrame with inconsistent values
        data = """Title,Price,Rating,Colors,Size,Gender,Timestamp
        Unknown Product,$100,4.5,3,M,Male,2025-04-28 14:21:38.988367
        Product B,$200,Invalid Rating / 5,5,L,Female,2025-04-28 14:22:38.988367
        Product C,$120,4,2,S,Male,2025-04-28 14:23:38.988367
        Product D,$170,3.5,4,XL,Male,2025-04-28 14:24:38.988367
        """

        df = pd.read_csv(StringIO(data))
        transformed_df = transform_data(df)

        self.assertFalse(transformed_df['Price'].isna().any(), "There's a NaN in 'Price' column")

    def test_transform_data_duplicates(self):
        data = """Title,Price,Rating,Colors,Size,Gender,Timestamp
        Product A,$100,4.5,3,M,Male,2024-07-26 10:00:00
        Product A,$100,4.5,3,M,Male,2024-07-26 10:00:00"""

        df = pd.read_csv(StringIO(data))
        transformed_df = transform_data(df)
        self.assertEqual(len(transformed_df), 1)

    def test_transform_data_null_values(self):
      data = """Title,Price,Rating,Colors,Size,Gender,Timestamp
      Product A,$100,4.5,3,M,Male,2024-07-26 10:00:00
      Product B,,4,5,L,Female,2024-07-26 11:00:00"""
      df = pd.read_csv(StringIO(data))
      transformed_df = transform_data(df)
      self.assertEqual(len(transformed_df), 1)
      
    def test_transform_data_price_conversion(self):
        data = """Title,Price,Rating,Colors,Size,Gender,Timestamp
        Product A,$100,4.5,3,M,Male,2024-07-26 10:00:00"""
        df = pd.read_csv(StringIO(data))
        transformed_df = transform_data(df)
        self.assertEqual(transformed_df['Price'].iloc[0], 1600000.0)

    def test_transform_data_type_conversion(self):
        data = """Title,Price,Rating,Colors,Size,Gender,Timestamp
        Product A,$100,4.5,3,M,Male,2025-04-28 14:21:42.821418
        Product J,$80,3.6,3,S,Female,2025-04-28 14:21:46.055148
        Product Q,$125,5,6,XL,Men,2025-04-28 14:21:51.310410"""
        df = pd.read_csv(StringIO(data))
        transformed_df = transform_data(df)

        self.assertEqual(transformed_df['Title'].dtype, 'object')
        self.assertEqual(transformed_df['Size'].dtype, 'object')
        self.assertEqual(transformed_df['Gender'].dtype, 'object')
        self.assertEqual(transformed_df['Rating'].dtype, np.float64)
        self.assertEqual(transformed_df['Colors'].dtype, np.int64)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)