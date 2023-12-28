import pyodbc

# Thiết lập kết nối với cơ sở dữ liệu SQL Server

SERVER='DESKTOP-9M2PQQV\SQLEXPRESS'
DATABASE='AOUni'
driver = 'DRIVER={SQL Server};SERVER=' + SERVER + ';DATABASE=' + DATABASE + ';Trusted_Connection=yes;'

conn=pyodbc.connect(driver)
# Hàm để kiểm duyệt thông tin tuyển sinh
def approve_tuyen_sinh(truong_id):
    cursor = conn.cursor()
    cursor.execute('UPDATE TruongDaiHoc SET kiemDuyet = 1 WHERE ID = ?', (truong_id,))
    conn.commit()

# Hàm để lấy danh sách thông tin tuyển sinh đã kiểm duyệt
def get_approved_tuyen_sinh():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM TruongDaiHoc WHERE kiemDuyet = 1')
    return cursor.fetchall()