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

fromaddr = "tu_usuario@uniovi.es"    # Cambia por tu dirección Uniovi
toaddr   = "tu_usuario@uniovi.es"
subject  = "Prueba SMTP con EmailMessage (Ejercicio 8)"
data     = "Este mensaje se ha construido usando EmailMessage y enviado con sockets TCP crudos."

# --- Crear el mensaje con la librería email ---
msg = EmailMessage()
msg["From"] = fromaddr
msg["To"] = toaddr
msg["Subject"] = subject
msg.set_content(data)

# Convertir a bytes (añadiremos la línea final del punto más adelante)
msg_bytes = msg.as_bytes()

# --- Crear socket TCP ---
print(f"Conectando a {server}:{port} ...")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server, port))

# --- Diálogo SMTP ---
RecvReply(sock, b"220")                             # Banner inicial
sock.send(b"HELO uniovi.es\r\n")
RecvReply(sock, b"250")

sock.send(f"MAIL FROM:<{fromaddr}>\r\n".encode())
RecvReply(sock, b"250")

sock.send(f"RCPT TO:<{toaddr}>\r\n".encode())
RecvReply(sock, b"250")

sock.send(b"DATA\r\n")
RecvReply(sock, b"354")

# Enviar cuerpo del mensaje y secuencia final
sock.send(msg_bytes)
sock.send(b"\r\n.\r\n")
RecvReply(sock, b"250")

sock.send(b"QUIT\r\n")
RecvReply(sock, b"221")

sock.close()
print("Mensaje enviado correctamente (si el servidor lo permite).")

