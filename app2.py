from flask import Flask, render_template,request,redirect, session
from flask_sqlalchemy import SQLAlchemy
import pyodbc

app = Flask(__name__)
#khởi tạo csdl
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc:///?odbc_connect={}'.format('DRIVER={SQL Server};SERVER=DESKTOP-9M2PQQV\SQLEXPRESS;DATABASE=AOUni;Trusted_Connection=yes;')
db = SQLAlchemy(app)
app.secret_key='29122004'

SERVER='DESKTOP-9M2PQQV\SQLEXPRESS'
DATABASE='AOUni'
driver = 'DRIVER={SQL Server};SERVER=' + SERVER + ';DATABASE=' + DATABASE + ';Trusted_Connection=yes;'

conn=pyodbc.connect(driver)
cursor = conn.cursor()

# Định nghĩa lớp TaiKhoan(Model)
class TaiKhoan(db.Model):
    __tablename__= 'TaiKhoan'
    tenthanhvien = db.Column(db.String(50))
    email = db.Column(db.String(50))
    tendangnhap = db.Column(db.String(50),primary_key=True)
    matkhau = db.Column(db.String(50))
    ngaysinh = db.Column(db.Date)
    gioitinh = db.Column(db.String(10))
    trangthai = db.Column(db.String(10))

    def __init__(self, tenthanhvien, email, tendangnhap, matkhau, ngaysinh, gioitinh, trangthai):
        self.tenthanhvien = tenthanhvien
        self.email = email
        self.tendangnhap = tendangnhap
        self.matkhau = matkhau
        self.ngaysinh = ngaysinh
        self.gioitinh = gioitinh
        self.trangthai = trangthai

# Định nghĩa lớp QuanTriVien(Model)
class QuanTriVien(db.Model):
    __tablename__= 'QuanTriVien'
    tendangnhap = db.Column(db.String(50),primary_key=True)
    matkhau = db.Column(db.String(50),primary_key=True)

    def __init__(self, tendangnhap, matkhau):
        self.tendangnhap = tendangnhap
        self.matkhau = matkhau

@app.route('/')
def home():
    if 'logged_in' in session and session['logged_in']:
        return redirect('/giaodien2')
    else:
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        quantrivien = QuanTriVien.query.filter_by(tendangnhap=username, matkhau=password).first()
        if quantrivien:
            session['logged_in'] = True
            session['username'] = username
            return redirect('http://localhost:5500/giaodien2.html')
        else:
            return "Thông tin đăng nhập không chính xác. Vui lòng thử lại."

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# Route để hiển thị thông tin tài khoản
@app.route('/taikhoan')
def xem_taikhoan():
    danh_sach_taikhoan = TaiKhoan.query.all()
    return render_template('taikhoan.html', taikhoans=danh_sach_taikhoan)

#Route để cập nhật thông tin


@app.route('/update', methods=['POST'])
def update():
    id = request.form['id']
    tenTruong = request.form['tenTruong']
    website = request.form['website']
    soluongts = request.form['soluongts']
    maTruong = request.form['maTruong']
    slNganh = request.form['slNganh']
    webTs = request.form['webTs']
    trangthai = request.form['trangthai']

    # Thực hiện câu truy vấn để cập nhật thông tin vào cơ sở dữ liệu
    query = f"UPDATE TruongDaiHoc SET tenTruong='{tenTruong}', website='{website}', soluongts='{soluongts}', maTruong=',{maTruong}', slNganh='{slNganh}', webTs='{webTs}', TrangThai='{trangthai}' WHERE ID={id}"
    cursor.execute(query)
    conn.commit()

    return redirect('/duyetthongtin')

@app.route('/khongduyet', methods=['POST'])
def khongduyet():
    id = request.form['id']

    # Thực hiện câu truy vấn để xóa bản ghi khỏi cơ sở dữ liệu
    query = f"DELETE FROM TruongDaiHoc WHERE ID={id}"
    cursor.execute(query)
    conn.commit()

    return 'Success'

@app.route('/duyetthongtin')
def duyetthongtin():
    # Lấy thông tin từ cơ sở dữ liệu để hiển thị trên trang duyetthongtin.html
    query = "SELECT ID, tenTruong, Website, Soluongts, maTruong, slNganh, webTs, TrangThai FROM TruongDaiHoc"
    cursor.execute(query)
    truongs = cursor.fetchall()

    return render_template('duyetthongtin.html', truongs=truongs)

@app.route('/chuyentrangthai', methods=['POST'])
def chuyentrangthai():
    id = request.form['id']
    trangthai = request.form['trangthai']

    if trangthai == 'Duyệt':
        # Thực hiện câu truy vấn để cập nhật trạng thái thành 'Đã duyệt'
        query = f"UPDATE TruongDaiHoc SET trangthai='Đã duyệt' WHERE ID={id}"
    elif trangthai == 'Không Duyệt':
        # Thực hiện câu truy vấn để cập nhật trạng thái thành 'Đã xóa'
        query = f"UPDATE TruongDaiHoc SET trangthai='Đã xóa' WHERE ID={id}"
    else:
        return 'Invalid trangthai'

    cursor.execute(query)
    conn.commit()

    return redirect('/duyetthongtin')

if __name__ == '__main__':
    app.run()