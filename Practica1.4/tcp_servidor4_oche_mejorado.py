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

def recibe_mensaje(socket_cliente):
    """
    Recibe un mensaje completo del socket cliente leyendo byte a byte
    hasta encontrar una línea completa (terminada en \\r\\n).
    
    Args:
        socket_cliente: El socket del cliente del cual leer
        
    Returns:
        str: La línea completa recibida (sin \\r\\n) o None si hay error/conexión cerrada
    """
    mensaje = ""
    
    try:
        while True:
            # Leer un byte a la vez
            byte = socket_cliente.recv(1)
            
            # Si no se recibe nada, el cliente cerró la conexión
            if not byte:
                return None
                
            # Convertir byte a carácter
            try:
                char = byte.decode('utf-8')
            except UnicodeDecodeError:
                # Si hay error de decodificación, ignorar este byte
                continue
                
            # Añadir el carácter al mensaje
            mensaje += char
            
            # Verificar si hemos recibido una línea completa (\r\n)
            if mensaje.endswith('\r\n'):
                # Retornar la línea sin el \r\n
                return mensaje[:-2]
                
    except socket.error as e:
        print(f"Error al recibir mensaje: {e}")
        return None

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
        
        # Primero recibir el mensaje del cliente usando la función recibe_mensaje()
        linea = recibe_mensaje(sd)
        
        if linea is None:
            # Si recibe_mensaje() retorna None, el cliente cerró la conexión o hubo error
            print("Conexión cerrada por el cliente.")
            sd.close()
            continuar = False
            continue
        
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
