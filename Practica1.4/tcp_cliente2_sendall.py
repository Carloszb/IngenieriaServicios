import socket
import sys
import time

# --- Configuración del Servidor ---
IP_DEFECTO = 'localhost'
PUERTO_DEFECTO = 9999

IP_SERVIDOR = IP_DEFECTO
PUERTO_SERVIDOR = PUERTO_DEFECTO

# Verifica si se han pasado IP y Puerto por línea de comandos
if len(sys.argv) > 2:
    # Usar IP y Puerto especificados
    IP_SERVIDOR = sys.argv[1]
    try:
        PUERTO_SERVIDOR = int(sys.argv[2])
    except ValueError:
        print(f"Advertencia: El puerto '{sys.argv[2]}' no es un número. Usando puerto por defecto: {PUERTO_DEFECTO}")
        PUERTO_SERVIDOR = PUERTO_DEFECTO
elif len(sys.argv) == 2:
    # Solo se pasó la IP
    IP_SERVIDOR = sys.argv[1]
    print(f"Usando IP: {IP_SERVIDOR}. Puerto por defecto: {PUERTO_DEFECTO}")
else:
    # Usar valores por defecto
    print(f"No se especificaron IP ni Puerto. Usando por defecto: {IP_DEFECTO}:{PUERTO_DEFECTO}")

# --- Creación y Conexión del Socket ---
try:
    # Crear un socket TCP
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conectarse al servidor
    print(f"Intentando conectar a {IP_SERVIDOR}:{PUERTO_SERVIDOR}...")
    c.connect((IP_SERVIDOR, PUERTO_SERVIDOR))
    print("Conexión exitosa. Iniciando envíos de datos.")

    # --- Bucle de Envío de Datos ---
    MENSAJE_5_BYTES = "ABCDE"
    NUM_ENVIOS = 5

    for i in range(NUM_ENVIOS):
        # *** Usando sendall() ***: Garantiza que se envían todos los bytes.
        try:
            c.sendall(MENSAJE_5_BYTES.encode('ascii')) 
            print(f"Envío {i+1}/{NUM_ENVIOS}: Enviado '{MENSAJE_5_BYTES}'.")
        except socket.error as e:
            print(f"Error al enviar datos: {e}")
            break
        time.sleep(0.1)

    # --- Envío de Mensaje de Finalización ---
    MENSAJE_FINAL = "FINAL"
    try:
        # *** Usando sendall() ***: Garantiza que se envían todos los bytes.
        c.sendall(MENSAJE_FINAL.encode('ascii'))
        print(f"Envío final: Enviado '{MENSAJE_FINAL}'.")
    except socket.error as e:
        print(f"Error al enviar mensaje FINAL: {e}")

except ConnectionRefusedError:
    print(f"Error: Conexión rechazada. Asegúrate de que el servidor esté corriendo en {IP_SERVIDOR}:{PUERTO_SERVIDOR}.")
except socket.error as e:
    print(f"Error de socket: {e}")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")

finally:
    # Asegurarse de cerrar el socket
    if 'c' in locals() and c.fileno() != -1:
        print("Cerrando socket cliente y terminando.")
        c.close()