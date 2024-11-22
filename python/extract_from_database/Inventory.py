import os
import pandas as pd
from sqlalchemy import create_engine
from google.cloud import bigquery

# Đọc truy vấn từ tệp .sql
def read_sql_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

# Lấy dữ liệu từ SQL Server và trả về DataFrame
def fetch_data_from_sql_server(server, user, password, database, port, sql_file):
    sql_query = read_sql_file(sql_file)
    if not sql_query:
        raise ValueError("SQL query is empty.")
    
    conn_str = f'mssql+pyodbc://{user}:{password}@{server}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
    # conn_str=f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server},{port};DATABASE={database};UID={user};PWD={password}'  
    engine = create_engine(conn_str)
    
    with engine.connect() as conn:
        return pd.read_sql(sql_query, conn)

# Tải dữ liệu vào BigQuery
def upload_to_bigquery(dataframe, table_id, write_disposition='WRITE_TRUNCATE'):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'D:\\GItHub\\Project 1\\Airflow\\credential\\dw-pgi-5581e99467ae.json'
    
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(autodetect=True, write_disposition=write_disposition)
    job = client.load_table_from_dataframe(dataframe, table_id, job_config=job_config)
    
    job.result()  # Chờ cho công việc hoàn thành
    print(f'Data loaded to {table_id}')

# Hàm chính để lấy và tải dữ liệu
def get_and_load_data(table_id, sql_file):
    server = '192.168.60.252'
    user = 'pgi'
    password = 'Pgi@2023Dev'
    database = 'PGI_UAT'
    port = '1433'

    dataframe = fetch_data_from_sql_server(server, user, password, database, port, sql_file)
    upload_to_bigquery(dataframe, table_id)

# Gọi hàm để lấy và tải dữ liệu
get_and_load_data('dw-pgi.Inventory.whse_journal', 'sql/IN_Whse_Journal.sql')
