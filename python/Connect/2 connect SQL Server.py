import pyodbc
import pandas as pd  # Nhập khẩu pandas
from datetime import datetime
import os
from google.cloud import bigquery

def execute_sql_from_file(sql_file_path):
    """Đọc truy vấn từ tệp .sql"""
    with open(sql_file_path, 'r', encoding='utf-8') as file:
        query = file.read()
    return query
def get_data_from_sql_server():
    try:
        # conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={'43.239.220.33'},{'1433'};DATABASE={'MITACOSQL'};UID={'ba01'};PWD={'123456aA@'}')
        # connection_string=f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={'43.239.220.33'},{'1433'};DATABASE={'MITACOSQL'};UID={'ba01'};PWD={'123456aA@'}'  
        connection_string=f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={'192.168.60.252'},{'1433'};DATABASE={'DWH'};UID={'pgi'};PWD={'Pgi@2023Dev'}'  
        # Kết nối đến cơ sở dữ liệu
        conn = pyodbc.connect(connection_string)
        # Truy vấn dữ liệu
        # sql_query=execute_sql_from_file('D:/GItHub/Project 1/Airflow/sql/HR_Check_In_Out.sql')
        # sql_query=execute_sql_from_file('D:\GItHub\Project 1\Airflow\sql\FI_Balance_Sheet.sql')     
        sql_query="""Select REPLACE(left(Period,2),'-','') Months,right(Period,4) Years,Account,CatName,N0,N1,CurPeriod,CatId from KQHDKD"""   
        # sql_query = """SELECT
        #                 t1.machamcong,
        #                 tennhanvien,
        #                 tenchamcong,
        #                 ngaycham,
        #                 MIN(GIOCHAM) AS checkin,
        #                 CASE WHEN MAX(giocham) = MIN(giocham) THEN NULL ELSE MAX(giocham) END AS checkout
        #                 FROM CHECKINOUT T1
        #                 LEFT JOIN NHANVIEN T2 ON T1.MaChamCong = T2.MaChamCong 
        #                 GROUP BY t1.machamcong, tennhanvien, tenchamcong, NGAYCHAM
        #                 ORDER BY ngaycham"""  
        # Sử dụng pandas để đọc dữ liệu vào DataFrame
        datafarm_outcome = pd.read_sql(sql_query, conn)
        datafarm_outcome['current_date'] = datetime.now().date()
        print(datafarm_outcome)
        # Đóng kết nối
        conn.close()
        # Hiển thị dữ liệu
 
        print("Kết nối thành công!")
    except Exception as e:
        print(f"Lỗi kết nối: {e}")


def get_data_from_bigquery(var_pathinputsql):
    # BQ credential
    try:
        credentials_path = os.getenv('DBT_PRD_SA')
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'Airflow/credential/dw-pgi-5581e99467ae.json'
        client = bigquery.Client()
        # lấy ngày trong tháng từ Bigquery
        inputsql = get_data_from_sql_server()
        # inputsql = var_pathinputsql
        result = client.query(inputsql).result().to_dataframe()
        return result
        print("Kết nối thành công!")
    except Exception as e:
        print(f"Lỗi kết nối: {e}")

        get_data_from_sql_server