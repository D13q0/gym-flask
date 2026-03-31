from flask import Flask,request, render_template
import pyodbc

app = Flask(__name__ )
#Conexión a SQL Server
def get_coneection():
 return pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-GOA1JMC\\SQLEXPRESS;"
    "DATABASE=GymDB;"
    "Trusted_Connection=yes;"
)

@app.route("/")
def inicio():
    conexion = get_coneection()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM classes")
    clases = cursor.fetchall()
    return render_template("index.html", clases=clases)

@app.route("/classes")
def ver_clases():
    conexion = get_coneection()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM classes")
    clases = cursor.fetchall()

    resultado = "<h1>Clases disponibles</h1>"

    for c in clases:
        resultado = resultado + f"<p>{c.name} - {c.schedule}</p>"
    
    return resultado

@app.route("/book", methods=["POST"])
def reservar():
   user_id= request.form["user_id"]
   class_id=request.form["class_id"]

   conexion=get_coneection()
   cursor = conexion.cursor()

   cursor.execute(
      "INSERT INTO bookings (user_id, class_id) VALUES (?, ?)",
      (user_id, class_id)
   )
   conexion.commit()

   return("La reserva ha sido exitosa")

@app.route("/bookings")
def ver_reservas():
   conexion= get_coneection()
   cursor = conexion.cursor()

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


if __name__  == "__main__":
    app.run(debug=True)


