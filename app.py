from flask import Flask,request, render_template, session
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

app.secret_key= "clave_secreta_super_segura"

@app.route("/login", methods=["GET","POST"])
def login():
 if request.method == "GET":
    return render_template("login.html")

 elif request.method == "POST":
   email = request.form["email"]
   password = request.form["password"]

   conexion = get_coneection()
   cursor = conexion.cursor()

   cursor.execute(
    "SELECT * FROM users WHERE email = ? AND password = ?",(email, password)
    )

   user = cursor.fetchone()

   if user:
            session["user_id"] = user.id
            session["user_name"] = user.name
            session["role"] = user.role
            return f"Bienvenido {user.name}"
   else:
            return "Credenciales incorrectas"

@app.route("/admin")
def admin_panel():
    if "user_id" not in session:
        return "Debes iniciar sesión"
    
    if session["role"] != "admin":
        return "No tienes permiso"
    
    conexion = get_coneection()
    cursor = conexion.cursor()

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

@app.route("/create_class", methods=["POST"])
def create_class():
    if "user_id" not in session or session["role"] != "admin":
        return "No autorizado"
    
    name = request.form["name"]
    schedule = request.form["schedule"].replace("T", " ")
    
    conexion = get_coneection()
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO classes (name,schedule) VALUES (?, ?)", (name,schedule)
    )

    conexion.commit()
    return "Clase creada exitosamente"

@app.route("/")
def inicio():
    if "user_id" not in session:
        return "Debes iniciar sesión"
    
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
   
   if "user_id" not in session:
       return "Debes iniciar sesión"
   user_id= session["user_id"]
   class_id=request.form["class_id"]

   conexion=get_coneection()
   cursor = conexion.cursor()

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
      return "Ya reservaste esta clase"

   cursor.execute(
      "INSERT INTO bookings (user_id, class_id) VALUES (?, ?)",
      (user_id, class_id)
   )
   conexion.commit()

   return("<h2 style='color:green'>La reserva ha sido exitosa</h2>")

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


@app.route("/logout")
def logout():
    session.clear()
    return "Sesión cerrada"
if __name__  == "__main__":
    app.run(debug=True)


