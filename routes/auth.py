from flask import Blueprint, render_template, request, session, redirect, url_for
from models.db import get_connection

auth = Blueprint("auth",__name__)

@auth.route("/login", methods=["GET","POST"])
def login():
 if request.method == "GET":
    return render_template("login.html")

 elif request.method == "POST":
   email = request.form["email"]
   password = request.form["password"]

   conn = get_connection()
   cursor = conn.cursor()

   cursor.execute(
    "SELECT * FROM users WHERE email = ? AND password = ?",
    (email, password)
    )

   user = cursor.fetchone()

   if user:
            session["user_id"] = user.id
            session["user_name"] = user.name
            session["role"] = user.role
            
            if user.role =="admin":
                 return redirect(url_for("admin.dashboard")) 
            else:
                     return redirect(url_for("user.home"))
   else:
        return render_template("login.html", error="Credenciales incorrectas")
   
@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

@auth.route("/register",methods=["GET","POST"])
def register():
     if request.method == "GET":
          return render_template("register.html")
     
     name = request.form["name"]
     email = request.form["email"]
     password = request.form["password"]

     conn = get_connection()
     cursor = conn.cursor()

     cursor.execute("""
              INSERT INTO users (name, email, password, role)
              VALUES (?, ?, ?, 'user')              
               """, (name, email, password))
     
     conn.commit()

     return redirect(url_for("auth.login"))