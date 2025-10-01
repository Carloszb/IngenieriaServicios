import socket
import sys

# --- Función Auxiliar para Recepción Completa ---
def recvall(sock, n):
    """
    Recibe exactamente 'n' bytes del socket.

    Args:
        sock (socket.socket): El socket del cual leer.
        n (int): El número de bytes a recibir.

    Returns:
        bytes: Los datos recibidos, o cadena vacía si la conexión se cierra.
    """
    data = b'' # Inicializa el buffer de bytes
    bytes_restantes = n

    while bytes_restantes > 0:
        try:
            # Intenta leer lo que queda. Si bytes_restantes es grande,
            # recv() leerá lo que pueda hasta ese límite.
            chunk = sock.recv(bytes_restantes)
        except socket.error as e:
            print(f"Error de socket durante recvall: {e}")
            return b'' # Retorna vacío si hay un error de socket

        if not chunk:
            # Si se recibe una cadena vacía, el peer ha cerrado la conexión
            return data # Retorna lo que se haya recibido hasta el momento

        data += chunk
        bytes_restantes -= len(chunk)
    
    return data # Retorna todos los bytes concatenados

# --- Configuración del Puerto ---
PUERTO_DEFECTO = 9999
PUERTO = PUERTO_DEFECTO

# Verifica si se ha pasado un argumento por línea de comandos
if len(sys.argv) > 1:
    try:
        PUERTO = int(sys.argv[1])
        print(f"Usando puerto especificado por línea de comandos: {PUERTO}")
    except ValueError:
        print(f"Advertencia: El argumento '{sys.argv[1]}' no es un número. Usando puerto por defecto: {PUERTO_DEFECTO}")
else:
    print(f"No se especificó puerto. Usando puerto por defecto: {PUERTO_DEFECTO}")

# --- Creación del socket de escucha ---
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asignarle puerto
try:
    s.bind(("", PUERTO))
except socket.error as e:
    print(f"Error al enlazar el socket: {e}")
    sys.exit(1)

# Ponerlo en modo pasivo
s.listen(5)

print("Servidor listo y escuchando...")

# --- Bucle principal de espera por clientes ---
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
    
    # Bucle de atención al cliente conectado
    while continuar:
        # Aquí se usa la nueva función recvall() para asegurar los 5 bytes
        # Observa que ahora la función retorna bytes directamente
        datos_bytes = recvall(sd, 5) 

        if not datos_bytes: 
            # Si recvall retorna b'', es que el cliente cerró o hubo un error fatal
            print("Conexión cerrada por el cliente o error de recepción.")
            sd.close()
            continuar = False
            continue
        
        # Pasar los bytes a caracteres
        try:
            # Se asume que siempre son 5 bytes si la conexión sigue abierta
            datos = datos_bytes.decode("ascii")
        except UnicodeDecodeError:
            print("Advertencia: Datos recibidos no son ASCII puro.")
            datos = f"<{datos_bytes.hex()}> (No ASCII)"

        if datos == "FINAL":
            print("Recibido mensaje de finalización. Cerrando conexión con el cliente.")
            sd.close()
            continuar = False
        else:
            # La lógica original requiere que la lectura sea exactamente de 5 bytes.
            # Si se recibieran menos de 5 bytes y el cliente no cerró, significaría
            # que hubo un problema de protocolo o que la función recvall falló.
            if len(datos_bytes) < 5:
                 print(f"Advertencia: Se esperaban 5 bytes, pero recvall solo devolvió {len(datos_bytes)}. Terminando.")
                 sd.close()
                 continuar = False
            else:
                print("Recibido mensaje: %s" % datos)