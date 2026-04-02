from flask import Blueprint, render_template, request, session, redirect, url_for
from models.db import get_connection

admin = Blueprint("admin", __name__)

@admin.route("/admin")
def dashboard():
    if "user_id" not in session:
        return "Debes iniciar sesión"
    
    if session["role"] != "admin":
        return "No tienes permiso"
    
    conn = get_connection()
    cursor = conn.cursor()

    #usuarios
    cursor.execute("SELECT * FROM users")
    users=cursor.fetchall()

    #clases
    cursor.execute("SELECT * FROM classes")
    clases=cursor.fetchall()

    #reservas(JOIN)
    cursor.execute("""
        SELECT users.name, classes.name, classes.schedule
        FROM bookings
        JOIN users ON bookings.user_id = users.id
        JOIN classes ON bookings.class_id= classes.id
    """)
    reservas= cursor.fetchall()
    return render_template("admin_dashboard.html",
                           users=users,
                           clases=clases,
                           reservas=reservas)

#CRUD

@admin.route("/create_class", methods=["POST"])
def create_class():
    if "user_id" not in session or session["role"] != "admin":
        return "No autorizado"
    
    name = request.form["name"]
    schedule = request.form["schedule"].replace("T", " ")
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO classes (name,schedule) VALUES (?, ?)", (name,schedule)
    )

    conn.commit()
    return redirect(url_for("admin.dashboard"))

@admin.route("/update_class", methods=["POST"])
def update_class():
    if "user_id" not in session or session["role"] != "admin":
        return "No autorizado"
    
    id =request.form["id"]
    name = request.form["name"]
    schedule = request.form["schedule"].replace("T", " ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE classes SET name = ?, schedule = ? WHERE id = ?",
                   (name, schedule, id))
    
    conn.commit()

    return redirect(url_for("admin.dashboard"))

@admin.route("/delete_class/<int:id>")
def delete_class(id):
    if "user_id" not in session or session["role"] != "admin":
        return "No autorizado"
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM bookings WHERE class_id = ?", (id,))
    cursor.execute("DELETE FROM classes WHERE id = ?",(id,))
    conn.commit()

    return redirect(url_for("admin.dashboard"))
    
@admin.route("/edit_class/<int:id>")
def edit_class(id):
    if "user_id" not in session or session["role"] != "admin":
        return "No autorizado"
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM classes WHERE id = ?", (id,))
    clase= cursor.fetchone()

    return render_template("edit_class.html", clase=clase)

#Ver reservas de todos los clientes

@admin.route("/bookings")
def ver_reservas():
   if "user_id" not in session or session["role"] != "admin":
        return "No autorizado"
   
   conn = get_connection()
   cursor = conn.cursor()

   cursor.execute("""
        SELECT users.name, classes.name, classes.schedule
        FROM bookings
        JOIN users ON bookings.user_id = users.id
        JOIN classes ON bookings.class_id= classes.id
    """)
   
   reservas = cursor.fetchall()

   resultado = "<h1>Reservas</h1>"

   for r in reservas:
      resultado = resultado + f"<p>{r[0]} - {r[1]} - {r[2]}</p>"
      
   return resultado