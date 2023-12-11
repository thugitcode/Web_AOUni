from flask import Blueprint, render_template, request
import requests

admin = Blueprint('admin', __name__)

@admin.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        return f"{username} {password}"
        # return render_template('admin/admin_login.html',username = username)
    else:
        return render_template('admin/admin_login.html')

   