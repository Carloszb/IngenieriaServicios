import socket
import sys
from email.message import EmailMessage

# --- Función para recibir y verificar respuesta del servidor SMTP ---
def RecvReply(sock, expected_code):
    reply = sock.recv(1024)
    print("Servidor:", reply.decode().strip())

    code = reply[:3]
    if code != expected_code:
        print(f"❌ Error: se esperaba {expected_code.decode()}, pero se recibió {code.decode()}")
        sys.exit(1)
    return reply


# --- Datos de configuración ---
server = "relay.uniovi.es"
port = 25

fromaddr = "tu_usuario@uniovi.es"     # Cambia por tu dirección Uniovi
toaddr   = "tu_usuario@uniovi.es"     # Puedes usar tu propio correo como destinatario
subject  = "Prueba SMTP con adjunto (logo ATC)"
data     = "Este correo contiene el logo ATC adjunto.\n\nSaludos."

# --- Crear el mensaje con adjunto usando EmailMessage ---
msg = EmailMessage()
msg["From"] = fromaddr
msg["To"] = toaddr
msg["Subject"] = subject
msg.set_content(data)

# Adjuntar el archivo logoatc.gif (descargado previamente con wget)
try:
    with open("logoatc.gif", "rb") as adjunto:
        contenido = adjunto.read()
        msg.add_attachment(contenido,
                           maintype="image",
                           subtype="gif",
                           filename="logoatc.gif")
except FileNotFoundError:
    print("⚠️  No se encontró 'logoatc.gif'. Asegúrate de haberlo descargado antes:")
    print("    wget http://www.atc.uniovi.es/estilo_atc/logoatc.gif")
    sys.exit(1)

# Convertir mensaje a bytes
msg_bytes = msg.as_bytes()

# --- Crear conexión TCP al servidor SMTP ---
print(f"Conectando a {server}:{port} ...")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server, port))

# --- Secuencia de comandos SMTP ---
RecvReply(sock, b"220")                             # Banner del servidor
sock.send(b"HELO uniovi.es\r\n")
RecvReply(sock, b"250")

sock.send(f"MAIL FROM:<{fromaddr}>\r\n".encode())
RecvReply(sock, b"250")

sock.send(f"RCPT TO:<{toaddr}>\r\n".encode())
RecvReply(sock, b"250")

sock.send(b"DATA\r\n")
RecvReply(sock, b"354")

# Enviar mensaje (cabeceras + cuerpo + adjunto)
sock.send(msg_bytes)
sock.send(b"\r\n.\r\n")   # Línea final de mensaje
RecvReply(sock, b"250")

sock.send(b"QUIT\r\n")
RecvReply(sock, b"221")

sock.close()
print("Mensaje enviado correctamente (si el servidor lo permite).")

