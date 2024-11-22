import sys
import os
import time
import pymssql
import pyodbc
import pandas as pd
from datetime import datetime, timedelta
from google.cloud import bigquery


#------------------------------Định nghĩa function-----------------
#Hàm để đọc sql từ path
def execute_sql_from_file(sql_file_path):
    """Đọc truy vấn từ tệp .sql"""
    with open(sql_file_path, 'r', encoding='utf-8') as file:
        query = file.read()
    return query

# Hàm để lấy dữ liệu từ SQL Server
def get_data_from_sql_server(var_server, var_user, var_password, var_database, var_port, var_sqlinput):
    # Khai báo chuỗi truy vấn SQL
    # sql_input = var_sqlinput
    sql_input = execute_sql_from_file('sql/HR_Check_In_Out.sql')

    # Kết nối đến cơ sở dữ liệu SQL Server
    # conn = pymssql.connect(
    #     server=var_server,
    #     user=var_user,
    #     password=var_password,
    #     database=var_database,
    #     port=var_port,
    # )
    connection_string=f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={'43.239.220.33'},{'1433'};DATABASE={'MITACOSQL'};UID={'ba01'};PWD={'123456aA@'}'  
        # Kết nối đến cơ sở dữ liệu
    conn = pyodbc.connect(connection_string)
    # Thực hiện truy vấn và lấy dữ liệu vào DataFrame
    datafarm_outcome = pd.read_sql(sql_input, conn)
    datafarm_outcome['current_date'] = datetime.now().date()
    # print (datafarm_outcome)
    # Đóng kết nối
    print(type(conn))
    conn.close()
    
    return datafarm_outcome
# Hàm để tải dữ liệu lên BigQuery
def load_data_to_bigquery(var_dataframe, var_table_id, var_write_disposition = 'WRITE_TRUNCATE'):
    # Cấu hình đường dẫn cho credentials của BigQuery
    credentials_path = os.getenv('DBT_PRD_SA')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'D:\\GItHub\\Project 1\\Airflow\\credential\\dw-pgi-5581e99467ae.json'

    # Kết nối đến BigQuery và tải dữ liệu vào bảng
    client = bigquery.Client()
    # table_id = var_table_id

    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        write_disposition= var_write_disposition
    )

    job = client.load_table_from_dataframe(var_dataframe, var_table_id, job_config=job_config)
    # print (var_dataframe)
    # Đợi cho công việc tải dữ liệu hoàn thành
    while job.state != 'DONE':
        time.sleep(2)
        job.reload()
       

    # In kết quả của công việc tải
    return print(job.result())

def get_data_from_bigquery(var_pathinputsql):
    # BQ credential
    credentials_path = os.getenv('DBT_PRD_SA')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'D:\\GItHub\\Project 1\\Airflow\\credential\\dw-pgi-5581e99467ae.json'
    client = bigquery.Client()

    # lấy ngày trong tháng từ Bigquery
    inputsql = execute_sql_from_file(var_pathinputsql)
    # inputsql = var_pathinputsql
    result = client.query(inputsql).result().to_dataframe()
    return result

#----------------------Dùng function------------------------------------------------------------------------


def get_and_load_data():
    var_sqlinput='sql/HR_Check_In_Out.sql'
    var_server='43.239.220.33'
    var_user='ba01'
    var_password='123456aA@'
    var_database='MITACOSQL'
    var_port=1433
    
    var_dataframe=get_data_from_sql_server(var_server, var_user, var_password, var_database, var_port, var_sqlinput)
    var_table_id='dw-pgi.Human_Resources.checkin_checkout_detail'
    load_data_to_bigquery(var_dataframe, var_table_id, var_write_disposition = 'WRITE_TRUNCATE')

get_and_load_data()