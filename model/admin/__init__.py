from flask import render_template
import pyodbc

def connection():
    connection = pyodbc.connect(app.config['SQL_SERVER_DATABASE_URI'])
    cursor = connection.cursor()

    # Thực hiện truy vấn
    data = cursor.execute('SELECT * FROM YourTable')
    rows = cursor.fetchall()

    # Đóng kết nối
    cursor.close()
    connection.close()
    return data