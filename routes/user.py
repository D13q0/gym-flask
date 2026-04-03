from flask import Blueprint, render_template, request, session
from models.db import get_connection

user = Blueprint("user", __name__)

@user.route("/")
def home():
    if "user_id" not in session:
        return "Debes iniciar sesión"
    
    conn = get_connection()
    cursor = conn.cursor()

            
    cursor.execute("SELECT * FROM classes")
    clases = cursor.fetchall()
    return render_template("index.html", clases=clases)


@user.route("/classes")
def ver_clases():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM classes")
    clases = cursor.fetchall()

    resultado = "<h1>Clases disponibles</h1>"

    for c in clases:
        resultado = resultado + f"<p>{c.name} - {c.schedule}</p>"
    
    return resultado

@user.route("/book", methods=["POST"])
def reservar():
   
   if "user_id" not in session:
       return "Debes iniciar sesión"
   user_id= session["user_id"]
   class_id=request.form["class_id"]

   conn = get_connection()
   cursor = conn.cursor()
   

   #Validar Usuario
   cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
   user = cursor.fetchone()

   if not user:
      return "<h2 style='color:red'>Usuario no existe</h2>"

   #Validar clase
   cursor.execute("SELECT * FROM classes WHERE id = ?", (class_id,))
   clase = cursor.fetchone()

   if not clase:
      return "Clase no existe"
   

   cursor.execute("""
                SELECT * FROM bookings
                WHERE user_id = ? AND class_id = ?
                  """, (user_id, class_id))
   
   existe = cursor.fetchone()
   
   if existe:
      cursor.execute("SELECT * FROM classes")
      clases = cursor.fetchall()
      return render_template("index.html", clases=clases, error="Ya reservaste esta clase")

   cursor.execute(
      "INSERT INTO bookings (user_id, class_id) VALUES (?, ?)",
      (user_id, class_id)
   )
   conn.commit()

   cursor.execute("SELECT * FROM classes")
   clases = cursor.fetchall()
   return render_template("index.html", clases=clases,  success = "Reservaste con exito")

@user.route("/bookings")
def ver_reservas():
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