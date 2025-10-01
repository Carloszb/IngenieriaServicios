import socket
import sys

# --- Configuración del Puerto ---
PUERTO_DEFECTO = 9999
PUERTO = PUERTO_DEFECTO
BUFFER_SIZE = 80 # Máximo de bytes a recibir en una lectura

# Obtener puerto de línea de comandos o usar defecto
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
        
        # --- SERVICIO (Inicio de la parte del ejercicio) ---
        
        # Primero recibir el mensaje del cliente
        try:
            # Nota: recv() puede retornar menos de 80 bytes.
            mensaje_bytes = sd.recv(BUFFER_SIZE) 
        except socket.error as e:
            print(f"Error de socket durante la recepción: {e}")
            mensaje_bytes = b""
            
        if not mensaje_bytes: 
            # Si se recibe una cadena vacía (b""), el cliente cerró el socket
            print("Conexión cerrada por el cliente.")
            sd.close()
            continuar = False
            continue
        
        # Convertir los bytes a caracteres (asumiendo UTF-8)
        try:
            mensaje = mensaje_bytes.decode("utf8")
        except UnicodeDecodeError:
            print("Advertencia: Error de decodificación UTF-8. Usando datos brutos.")
            mensaje = str(mensaje_bytes)

        # Segundo, quitarle el "fin de línea" (los 2 últimos caracteres: \r\n)
        # Se asume que el cliente SIEMPRE envía \r\n
        linea = mensaje[:-2] 
        
        # Tercero, darle la vuelta
        linea_invertida = linea[::-1]
        
        # Finalmente, enviar la respuesta con un fin de línea añadido
        respuesta = linea_invertida + "\r\n"
        print(f"Recibido: '{linea}'. Enviando: '{linea_invertida}'")
        
        # Observa la transformación en bytes para enviarlos
        try:
            sd.sendall(respuesta.encode("utf8"))
        except socket.error as e:
            print(f"Error al enviar respuesta: {e}")
            sd.close()
            continuar = False
            
        # --- SERVICIO (Fin de la parte del ejercicio) ---