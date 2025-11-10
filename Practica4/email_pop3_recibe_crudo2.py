import socket
import ssl
import sys
import getpass

def RecvReply(sock):
    reply = sock.recv(1024)
    print("Servidor:", reply.decode(errors="ignore").strip())
    if not reply.startswith(b"+OK"):
        print("Error en la respuesta del servidor POP3.")
        sys.exit(1)
    return reply


# Configuración del servidor POP3 de Gmail
server = "pop.gmail.com"
port = 995

print(f"Conectando a {server}:{port} ...")

# Creación del socket y canal seguro
s = socket.socket()
s.connect((server, port))
context = ssl.create_default_context()
sc = context.wrap_socket(s, server_hostname=server)

# Leer mensaje inicial del servidor
RecvReply(sc)

# Solicitar usuario y clave
username = input("Usuario Gmail (con @gmail.com): ")
password = getpass.getpass("Clave de aplicación (la de 16 letras): ")

# Enviar comandos USER y PASS
sc.sendall(f"USER {username}\r\n".encode())
RecvReply(sc)

sc.sendall(f"PASS {password}\r\n".encode())
RecvReply(sc)

# Consultar cuántos mensajes hay disponibles
sc.sendall(b"STAT\r\n")
reply = sc.recv(1024).decode()
print("Servidor:", reply.strip())

try:
    num_msgs = int(reply.split()[1])
except (IndexError, ValueError):
    print("No se pudo obtener el número de correos.")
    sys.exit(1)

if num_msgs == 0:
    print("No hay mensajes nuevos.")
    sc.sendall(b"QUIT\r\n")
    RecvReply(sc)
    sc.close()
    sys.exit(0)

print(f"Hay {num_msgs} mensajes disponibles.\n")

# Procesar los 5 más recientes
inicio = max(num_msgs - 4, 1)
fin = num_msgs

for i in range(fin, inicio - 1, -1):
    print(f"--- Mensaje {i - inicio + 1} de 5 (ID real: {i}) ---")
    sc.sendall(f"RETR {i}\r\n".encode())

    sc.settimeout(10)
    mensaje = b""
    try:
        while True:
            parte = sc.recv(4096)
            if not parte:
                break
            mensaje += parte
            if b"\r\n.\r\n" in mensaje:
                break
    except socket.timeout:
        print(f"(Advertencia) Tiempo de espera agotado al leer el mensaje {i}")

    texto = mensaje.decode(errors="ignore")
    lineas = texto.split("\r\n")

    remitente = None
    asunto = None
    for linea in lineas:
        if linea.lower().startswith("from:"):
            remitente = linea
        elif linea.lower().startswith("subject:"):
            asunto = linea
        if remitente and asunto:
            break

    print(remitente or "From: (no encontrado)")
    print(asunto or "Subject: (no encontrado)")
    print()

# Cerrar sesión
sc.sendall(b"QUIT\r\n")
RecvReply(sc)
sc.close()
print("Conexión cerrada correctamente.")
