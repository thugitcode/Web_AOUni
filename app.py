from flask import Flask, render_template
import pyodbc

app = Flask(__name__)

SERVER='DESKTOP-9M2PQQV\SQLEXPRESS'
DATABASE='AOUni'
driver = 'DRIVER={SQL Server};SERVER=' + SERVER + ';DATABASE=' + DATABASE + ';Trusted_Connection=yes;'

conn=pyodbc.connect(driver)

@app.route('/admin/index')
def truong_dai_hoc():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM TruongDaiHoc')
    truong_dai_hoc = cursor.fetchall()
    return render_template('admin/index.html', truong_dai_hoc=truong_dai_hoc)

#điều chỉnh link
from flask import redirect, url_for

@app.route('/admin/redirect/<path:url>')
def redirect_to_website(url):
    return redirect("https://" + url)

def tinh_trung_binh(data):
    if len(data)==0:
        return 0
    return sum(data) / len(data)

@app.route('/admin/diemchuan')
def index():
    # Thực thi truy vấn SQL để lấy thông tin từ bảng dai_hoc
    cursor = conn.cursor()
    cursor.execute('SELECT idMaMon, tenNganh, tenTruong, diemN1, diemN2, diemN3 FROM DiemChuan')

    # Lấy tất cả các bản ghi từ kết quả truy vấn
    data = cursor.fetchall()
    diem_trung_binh=[]
    # Tính điểm trung bình cộng 4 năm của các trường Đại học
    for row in data:
        diem_tb=tinh_trung_binh(row[3:6])
        diem_tb=diem_tb+diem_tb*0.02
        diem_tb=round(diem_tb,3)
        diem_trung_binh.append(diem_tb)
    #kết hợp dữ liệu và dtb thành 1 danh sách    
        zipped_data=list(zip(data,diem_trung_binh))

    # Trả về kết quả điểm trung bình cho template để hiển thị
    return render_template('admin/diemchuan.html', zipped_data=zipped_data)


if __name__ == '__main__':
    app.run(debug=True)
