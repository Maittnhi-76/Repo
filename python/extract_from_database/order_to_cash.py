import os
import time
import pandas as pd
import pyodbc
from google.cloud import bigquery

DBT_PRD_SA='D:\\GItHub\\Project 1\\Airflow\\credential\\dw-pgi-5581e99467ae.json'
# Hàm để đọc SQL từ file
def execute_sql_from_file(sql_file_path):
    """Đọc truy vấn từ tệp .sql"""
    with open(sql_file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Hàm để lấy dữ liệu từ SQL Server
def get_data_from_sql_server(server, user, password, database, port, sqlinput):
    query = execute_sql_from_file(sqlinput)
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server},{port};DATABASE={database};UID={user};PWD={password}'
    
    with pyodbc.connect(connection_string) as conn:
        return pd.read_sql(query, conn)

# Hàm để tải dữ liệu lên BigQuery
def load_data_to_bigquery(dataframe, table_id, write_disposition='WRITE_TRUNCATE'):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] =DBT_PRD_SA
    client = bigquery.Client()

    job_config = bigquery.LoadJobConfig(autodetect=True, write_disposition=write_disposition)
    job = client.load_table_from_dataframe(dataframe, table_id, job_config=job_config)

    while job.state != 'DONE':
        time.sleep(2)
        job.reload()

    print(job.result())

# Hàm để lấy dữ liệu từ BigQuery
def get_data_from_bigquery(pathinputsql):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = DBT_PRD_SA
    client = bigquery.Client()
    
    query = execute_sql_from_file(pathinputsql)
    return client.query(query).result().to_dataframe()

# Hàm chính để lấy và tải dữ liệu
def get_and_load_data(table, sqlinput):
    server = '192.168.60.252'
    user = 'pgi'
    password = 'Pgi@2023Dev'
    database = 'PGI_UAT'
    port = '1433'

    dataframe = get_data_from_sql_server(server, user, password, database, port, sqlinput)
    load_data_to_bigquery(dataframe, table)
    print(table, sqlinput)

# Ví dụ sử dụng
get_and_load_data('dw-pgi.Sales.order_to_cash', 'sql/SA_sales_detail_restructer.sql')
