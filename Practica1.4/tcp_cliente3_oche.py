import socket
import sys

# --- Configuración ---
IP_DEFECTO = 'localhost'
PUERTO_DEFECTO = 9999

IP_SERVIDOR = IP_DEFECTO
PUERTO_SERVIDOR = PUERTO_DEFECTO

# Obtener IP y Puerto de línea de comandos o usar valores por defecto
if len(sys.argv) > 2:
    IP_SERVIDOR = sys.argv[1]
    try:
        PUERTO_SERVIDOR = int(sys.argv[2])
    except ValueError:
        print(f"Advertencia: Puerto '{sys.argv[2]}' no es válido. Usando {PUERTO_DEFECTO}.")
        PUERTO_SERVIDOR = PUERTO_DEFECTO
elif len(sys.argv) == 2:
    IP_SERVIDOR = sys.argv[1]
    print(f"Usando IP: {IP_SERVIDOR}. Puerto por defecto: {PUERTO_DEFECTO}")
else:
    print(f"Usando por defecto: {IP_DEFECTO}:{PUERTO_DEFECTO}")

# --- Datos de prueba ---
MENSAJES = [
    "HOLA MUNDO!\r\n",
    "PYTHON ES GENIAL.\r\n",
    "1234567890\r\n",
    "FINALIZAR\r\n"
]

# --- Lógica del Cliente ---
try:
    # 1. Crear y Conectar Socket
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"\nIntentando conectar a {IP_SERVIDOR}:{PUERTO_SERVIDOR}...")
    c.connect((IP_SERVIDOR, PUERTO_SERVIDOR))
    print("Conexión exitosa.")

    # 2. Bucle de Envío y Recepción
    for mensaje in MENSAJES:
        
        # Enviar mensaje. Recordar que ya contiene "\r\n".
        datos_a_enviar = mensaje.encode('utf8')
        c.sendall(datos_a_enviar)
        print(f"CLIENTE: Enviado: '{mensaje.strip()}'")

        # Recibir la respuesta del servidor (puede ser más grande que el mensaje enviado)
        respuesta_bytes = c.recv(1024) 
        
        if not respuesta_bytes:
            print("CLIENTE: El servidor cerró la conexión inesperadamente.")
            break
            
        respuesta = respuesta_bytes.decode('utf8').strip()
        print(f"CLIENTE: Recibido (invertido): '{respuesta}'")
        
    # 3. Cerrar Socket
    print("\nCLIENTE: Cerrando conexión.")
    c.close()

except ConnectionRefusedError:
    print(f"\nError: Conexión rechazada. Asegúrate de que '{IP_SERVIDOR}:{PUERTO_SERVIDOR}' esté funcionando.")
except socket.error as e:
    print(f"\nError de socket: {e}")
except Exception as e:
    print(f"\nOcurrió un error inesperado: {e}")