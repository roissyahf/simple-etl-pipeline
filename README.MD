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
### 1. Clone the repository
```git clone https://github.com/roissyahf/simple-etl-pipeline.git```

### 2. Set up virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependency
```pip install -r requirements.txt```

### 4. Set up environment variable using dotenv
Ensure you have installed `python-dotenv`, then fill in the necessary keys
```
SPREADSHEET_ID=your_spreadsheet_id
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
```

### 5. Run ETL script
```python main.py```

### 6. Run unit test in the tests folder
```pytest tests/ -v```

### 7. Run test coverage in the tests folder
```pytest tests/ --cov=tests --cov-report=term-missing```

## 📁 Output
- Data stored in fashion_product.csv
- Data stored in Google Spreadsheet
- Data loaded into local PostgreSQL database

After testing with `pytest`, the code built covers 97% coverage

![Image](https://github.com/user-attachments/assets/7ded3119-5243-4671-a7c7-d930e343b59e)