# Train Route Data Engineering Pipeline

An end-to-end Data Engineering project that processes Indian railway train and station route data using Python, PySpark, MySQL, dbt, and Apache Airflow.

## Project Overview

This project demonstrates a complete Data Engineering pipeline that takes raw train and station JSON data, cleans and transforms it, enriches the route data using PySpark, stores the processed data in MySQL, applies dbt transformations and data quality tests, and orchestrates the workflow using Apache Airflow.

## Pipeline

Raw JSON Data
↓
Python Data Cleaning
↓
PySpark Transformation & Enrichment
↓
MySQL
↓
dbt Models & Data Quality Tests
↓
Apache Airflow Orchestration

## Technologies

* Python
* PySpark
* MySQL
* dbt
* Apache Airflow
* Git & GitHub

## Dataset

The pipeline processes:

* 5,208 trains
* 8,990 stations
* 416,637 train route records

The source data contains train schedules, station information, route sequences, arrival and departure times, and journey-day information.

## Data Processing

### Python

Python scripts are used for:

* Cleaning train and station JSON data
* Flattening nested train route information
* Loading processed data into MySQL

### PySpark

PySpark is used to:

* Process 416,637 route records
* Join train routes with station information
* Identify the next station for each route
* Calculate approximate geographic distance using the Haversine formula
* Calculate cumulative route distance
* Calculate remaining route distance

### MySQL

The enriched route dataset is stored in MySQL for structured storage and downstream transformations.

### dbt

dbt is used to:

* Create staging models
* Create train route summary models
* Run data quality tests

### Apache Airflow

Apache Airflow orchestrates the complete pipeline:

1. Run PySpark processing
2. Run dbt models
3. Run dbt data quality tests

The complete Airflow pipeline successfully runs:

`run_spark → run_dbt → test_dbt`

## Project Structure

```text
train-delay-data-engineering/
│
├── data/
│   └── raw/
│
├── ingestion/
│   ├── clean_data.py
│   ├── flatten_routes.py
│   └── load_to_mysql.py
│
├── spark/
│   └── first_spark.py
│
├── dbt_train_delay/
│   ├── models/
│   ├── tests/
│   └── dbt_project.yml
│
├── airflow/
├── tests/
├── config/
├── requirements.txt
└── README.md
```

## Data Quality

The pipeline includes validation and dbt tests to ensure data quality.

Current pipeline results:

* 416,637 route records processed
* 5,208 unique trains
* 0 unmatched route-to-station records
* 0 negative calculated distances
* dbt models successfully executed
* dbt tests successfully passed

## Important Note

This project currently works with train route and scheduled timetable data.

It does **not** contain historical actual-delay observations, so it does not currently perform real train-delay prediction.

The main focus of this project is Data Engineering:

* Data ingestion
* Data cleaning
* Data transformation
* Data enrichment
* Data storage
* Data modeling
* Data quality testing
* Workflow orchestration

## Author

**Omprakash Jadhav**

GitHub: [omprakashjadhav-git](https://github.com/omprakashjadhav-git)

LinkedIn: [Omprakash Jadhav](https://www.linkedin.com/in/omprakash-jadhav-46a752269/)

