from datetime import timedelta, datetime
import pandas as pd
import sys
import time
from google.cloud import bigquery
import os
import gspread as gs
from oauth2client.service_account import ServiceAccountCredentials


# Các bước Bật Google Sheets API
# Truy cập Google Cloud Console.
# Chọn dự án mà bạn đã tạo hoặc nơi bạn đã tải xuống thông tin xác thực.
# Vào menu "APIs & Services" và chọn "Library".
# Tìm kiếm "Google Sheets API".
# Nhấn vào "Google Sheets API" và chọn "Enable" để bật API.
#-----------------------General Information----------------------------------
#BQ credential
#Set var in local and cloud is difference
# credentials_path = os.getenv('DBT_PRD_SA')
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credential/dw-pgi-5581e99467ae.json'

client = bigquery.Client()
# Xác định phạm vi của quyền truy cập
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# Đường dẫn tới tệp JSON của tài khoản dịch vụ
creds = ServiceAccountCredentials.from_json_keyfile_name('credential/dw-pgi-5581e99467ae.json', scope)
# Uỷ quyền với các thông tin từ tệp JSON
client_ggs = gs.authorize(creds)
# Mở Google Sheet bằng ID
sheet = client_ggs.open_by_key('1wZ62mY7jvQLEkeWWAoZb_U60mRUrCFSxf0e7FO81q_c')


# Lấy trang tính đầu tiên
worksheet = sheet.get_worksheet(0)

# Lấy tất cả các bản ghi từ trang tính
records = worksheet.get_all_records()


df = pd.DataFrame(records)

# Ép kiểu trong pandas
df.columns = df.columns.str.strip()
df['DlrCode'] = df['DlrCode'].astype(pd.Int64Dtype())
df['DlrS1Name'] = df['DlrS1Name'].astype(str)
df['DlrSCode'] = df['DlrSCode'].astype(pd.Int64Dtype())
df['DlrS1Name1'] = df['DlrS1Name1'].astype(str)
df['target'] = df['target'].astype(pd.Int64Dtype())
df['DlrTarget'] = df['DlrTarget'].astype(pd.Int64Dtype())
df['Slman'] = df['Slman'].astype(str)
df['slmanB1'] = df['slmanB1'].astype(str)
df['Namemap'] = df['Namemap'].astype(str)
df['yearmonth'] = pd.to_datetime(df['yearmonth']).dt.date

# df.columns = df.columns.str.strip()
# print (df.columns)
# print(df.head())
# sys.exit ('1234')

table_id = 'dw-pgi.Sales.Target'
schema = [
    bigquery.SchemaField("DlrCode", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("DlrS1Name", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("DlrSCode", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("DlrS1Name1", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("target", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("DlrTarget", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("Slman", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("slmanB1", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("Namemap", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("yearmonth", "DATE", mode="NULLABLE"),
    # Thêm các cột khác tương ứng
]

job_config= bigquery.LoadJobConfig(
# autodetect= True,
schema=schema,
write_disposition ='WRITE_TRUNCATE'
)

job = client.load_table_from_dataframe(df,table_id,job_config=job_config)

while job.state!='DONE':
    time.sleep(2)
    job.reload()
print(job.result())

