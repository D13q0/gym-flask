from flask import Flask,request, render_template, session, redirect, url_for
import pyodbc
from routes.auth import auth
from routes.admin import admin
from routes.user import user

app = Flask(__name__ )
#Conexión a SQL Server
def get_coneection():
 return pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-GOA1JMC\\SQLEXPRESS;"
    "DATABASE=GymDB;"
    "Trusted_Connection=yes;"
)

app.secret_key= "clave_secreta_super_segura"

app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(user)
if __name__  == "__main__":
    app.run(debug=True)


