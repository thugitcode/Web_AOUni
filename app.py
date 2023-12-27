from flask import Flask, render_template,request, redirect, url_for
import pyodbc #kết nối với SQLs

app = Flask(__name__)

SERVER='MAYTINHEDUNG\SQLEXPRESS'
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


#bài in điểm chuẩn
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
    # Tính điểm trung bình cộng 3 năm của các trường Đại học
    for row in data:
        diem_tb=tinh_trung_binh(row[3:6])
        diem_tb=diem_tb+diem_tb*0.02
        diem_tb=round(diem_tb,3)
        diem_trung_binh.append(diem_tb)
    #kết hợp dữ liệu và dtb thành 1 danh sách    
        zipped_data=list(zip(data,diem_trung_binh))

    # Trả về kết quả điểm trung bình cho template để hiển thị
    return render_template('admin/diemchuan.html', zipped_data=zipped_data)

    # ...

# Route để chỉnh sửa thông tin của một trường đại học
@app.route('/admin/edit_truong_dai_hoc/<int:truong_dai_hoc_id>', methods=['GET', 'POST'])
def edit_truong_dai_hoc(truong_dai_hoc_id):
    # Kết nối lại đến cơ sở dữ liệu
    conn = pyodbc.connect(driver)
    cursor = conn.cursor()

    # Xử lý yêu cầu POST khi biểu mẫu chỉnh sửa được gửi đi
    if request.method == 'POST':
        # Lấy dữ liệu mới từ biểu mẫu và đặt vào một dictionary
        new_info = {
            'ten_truong': request.form['tenTruong'],
            'dia_chi': request.form['diachi'],
            'website': request.form['Website'],
            'so_luong_tuyen_sinh': request.form['Soluongts'],
            'ma_truong': request.form['matruong'],
            'so_nganh': request.form['slNganh'],
        }

        # Cập nhật thông tin trong cơ sở dữ liệu
        cursor.execute('UPDATE TruongDaiHoc SET diachi=?, Website=?,Soluongts=?,matruong=?,slNganh=?,tenTruong=? WHERE ID=?',
                       (new_info['dia_chi'],
                        new_info['website'],
                        new_info['so_luong_tuyen_sinh'],
                        new_info['ma_truong'],
                        new_info['so_nganh'],
                        new_info['ten_truong'], truong_dai_hoc_id))
        conn.commit()

        # Lấy lại danh sách trường đại học sau khi chỉnh sửa
        cursor.execute('SELECT * FROM TruongDaiHoc')
        truong_dai_hoc = cursor.fetchall()

        # Hiển thị lại trang 'admin/index.html' với danh sách trường đại học đã cập nhật
        return render_template('admin/index.html', truong_dai_hoc=truong_dai_hoc)

    # Lấy thông tin hiện tại của trường đại học từ cơ sở dữ liệu
    cursor.execute('SELECT * FROM TruongDaiHoc WHERE ID = ?', (truong_dai_hoc_id,))
    truong_dai_hoc_info = cursor.fetchone()

    # Hiển thị trang 'admin/edit_truong_dai_hoc.html' với thông tin trường đại học cần chỉnh sửa
    return render_template('admin/edit_truong_dai_hoc.html', truong_dai_hoc_info=truong_dai_hoc_info)

if __name__ == '__main__':
    app.run(debug=True)
