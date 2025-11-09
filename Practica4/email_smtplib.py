import smtplib
import ssl
import getpass
from email.message import EmailMessage

# --- Configuración del servidor SMTP de Gmail ---
server = "smtp.gmail.com"
port = 587  # STARTTLS

# --- Leer usuario y contraseña desde teclado ---
fromaddr = input("Tu cuenta Gmail: ")
password = getpass.getpass("Contraseña o clave de aplicación: ")

# --- Destinatario y contenido ---
toaddr = input("Correo de destino: ")
subject = "Prueba de envío con smtplib (Ejercicio 12)"
body = "Mensaje enviado correctamente usando smtplib, STARTTLS y autenticación segura."

# --- Crear el mensaje con email.message ---
msg = EmailMessage()
msg["From"] = fromaddr
msg["To"] = toaddr
msg["Subject"] = subject
msg.set_content(body)

# --- Crear conexión SMTP ---
print(f"Conectando a {server}:{port} ...")
context = ssl.create_default_context()
s = smtplib.SMTP(server, port)
s.set_debuglevel(1)  # Muestra comandos SMTP y respuestas

# --- Iniciar comunicación y cifrado ---
s.ehlo()
s.starttls(context=context)
s.ehlo()

# --- Autenticación ---
try:
    s.login(fromaddr, password)
    print("Autenticación correcta.")
except smtplib.SMTPAuthenticationError as e:
    print("Error de autenticación:", e)
    s.quit()
    exit()

# --- Enviar el mensaje ---
s.sendmail(fromaddr, toaddr, msg.as_string())
print(" Mensaje enviado correctamente.")

# --- Cerrar conexión ---
s.quit()
print("Conexión cerrada.")
