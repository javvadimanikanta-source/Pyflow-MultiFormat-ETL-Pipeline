# PyFlow Multi-Format ETL Pipeline
PyFlow is a Python-based ETL pipeline built to clean and process large taxi trip data.
The main goal of this project is to understand how raw data is converted into clean, usable, and database-ready data using an ETL process.
ETL means:
```text
Extract → Transform → Load
```
---
## Why I Built This Project
In real-world data work, raw data usually comes from different sources and formats. It may contain invalid values, missing columns, duplicate records, or wrong entries.
This project helped me understand how a data pipeline works step by step:
```text
Read raw data
Validate records
Separate invalid rows
Transform useful columns
Save clean output
Load data into database
Generate reports
```
---
## Use Case
This project can be used when we have large trip or transaction data and want to:
* Clean the raw data
* Remove or separate invalid records
* Convert data into different formats
* Load clean records into a database
* Generate simple reports for analysis
I tested this pipeline using NYC Yellow Taxi trip data.
---
## Features
* Reads data from CSV, Parquet, JSON, Excel, and ZIP files
* Saves clean output as CSV, Parquet, JSON, and ZIP
* Loads valid records into MySQL or SQLite
* Separates invalid records into a separate folder
* Generates simple data quality and analysis reports
* Uses YAML config file to control input, output, and database settings
* Supports configurable row processing for testing large datasets
* Includes basic unit tests for main modules
---
## Tech Stack
* Python
* Pandas
* PyArrow
* PyYAML
* MySQL
* SQLite
* SQLAlchemy
* Pytest
* OpenPyXL
* Chardet
---
## Project Structure
```text
Pyflow_ETL_Pipeline/
│
├── config/              # Configuration files
├── data/                # Raw, processed, and invalid data folders
├── logs/                # Pipeline log files
├── pyflow/              # Main ETL source code
├── reports/             # Generated reports
├── screenshots/         # Project screenshots
├── tests/               # Basic unit tests
│
├── main.py              # Pipeline entry point
├── requirements.txt     # Required Python packages
├── pytest.ini           # Pytest configuration
└── README.md
```
---
## Dataset
This project was tested using NYC Yellow Taxi trip data.
The dataset contains taxi trip details such as pickup time, dropoff time, passenger count, trip distance, fare amount, pickup location, and dropoff location.
Large raw datasets are not included in this repository because of file size.
---
## Current Scope
The current validation and transformation logic is based on taxi trip data.
However, the project structure can be reused for other datasets by changing:
* Required columns
* Validation rules
* Transformation logic
* Input file path
* Database settings
So, this project is tested on taxi data, but the pipeline structure is reusable.
---
## How It Works
### 1. Extract
The pipeline reads the input file based on the file type mentioned in the config file.
Supported input formats:
```text
CSV
Parquet
JSON
Excel
ZIP
```
### 2. Validate
The pipeline checks important columns and separates invalid records.
Examples of invalid records:
```text
Negative fare amount
Zero trip distance
Invalid passenger count
```
### 3. Transform
The pipeline creates useful columns such as:
```text
trip_duration_minutes
pickup_hour
pickup_date
```
### 4. Load
The cleaned valid records are loaded into a database.
Supported databases:
```text
MySQL
SQLite
```
### 5. Reports
The pipeline generates simple reports such as:
```text
Data quality report
Hourly fare report
Pickup location report
```
---
## Configuration
The project uses a YAML config file.
Before running the project, copy the example config file:
```bash
copy config\config.example.yaml config\config.yaml
```
Then update the input file path and database details inside:
```text
config/config.yaml
```
Example database section:
```yaml
database:
  type: "mysql"
  table_name: "taxi_trips"
  load_mode: "replace"
  mysql:
    host: "localhost"
    port: 3306
    user: "your_mysql_user"
    password: "your_mysql_password"
    database_name: "pyflow_db"
```
---
## Configurable Row Processing
For large datasets, running the full pipeline every time can take more time.
So, the config file supports row limit-based execution for testing or recording.
Example:
```yaml
processing:
  demo_mode: true
  demo_row_limit: 100000
```
For full data processing:
```yaml
processing:
  demo_mode: false
```
---

## Setup Instructions
### 1. Clone the Repository
```bash
git clone https://github.com/your-username/PyFlow-Multi-Format-ETL-Pipeline.git
cd PyFlow-Multi-Format-ETL-Pipeline
```
### 2. Create Virtual Environment
```bash
python -m venv .venv
```
Activate it on Windows:
```bash
.venv\Scripts\activate
```
### 3. Install Requirements
```bash
pip install -r requirements.txt
```
### 4. Prepare Config File
```bash
copy config\config.example.yaml config\config.yaml
```
Update the input file path and database details.

### 5. Run the Pipeline
```bash
python main.py
```
---
## Sample Output
```text
ETL pipeline Completed Successfully
Total rows: 100000
Valid rows: 97813
Invalid rows: 2187
Clean CSV: data/processed/clean_taxi_data.csv
Clean Parquet: data/processed/clean_taxi_data.parquet
Clean JSON: data/processed/clean_taxi_data.json
Clean ZIP: data/processed/clean_taxi_data.zip
Database type: mysql
Database table: taxi_trips
```
---

## MySQL Verification

After running the pipeline, the loaded data can be checked in MySQL:
```sql
use pyflow_db;
select COUNT(*) AS loaded_rows from taxi_trips;
select * from taxi_trips
limit 10;
```
---
## Testing
Basic unit tests are included.
To run tests:
```bash
pytest
```
---
## Screenshots
Some screenshots of the pipeline execution, generated files, reports, and MySQL verification are added in the `screenshots/` folder.
---
## What I Learned
Through this project, I learned how to build a basic data engineering pipeline using Python.
I learned how to handle multiple file formats, validate data, separate invalid records, transform columns, load clean data into a database, generate reports, and use configuration files to control the pipeline.
---