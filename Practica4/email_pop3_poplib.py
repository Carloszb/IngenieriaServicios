import poplib
import getpass

# Configuración del servidor POP3
server = "pop.gmail.com"
port = 995

print(f"Conectando a {server}:{port} ...")

# Crear conexión segura con POP3
pop3_mail = poplib.POP3_SSL(server, port)
pop3_mail.set_debuglevel(2)  # Muestra el diálogo POP3 (depuración)

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

# Obtener el primer mensaje
print("Descargando el primer mensaje...\n")
msg_num = 1
response, lines, octets = pop3_mail.retr(msg_num)

# Mostrar contenido del mensaje línea a línea
print("--- Contenido completo del mensaje ---\n")
for line in lines:
    print(line.decode("utf-8", errors="ignore"))

# Cerrar la sesión
pop3_mail.quit()
print("\nConexión cerrada correctamente.")
