import os
import sys
import unittest
from unittest.mock import patch, Mock
import pandas as pd
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.extract import extract_fashion_data, scrape_fashion_data

class TestFashionDataExtraction(unittest.TestCase):

    def setUp(self):
        # Sample HTML for testing
        self.sample_html_1 = """
        <div class="collection-card">
            <h3>Test Title</h3>
            <div class='price-container'><span class='price'>$100</span></div>
            <div class='product-details'>
                <p>Rating: ⭐ 4.5 / 5</p>
                <p>Colors: 3 Colors</p>
                <p>Size: M</p>
                <p>Gender: Male</p>
            </div>
        </div>
        """
        self.sample_html_2 = """
        <div class="collection-card">
            <h3>Test Title</h3>
            <p class='price'>$100</p>
            <div class='product-details'>
                <p>Rating: ⭐ 4 / 5</p>
                <p>Colors: 5 Colors</p>
                <p>Size: L</p>
                <p>Gender: Female</p>
            </div>
        </div>
        """
        self.sample_html_empty = """<div class="collection-card"></div>"""


    def test_extract_fashion_data_success(self):
        soup_1 = BeautifulSoup(self.sample_html_1, 'html.parser')
        fashion_1 = soup_1.find("div", class_="collection-card")
        expected_data_1 = {
            "Title": "Test Title",
            "Price": "$100",
            "Rating": "4.5",
            "Colors": "3",
            "Size": "M",
            "Gender": "Male",
            "Timestamp": type(pd.Timestamp.now())
        }

        result_1 = extract_fashion_data(fashion_1)

        self.assertIsInstance(result_1["Timestamp"], pd.Timestamp)
        result_1["Timestamp"] = type(pd.Timestamp.now())
        self.assertDictEqual(result_1, expected_data_1)


        soup_2 = BeautifulSoup(self.sample_html_2, 'html.parser')
        fashion_2 = soup_2.find("div", class_="collection-card")
        expected_data_2 = {
            "Title": "Test Title",
            "Price": "$100",
            "Rating": "4",
            "Colors": "5",
            "Size": "L",
            "Gender": "Female",
            "Timestamp": type(pd.Timestamp.now())
        }
        result_2 = extract_fashion_data(fashion_2)

        self.assertIsInstance(result_2["Timestamp"], pd.Timestamp)
        result_2["Timestamp"] = type(pd.Timestamp.now())
        self.assertDictEqual(result_2, expected_data_2)

    def test_extract_fashion_data_missing_elements(self):
      soup_empty = BeautifulSoup(self.sample_html_empty, 'html.parser')
      fashion_empty = soup_empty.find("div", class_="collection-card")

      result = extract_fashion_data(fashion_empty)
      self.assertIsNone(result) # or handle the exception appropriately

    @patch('requests.get')
    def test_scrape_fashion_data(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = self.sample_html_1
        mock_get.return_value = mock_response

        result = scrape_fashion_data("https://fashion-studio.dicoding.dev/?page={}", delay=0)
        self.assertIsInstance(result, list)  # Check if the result is a list
        self.assertGreater(len(result), 0) # Check if list is not empty

        # Further assertions based on the expected data structure
        self.assertIn("Title", result[0])
        self.assertIn("Price", result[0])


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

