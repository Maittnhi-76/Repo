from datetime import timedelta, datetime
import pandas as pd
import time
from google.cloud import bigquery
import os
import gspread as gs
from oauth2client.service_account import ServiceAccountCredentials

# Cấu hình cho Google Sheets API
def setup_google_sheets(api_key_path, sheet_id):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = api_key_path
    # Tạo client cho BigQuery
    client = bigquery.Client()    
    # Định nghĩa phạm vi quyền truy cập
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(api_key_path, scope)    
    # Uỷ quyền với các thông tin từ tệp JSON
    client_ggs = gs.authorize(creds)    
    # Mở Google Sheet bằng ID
    sheet = client_ggs.open_by_key(sheet_id)    
    # Lấy trang tính đầu tiên
    worksheet = sheet.get_worksheet(0)    
    return client, worksheet

# Lấy dữ liệu từ Google Sheets và chuyển đổi thành DataFrame
def load_data_to_dataframe(worksheet):
    records = worksheet.get_all_records()
    df = pd.DataFrame(records)    
    # Ép kiểu trong pandas   
    df.columns = df.columns.str.strip()
    df['Temp_code'] = df['Temp_code'].astype(str)
    df['Temp_name'] = df['Temp_name'].astype(str)
    df['Name_org'] = df['Name_org'].astype(str)
    df['Name_frgn'] = df['Name_frgn'].astype(str)
    
    # Handle empty strings and convert to appropriate data types
    df['No'] = pd.to_numeric(df['No'], errors='coerce').astype(pd.Int64Dtype())
    df['Level'] = pd.to_numeric(df['Level'], errors='coerce').astype(pd.Int64Dtype())
    df['FatherNum'] = pd.to_numeric(df['FatherNum'], errors='coerce').astype(pd.Int64Dtype())
    df['VisOrder'] = pd.to_numeric(df['VisOrder'], errors='coerce').astype(pd.Int64Dtype())

    df['Level3'] = df['Level3'].astype(str)
    df['Level2'] = df['Level2'].astype(str)
    df['Level1'] = df['Level1'].astype(str)
    return df

# Tải DataFrame lên BigQuery
def upload_dataframe_to_bigquery(df, table_id):
    schema = [
        bigquery.SchemaField("Temp_code", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("Temp_name", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("Name_org", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("Name_frgn", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("No", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("Level", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("FatherNum", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("VisOrder", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("Level3", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("Level2", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("Level1", "STRING", mode="NULLABLE")
    ]
    

    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition='WRITE_TRUNCATE'
    )

    client = bigquery.Client()
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)

    while job.state != 'DONE':
        time.sleep(2)
        job.reload()
    return job.result()

# Hàm chính để chạy các chức năng trên
def main(api_key_path, sheet_id, table_id):
    client, worksheet = setup_google_sheets(api_key_path, sheet_id)
    df = load_data_to_dataframe(worksheet)
    upload_result = upload_dataframe_to_bigquery(df, table_id)
    return upload_result

# Cấu hình và chạy hàm chính
if __name__ == "__main__":
    api_key_path = 'credential/dw-pgi-5581e99467ae.json'
    sheet_id = '1YzNFyapOpfO7ftk9yrUuE_qJ5GaITj3BOLA2Tg_2XXU'
    table_id = 'dw-pgi.Financials.financial_templates'

    result = main(api_key_path, sheet_id, table_id)
    print(result)
