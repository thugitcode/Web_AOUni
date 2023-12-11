from flask import Flask
from controller.admin import admin
from controller.user import user
app = Flask(__name__)

app.config['SQL_SERVER_DATABASE_URI'] = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=<server>;DATABASE=<database>;UID=<username>;PWD=<password>'
app.register_blueprint(admin)
app.register_blueprint(user)

if __name__ == '__main__':
    app.run(debug=True)
