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

def enviar_mensaje(sock, mensaje):
    """
    Envía la longitud en ASCII (con delimitador '\n') seguida del mensaje codificado en utf8
    """
    datos = mensaje.encode('utf8')
    longitud = f"{len(datos)}\n"
    sock.sendall(longitud.encode('utf8') + datos)

def recibe_mensaje(sock):
    """
    Recibe primero la longitud (ASCII, delimitada por '\n'), luego el mensaje de esa longitud
    """
    f = sock.makefile('rb')
    # Leer la longitud
    longitud_str = b''
    while True:
        c = f.read(1)
        if not c:
            return None
        if c == b'\n':
            break
        longitud_str += c
    try:
        longitud = int(longitud_str.decode('utf8'))
    except Exception:
        return None
    # Leer el mensaje completo
    mensaje_bytes = f.read(longitud)
    if not mensaje_bytes or len(mensaje_bytes) < longitud:
        return None
    return mensaje_bytes.decode('utf8')

# --- Datos de prueba ---
MENSAJES = [
    "HOLA MUNDO!",
    "PYTHON ES GENIAL.",
    "1234567890",
    "FINALIZAR"
]

# --- Lógica del Cliente ---
try:
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"\nIntentando conectar a {IP_SERVIDOR}:{PUERTO_SERVIDOR}...")
    c.connect((IP_SERVIDOR, PUERTO_SERVIDOR))
    print("Conexión exitosa.")

    for mensaje in MENSAJES:
        enviar_mensaje(c, mensaje)
        print(f"CLIENTE: Enviado: '{mensaje}'")
        respuesta = recibe_mensaje(c)
        if respuesta is None:
            print("CLIENTE: El servidor cerró la conexión inesperadamente.")
            break
        print(f"CLIENTE: Recibido (invertido): '{respuesta}'")

    print("\nCLIENTE: Cerrando conexión.")
    c.close()

except ConnectionRefusedError:
    print(f"\nError: Conexión rechazada. Asegúrate de que '{IP_SERVIDOR}:{PUERTO_SERVIDOR}' esté funcionando.")
except socket.error as e:
    print(f"\nError de socket: {e}")
except Exception as e:
    print(f"\nOcurrió un error inesperado: {e}")
