import poplib
import getpass
from email import message_from_bytes

# Configuración del servidor POP3 de Gmail
server = "pop.gmail.com"
port = 995

print(f"Conectando a {server}:{port} ...")

# Crear conexión POP3 con SSL
pop3_mail = poplib.POP3_SSL(server, port)
pop3_mail.set_debuglevel(2)  # Activa depuración del protocolo

# Solicitar credenciales
username = input("Usuario Gmail (con @gmail.com): ")
password = getpass.getpass("Clave de aplicación (la de 16 letras): ")

# Autenticación
pop3_mail.user(username)
pop3_mail.pass_(password)

# Consultar número de mensajes
num_messages, total_size = pop3_mail.stat()
print(f"\nNúmero de mensajes: {num_messages}, Tamaño total: {total_size} bytes\n")

if num_messages == 0:
    print("No hay mensajes en el buzón.")
    pop3_mail.quit()
    exit()

# Recorrer todos los mensajes
for i in range(1, num_messages + 1):
    print(f"--- Mensaje {i} ---")
    response, lines, octets = pop3_mail.retr(i)

    # Unir todas las líneas en un solo bloque de bytes
    raw_message = b"\r\n".join(lines)

    # Crear objeto de mensaje a partir de los bytes
    msg = message_from_bytes(raw_message)

    # Mostrar resumen de cabeceras
    print("From:", msg.get("From", "(sin remitente)"))
    print("Subject:", msg.get("Subject", "(sin asunto)"))
    print("Date:", msg.get("Date", "(sin fecha)"))
    print()

# Cerrar la sesión
pop3_mail.quit()
print("Conexión cerrada correctamente.")
