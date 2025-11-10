import poplib
import getpass

# Configuración del servidor POP3
server = "pop.gmail.com"
port = 995

print(f"Conectando a {server}:{port} ...")

# Crear conexión segura con POP3
pop3_mail = poplib.POP3_SSL(server, port)

# Solicitar credenciales
username = input("Usuario Gmail (con @gmail.com): ")
password = getpass.getpass("Clave de aplicación (la de 16 letras): ")

# Autenticación
pop3_mail.user(username)
pop3_mail.pass_(password)

# Consultar número de mensajes
num_messages, total_size = pop3_mail.stat()
print(f"\nNúmero total de mensajes: {num_messages}, Tamaño total: {total_size} bytes\n")

if num_messages == 0:
    print("No hay mensajes en el buzón.")
    pop3_mail.quit()
    exit()

# Procesar solo los 5 más recientes
inicio = max(num_messages - 4, 1)
fin = num_messages

for i, msg_id in enumerate(range(fin, inicio - 1, -1), start=1):
    print(f"--- Mensaje {i} de 5 (ID real: {msg_id}) ---")
    try:
        response, lines, octets = pop3_mail.retr(msg_id)
        print("--- Contenido parcial del mensaje ---")
        for line in lines[:10]:
            print(line.decode("utf-8", errors="ignore"))
        print("... (contenido truncado)\n")
    except Exception as e:
        print(f"Error al leer el mensaje {msg_id}: {e}\n")

# Cerrar conexión
pop3_mail.quit()
print("Conexión cerrada correctamente.")
