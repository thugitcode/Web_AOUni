from flask import Blueprint, render_template, request
import requests
import ../model.admin import connection

user = Blueprint('user', __name__)

@user.route('/')
def home_user():
    return render_template('user/index.html')

#test demo
@user.route('/tracuu')
def tracuu():
    data = connection()
    return render_template('user/index.html', data=data)