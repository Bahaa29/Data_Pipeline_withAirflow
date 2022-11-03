# Data Pipeline withAirflow

A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.

They have decided to bring you into the project and expect you to create high grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills. They have also noted that the data quality plays a big part when analyses are executed on top the data warehouse and want to run tests against their datasets after the ETL steps have been executed to catch any discrepancies in the datasets.

The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of CSV logs that tell about user activity in the application and JSON metadata about the songs the users listen to.

## Project Setup - to run locally

1. Install Airflow, create variable AIRFLOW_HOME and AIRFLOW_CONFIG with the appropiate paths, and place dags and plugins on airflor_home directory.
2. Initialize Airflow data base with `airflow initdb`, and open webserver with `airflow webserver`
3. Access the server `http://localhost:8080` and create:

## Project Structure

```
Data Pipeline with Apache Airflow
|
|____dags
| |____ create_tables.sql      # SQL CREATE queries
| |____ udac_example_dag.py    # Main DAG for this ETL data pipeline
|
|____plugins
| |____ __init__.py
| |
| |____operators
| | |____ __init__.py          # Define operators and helpers
| | |____ create_tables_dag.py # create all tables 
| | |____ stage_redshift.py    # COPY data from S3 to Redshift
| | |____ load_fact.py         # Execute INSERT query into fact table
| | |____ load_dimension.py    # Execute INSERT queries into dimension tables
| | |____ data_quality.py      # Data quality check after pipeline execution
| |
| |____helpers
| | |____ __init__.py
| | |____ sql_queries.py       # SQL queries for building up dimensional tables
```

## Data Source 
* Log data: `s3://udacity-dend/log_data`
* Song data: `s3://udacity-dend/song_data`

## DAG Overview 
![example-dag](https://user-images.githubusercontent.com/51878421/199726117-ff30a640-c15e-46db-99db-e10c4206d628.png)

## operators 
* Stage Operator
The stage operator is expected to be able to load any JSON formatted files from S3 to Amazon Redshift. The operator creates and runs a SQL COPY statement based on the parameters provided. The operator's parameters should specify where in S3 the file is loaded and what is the target table.
The parameters should be used to distinguish between JSON file. Another important requirement of the stage operator is containing a templated field that allows it to load timestamped files from S3 based on the execution time and run backfills.

* Fact and Dimension Operators
With dimension and fact operators, you can utilize the provided SQL helper class to run data transformations. Most of the logic is within the SQL transformations and the operator is expected to take as input a SQL statement and target database on which to run the query against. You can also define a target table that will contain the results of the transformation.

* Dimension loads are often done with the truncate-insert pattern where the target table is emptied before the load. Thus, you could also have a parameter that allows switching between insert modes when loading dimensions. Fact tables are usually so massive that they should only allow append type functionality.

* Data Quality Operator
The final operator to create is the data quality operator, which is used to run checks on the data itself. The operator's main functionality is to receive one or more SQL based test cases along with the expected results and execute the tests. For each the test, the test result and expected result needs to be checked and if there is no match, the operator should raise an exception and the task should retry and fail eventually.
For example one test could be a SQL statement that checks if certain column contains NULL values by counting all the rows that have NULL in the column. We do not want to have any NULLs so expected result would be 0 and the test would compare the SQL statement's outcome to the expected result.

* Create tables opeartor 
this oprator execute the create tables.sql file to create all the tables that are needed in the project 
