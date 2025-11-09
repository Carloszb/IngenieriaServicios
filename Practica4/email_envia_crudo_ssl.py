import socket
import ssl
import sys
import base64
import getpass
from email.message import EmailMessage

# --- Función para recibir y verificar respuesta del servidor SMTP ---
def RecvReply(sock, expected_code=None):
    reply = sock.recv(1024)
    decoded = reply.decode().strip()
    print("Servidor:", decoded)

    if expected_code:
        code = reply[:3]
        if code != expected_code:
            print(f"❌ Error: se esperaba {expected_code.decode()}, pero se recibió {code.decode()}")
            sys.exit(1)
    return reply


# --- Configuración del servidor ---
server = "smtp.gmail.com"
port = 587

fromaddr = input("Dirección remitente (tu cuenta Gmail): ")
toaddr   = input("Dirección destino: ")
subject  = "Prueba SMTP con SSL/TLS desde Python (Ejercicio 11)"
data     = "Este mensaje se ha enviado de forma segura usando STARTTLS.\n\nSaludos desde Ingeniería de Servicios."

# --- Crear mensaje con EmailMessage ---
msg = EmailMessage()
msg["From"] = fromaddr
msg["To"] = toaddr
msg["Subject"] = subject
msg.set_content(data)
msg_bytes = msg.as_bytes()

# --- Crear conexión TCP al servidor Gmail ---
print(f"Conectando a {server}:{port} ...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))

RecvReply(s, b"220")

# --- EHLO (en lugar de HELO) ---
s.send(b"EHLO python-client\r\n")
RecvReply(s, b"250")

# --- Iniciar cifrado STARTTLS ---
s.send(b"STARTTLS\r\n")
RecvReply(s, b"220")

# --- Envolver el socket con SSL ---
context = ssl.create_default_context()
sc = context.wrap_socket(s, server_hostname=server)

print(" Conexión segura establecida (TLS).")

# --- Enviar nuevamente EHLO sobre el canal cifrado ---
sc.send(b"EHLO python-client\r\n")
RecvReply(sc, b"250")

# --- Autenticación LOGIN ---
sc.send(b"AUTH LOGIN\r\n")
RecvReply(sc, b"334")

# --- Leer usuario y contraseña ---
username = input("Usuario Gmail (sin @gmail.com si ya lo incluye): ")
password = getpass.getpass("Contraseña o clave de aplicación: ")

# --- Enviar usuario codificado en base64 ---
sc.send(base64.b64encode(username.encode("ascii")) + b"\r\n")
RecvReply(sc, b"334")

# --- Enviar contraseña codificada en base64 ---
sc.send(base64.b64encode(password.encode("utf-8")) + b"\r\n")
RecvReply(sc, b"235")

print(" Autenticación correcta.")

# --- Enviar comandos SMTP para el envío ---
sc.send(f"MAIL FROM:<{fromaddr}>\r\n".encode())
RecvReply(sc, b"250")

sc.send(f"RCPT TO:<{toaddr}>\r\n".encode())
RecvReply(sc, b"250")

sc.send(b"DATA\r\n")
RecvReply(sc, b"354")

# --- Enviar mensaje completo ---
sc.send(msg_bytes)
sc.send(b"\r\n.\r\n")
RecvReply(sc, b"250")

# --- Terminar sesión ---
sc.send(b"QUIT\r\n")
RecvReply(sc, b"221")

sc.close()
print(" Mensaje enviado correctamente.")

