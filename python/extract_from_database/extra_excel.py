import pyodbc
import pandas as pd  # Nhập khẩu pandas
from datetime import datetime
import os

def execute_sql_from_file(sql_file_path):
    """Đọc truy vấn từ tệp .sql"""
    with open(sql_file_path, 'r', encoding='utf-8') as file:
        query = file.read()
    return query

def get_data_from_sql_server():
    try:
        connection_string = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER=192.168.60.252,1433;'
            f'DATABASE=DWH;'
            f'UID=pgi;'
            f'PWD=Pgi@2023Dev'
        )
        
        # Kết nối đến cơ sở dữ liệu
        conn = pyodbc.connect(connection_string)

        sql_query = """
        SELECT DISTINCT 
            U_InvNo AS 'Số h.đơn',
            U_Date13 AS 'Ngày đến kho',
            U_ContractNo AS 'Số hợp đồng',
            U_IDCCode AS 'Số tờ khai',
            U_BL AS 'Bill of Lading',
            T0.DocEntry,
            T0.DocDate,
            T2.DOCENTRY AS [Landed Cost 1 Number],
            T5.DOCENTRY AS [Landed Cost 2 Number],
            T5.TargetDoc AS [Landed Cost 3 Number],
            T8.TargetDoc AS [Landed Cost 4 Number],
            T11.TargetDoc AS [Landed Cost 5 Number],
            T1.ItemCode,
            T1.Dscription AS [Desription],
            T1.Quantity,
            T1.Price,
            T1.LineTotal,
            T4.AlcCode,
            T4.AlcName AS [Landed Cost 2 Cost Type],
            T3.costsum AS [Landed Cost Cost Total],
            (T2.FoBValue / (T0.DocTotal - T0.VatSum)) * T3.costsum AS [Freight Per SKU],
            T7.AlcCode,
            T7.AlcName AS [Landed Cost 2 Cost Type],
            T6.costsum AS [Landed Cost Cost Total],
            (T5.FoBValue / (T0.DocTotal - T0.VatSum)) * T6.costsum AS [Freight Per SKU],
            T10.AlcCode,
            T10.AlcName AS [Landed Cost 2 Cost Type],
            T9.costsum AS [Landed Cost Cost Total],
            (T8.FoBValue / (T0.DocTotal - T0.VatSum)) * T9.costsum AS [Freight Per SKU],
            T13.AlcCode,
            T13.AlcName AS [Landed Cost 2 Cost Type],
            T12.costsum AS [Landed Cost Cost Total],
            (T11.FoBValue / (T0.DocTotal - T0.VatSum)) * T12.costsum AS [Freight Per SKU]
        FROM OPDN T0 
        INNER JOIN PDN1 T1 ON T0.DocEntry = T1.DocEntry 
        INNER JOIN IPF1 T2 ON T2.BaseType = 20 AND T2.BaseEntry = T1.DocEntry AND T2.ItemCode = T1.ItemCode
        INNER JOIN IPF2 T3 ON T2.DocEntry = T3.DocEntry 
        INNER JOIN OALC T4 ON T3.AlcCode = T4.AlcCode 
        LEFT OUTER JOIN IPF1 T5 ON T5.BaseType = 69 AND T5.BaseEntry = T2.DocEntry AND T5.ItemCode = T2.ItemCode
        LEFT OUTER JOIN IPF2 T6 ON T5.DocEntry = T6.DocEntry
        LEFT OUTER JOIN OALC T7 ON T6.AlcCode = T7.AlcCode
        LEFT OUTER JOIN IPF1 T8 ON T8.BaseType = 69 AND T8.BaseEntry = T5.DocEntry AND T8.ItemCode = T5.ItemCode
        LEFT OUTER JOIN IPF2 T9 ON T8.DocEntry = T9.DocEntry
        LEFT OUTER JOIN OALC T10 ON T9.AlcCode = T10.AlcCode
        LEFT OUTER JOIN IPF1 T11 ON T11.BaseType = 69 AND T11.BaseEntry = T8.DocEntry AND T11.ItemCode = T8.ItemCode
        LEFT OUTER JOIN IPF2 T12 ON T11.DocEntry = T12.DocEntry
        LEFT OUTER JOIN OALC T13 ON T12.AlcCode = T13.AlcCode
        WHERE T0.DocDate BETWEEN '2023-01-01' AND '2023-03-31'
        """   
        
        # Truy vấn dữ liệu
        datafarm_outcome = pd.read_sql(sql_query, conn)

        # Chuyển đổi cột DocDate sang định dạng datetime
        datafarm_outcome['DocDate'] = pd.to_datetime(datafarm_outcome['DocDate'])

        # Đóng kết nối
        conn.close()

        print("Kết nối thành công!")

        # Xuất dữ liệu ra file Excel
        with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
            # Lặp qua từng năm trong dữ liệu
            for year, group in datafarm_outcome.groupby(datafarm_outcome['DocDate'].dt.year):
                # Xuất từng nhóm dữ liệu ra một sheet tương ứng với năm
                group.to_excel(writer, sheet_name=str(year), index=False)

        print("Xuất dữ liệu thành công vào file output.xlsx")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

get_data_from_sql_server()
