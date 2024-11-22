from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.message import EmailMessage
from email import encoders
import smtplib
import os
import json
import pyodbc
import pandas as pd
from pretty_html_table import build_table
import io

with open('D:\\GItHub\\Project 1\\Airflow\\credential\\gmail.json') as content:
    config = json.load(content)

# content = open('.\\Airflow\\credential\\gmail.json')
# config = json.load(content)
# email = config['local']
# password = config['pass']
# sender = 'admin@localmail.com'
# receiver = 'hnawaz@localmail.com'
# subject = "Top 5 Economies of the world"
# message = f"""From: From <{sender}>
# To: To <{receiver}>
# MIME-Version: 1.0
# Content-type: text/html
# Subject: {subject}

# This is an e-mail message to be sent in HTML format

# <b>This is HTML message.</b>
# <h1>This is headline.</h1>
# """
# server = smtplib.SMTP('localhost')
# server.login(email, password)
# server.sendmail(sender, receiver, message)
# {}
# def get_gdp_data():
#     """
#     GDP data
#     :return:
#     """
#     gdp_dict = {'Country': ['United States', 'China', 'Japan', 'Germany', 'India'],
#                 'GDP': ['$21.44 trillion', '$14.14 trillion', '$5.15 trillion', '$3.86 trillion', '$2.94 trillion']}
#     data = pd.DataFrame(gdp_dict)
#     return data
# def send_mail(body):
    
#     message = MIMEMultipart()
#     message['Subject'] = 'Top 5 Economies of the World!'
#     message['From'] = 'maittnhi76@gmail.com'
#     message['To'] = 'nhi.mai@pgi.com.vn'
    
#     body_content = body
#     message.attach(MIMEText(body_content, "html"))
#     msg_body = message.as_string()
    
#     server = smtplib.SMTP('localhost')
#     server.login(email, password)
#     server.sendmail(sender, receiver, msg_body)
#     #
#     server.quit()
    
# data = get_gdp_data()
# data
# output = build_table(data, "blue_light")
# send_mail(output)
# connection = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
#                       "Server=serverName;"
#                       "Database=AdventureWorksDW2012;"
#                       "Trusted_Connection=yes;"
# )

# df = pd.read_sql_query("select top 10 * FROM [AdventureWorks2012].[Sales].[vw_salesoverview] order by OrderDate", connection)
# df.head()
# def send_dataframe(df):
#     multipart = MIMEMultipart()
#     multipart['Subject'] = 'Please find attach your weekly report'
#     multipart['From'] = 'admin@localmail.com'
#     multipart['To'] = 'hnawaz@localmail.com'
#     #
#     for filename in EXPORTERS:
#         attachment = MIMEApplication(EXPORTERS[filename](df))
#         attachment['content-Disposition'] = 'attachement; filename={}'.format(filename)
#         multipart.attach(attachment)
#     #
#     multipart.attach(MIMEText(temp, 'html'))
#     #
#     server = smtplib.SMTP('localhost')
#     server.login(email, password)
#     server.sendmail(sender, receiver, multipart.as_string())
#     #
#     server.quit()
# EXPORTERS = {'Weekly Product Report.csv': export_csv}
# def export_csv(df):
#     with io.StringIO() as buffer:
#         df.to_csv(buffer, index=False)
#         return buffer.getvalue()
# send_dataframe(df)
# bodytemp = r'PathToYourTemplate'
# with open(bodytemp, "r", encoding='utf-8') as f:
#     temp= f.read()