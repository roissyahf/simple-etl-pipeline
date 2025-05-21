# ETL Pipeline Project
This project is an ETL (Extract, Transform, Load) pipeline built using Python. It is designed to scrape data from a fictional fashion retail website, clean and transform it, and then store it in multiple formats and destinations.

## 🔧 Features
- **Extract**
Scrapes data from: https://fashion-studio.dicoding.dev/

- **Transform**
1. Handles missing and duplicate values
2. Converts prices into a standardized format
3. Ensures all columns are in the correct data types

- **Load**
Saves the clean, transformed dataset into:
1. CSV file
2. Google Spreadsheet (via Google Sheets API)
3. Local PostgreSQL database

**Testing**
Includes test cases using `pytest` to ensure data integrity and pipeline reliability

## 🚀 How to Replicate and Run the Project
### Clone the repository
```git clone https://github.com/roissyahf/simple-etl-pipeline.git```

### Set up virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependency
```pip install -r requirements.txt```

### Set up environment variable using dotenv
Ensure you have installed `python-dotenv`, then fill in the necessary keys
SPREADSHEET_ID=your_spreadsheet_id
DATABASE_URL=postgresql://username:password@localhost:5432/dbname

### Run ETL script
python main.py

### Run unit test in tests folder
pytest tests/ -v

### Run test coverage in tests folder
pytest tests/ --cov=tests --cov-report=term-missing

## 📁 Output
- Data stored in fashion_product.csv
- Data stored in Google Spreadsheet
- Data loaded into local PostgreSQL database

The test case cover 97% with pytest