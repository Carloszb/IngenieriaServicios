import socket
import sys
import time

# --- Configuración del Puerto ---
PUERTO_DEFECTO = 9999
PUERTO = PUERTO_DEFECTO
BUFFER_SIZE = 80

# Obtener puerto de línea de comandos o usar defecto
if len(sys.argv) > 1:
    try:
        PUERTO = int(sys.argv[1])
        print(f"Usando puerto especificado por línea de comandos: {PUERTO}")
    except ValueError:
        print(f"Advertencia: El argumento '{sys.argv[1]}' no es un número. Usando puerto por defecto: {PUERTO_DEFECTO}")
else:
    print(f"No se especificó puerto. Usando puerto por defecto: {PUERTO_DEFECTO}")

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

def enviar_mensaje(sock, mensaje):
    """
    Envía la longitud en ASCII (con delimitador '\n') seguida del mensaje codificado en utf8
    """
    datos = mensaje.encode('utf8')
    longitud = f"{len(datos)}\n"
    sock.sendall(longitud.encode('utf8') + datos)

# --- Creación del socket de escucha ---
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind(("", PUERTO))
except socket.error as e:
    print(f"Error al enlazar el socket: {e}")
    sys.exit(1)

s.listen(5)
print("Servidor listo y escuchando...")

while True:
    print("\nEsperando un cliente...")
    try:
        sd, origen = s.accept()
    except KeyboardInterrupt:
        print("\nServidor cerrado por el usuario (Ctrl+C).")
        s.close()
        sys.exit(0)
    except Exception as e:
        print(f"Error al aceptar la conexión: {e}")
        continue

    print("Nuevo cliente conectado desde %s:%d" % origen)
    continuar = True

    while continuar:
        linea = recibe_mensaje(sd)
        if linea is None:
            print("Conexión cerrada por el cliente.")
            sd.close()
            continuar = False
            continue
        time.sleep(1)
        linea_invertida = linea[::-1]
        print(f"Recibido: '{linea}'. Enviando: '{linea_invertida}'")
        enviar_mensaje(sd, linea_invertida)
