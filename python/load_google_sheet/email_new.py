import os
import time
import pandas as pd
from datetime import datetime, timedelta
from google.cloud import bigquery
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#------------------------------Định nghĩa function-----------------
def execute_sql_from_file(sql_file_path):
    """Đọc truy vấn từ tệp .sql"""
    with open(sql_file_path, 'r', encoding='utf-8') as file:
        return file.read()

def get_data_from_bigquery(var_pathinputsql):
    """Lấy dữ liệu từ BigQuery"""
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credential/dw-pgi-5581e99467ae.json' #os.getenv('DBT_PRD_SA')
    client = bigquery.Client()
    inputsql = execute_sql_from_file(var_pathinputsql)
    return client.query(inputsql).result().to_dataframe()

def send_email(email_from, password, email_to, subject, body):
    """Gửi email"""
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, "html"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(email_from, password)
        server.sendmail(email_from, email_to, msg.as_string())
#------------------------------End Định nghĩa function-----------------
print(get_data_from_bigquery('sql/HR_CheckInOut.sql'))
# send_email('maittnhi76@gmail.com', 'ftzo odkc byjd nvdx', 'nhi.mai@pgi.com.vn', 'Thông Tin Chấm Công Trong Tháng - ', 'HTML')
# def format_email_body(df, employee_name, date_note):
#     """Tạo nội dung email từ DataFrame"""
#     html_table = df.to_html(classes='table table-stripped', index=False, justify='left')
#     # Tô màu ngày chủ nhật (có thể mở rộng tùy ý)
#     html_table = html_table.replace("Chủ Nhật", """<span style="background-color:#D6EEEE;">Chủ Nhật</span>""")

#     return f"""
#     <p>Dear anh/chị {employee_name},</p>
#     <p>Phòng Nhân sự xin gửi thông tin chấm công tháng {date_note} như bên dưới:</p>
#     {html_table}
#     <p>Đối với các ngày làm việc bị thiếu chấm công, Anh/Chị vui lòng làm request bổ sung chấm công, phép hoặc xin đi trễ/về sớm chậm nhất là 3 ngày làm việc kể từ khi nhận email này.</p>
#     <p>Vui lòng không phản hồi email tự động này. Có bất kỳ thắc mắc hoặc lỗi vui lòng email: </p>
#     <p>HR: phung.le@pgi.com.vn hoặc liên hệ skype: Phung Le</p>
#     <p>IT: nhi.mai@pgi.com.vn hoặc liên hệ skype: Mai Nhi</p>
#     <p>Thanks & Best Regards</p>
#     """

# def sent_email_checkinout():
#     # Lấy ngày trong tháng
#     date_note = (pd.Timestamp.today() - timedelta(days=1)).strftime("%Y-%m")
    
#     # Lấy dữ liệu từ BigQuery
#     # df = get_data_from_bigquery('sql/HR_Check_In_Out.sql')
#     print (df)
#     exit()
#     # email_list = get_data_from_bigquery('/python/old_modules_bi/sqlfile/checkinout_email_listemail.sql')
#     email_list='nhi.mai@pgi.com.vn' 

#     # Vòng lặp gửi mail
#     for _, row in email_list.iterrows():
#         employee_name = row['tennhanvien']
#         email_to = 'nhi.mai@pgi.com.vn'  # Có thể thay đổi
#         df1 = df[df['machamcong'] == row['machamcong']].copy()
#         df1.columns = ['Tên Nhân Viên', 'Tên Chấm Công', 'Mã Chấm Công', 'Ngày', 'Thứ', 'Giờ Vào', 'Giờ ra', 'Thời gian làm việc']
#         df1 = df1[['Ngày', 'Thứ', 'Giờ Vào', 'Giờ ra']]
        
#         df1["Giờ Vào"].fillna("", inplace=True)
#         df1["Giờ ra"].fillna("", inplace=True)

#         # Tạo nội dung email
#         HTMLBody = format_email_body(df1, employee_name, date_note)
#         # send_email('maittnhi76@gmail.com', 'ftzo odkc byjd nvdx', email_to, f'Thông Tin Chấm Công Trong Tháng - {date_note}', HTMLBody)
#         send_email('maittnhi76@gmail.com', 'ftzo odkc byjd nvdx', email_to, 'Thông tin', HTMLBody)

# # Gọi hàm gửi email
# sent_email_checkinout()
