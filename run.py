import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, flash, redirect, render_template, request, session, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = 'astroatlas_secret_key_2026'

# -------------------------------------------------------------
# Conexión a Base de Datos MySQL en XAMPP
# -------------------------------------------------------------
def get_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",              # Por defecto en XAMPP está vacía
        database="astroatlas_db"
    )
    return conn

# -------------------------------------------------------------
# 1. Definición de los 2 usuarios fijos
# -------------------------------------------------------------
USUARIOS_FIJOS = {
    "admin": {
        "password": "AdminCosmos2026!",
        "rol": "admin"
    },
    "astro_visitante": {
        "password": "EstrellaNorte2026!",
        "rol": "visitante"
    }
}

# -------------------------------------------------------------
# Envío de credenciales por correo
# -------------------------------------------------------------
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_EMISOR = "astroatlas2627@gmail.com"
EMAIL_PASSWORD = "TU_CONTRASENA_DE_APLICACION"

def enviar_credenciales_correo(correo_destino, nombre_persona):
    cuenta_asignada = "astro_visitante"
    clave_asignada = USUARIOS_FIJOS[cuenta_asignada]["password"]

    asunto = "Credenciales de Acceso - AstroAtlas"
    cuerpo = f"""Hola {nombre_persona},

Gracias por registrarte en AstroAtlas. Tus credenciales de acceso son:

  • Usuario:    {cuenta_asignada}
  • Contraseña: {clave_asignada}

Puedes iniciar sesión en: http://127.0.0.1:5000/login

¡Bienvenido!
Equipo AstroAtlas.
"""
    msg = MIMEMultipart()
    msg['From'] = EMAIL_EMISOR
    msg['To'] = correo_destino
    msg['Subject'] = asunto
    msg.attach(MIMEText(cuerpo, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_EMISOR, EMAIL_PASSWORD)
        server.sendmail(EMAIL_EMISOR, correo_destino, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print("\n" + "=" * 55)
        print(f"[SIMULACIÓN CORREO ENVIADO A: {correo_destino}]")
        print(f"Usuario: {cuenta_asignada} | Clave: {clave_asignada}")
        print("=" * 55 + "\n")
        return True

# -------------------------------------------------------------
# Rutas principales del sitio web
# -------------------------------------------------------------

@app.route('/')
@app.route('/home')
def Home():
    return render_template('pagina_web/home.html')

@app.route('/app')
def App():
    return render_template('pagina_web/app.html')

@app.route('/informacion')
def Informacion():
    conn = get_db()
    # dictionary=True permite usar obs['nombre'], obs['pais'], etc. en Jinja
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM observatorios ORDER BY nombre ASC")
    observatorios = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('pagina_web/informacion.html', observatorios=observatorios)

# -------------------------------------------------------------
# Ruta exclusiva para admin: Agregar nuevo observatorio en MySQL
# -------------------------------------------------------------
@app.route('/agregar_observatorio', methods=['POST'])
def agregar_observatorio():
    if session.get('usuario') != 'admin':
        return "Acceso denegado: solo el administrador puede agregar observatorios.", 403

    nombre = request.form.get('nombre')
    categoria = request.form.get('categoria')
    pais = request.form.get('pais')
    continente = request.form.get('continente')
    coordenadas = request.form.get('coordenadas')
    instrumentos = request.form.get('instrumentos')
    hallazgos = request.form.get('hallazgos')
    ano_inicio = request.form.get('ano_inicio')

    conn = get_db()
    cursor = conn.cursor()
    query = """
        INSERT INTO observatorios (nombre, categoria, pais, continente, coordenadas, instrumentos, hallazgos, ano_inicio)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (nombre, categoria, pais, continente, coordenadas, instrumentos, hallazgos, ano_inicio))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('informacion'))

# -------------------------------------------------------------
# Rutas de Autenticación y Logout
# -------------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def Login():
    if 'usuario' in session:
        return redirect(url_for('informacion'))

    error_login = None
    if request.method == 'POST':
        usuario = request.form.get('usuario', '').strip()
        password = request.form.get('password', '').strip()

        if usuario in USUARIOS_FIJOS and USUARIOS_FIJOS[usuario]["password"] == password:
            session['usuario'] = usuario
            session['rol'] = USUARIOS_FIJOS[usuario]["rol"]
            return redirect(url_for('informacion'))
        else:
            error_login = "Credenciales incorrectas. Verifica tu usuario o contraseña."

    return render_template('aplicacion/login/login.html', error_login=error_login)

@app.route('/solicitar_acceso', methods=['POST'])
def solicitar_acceso():
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')

    if correo and nombre:
        enviar_credenciales_correo(correo, nombre)
        return render_template('aplicacion/login/login.html', correo_enviado=correo)

    return redirect(url_for('Login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('Login'))

# -------------------------------------------------------------
# Ejecución del servidor
# -------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)