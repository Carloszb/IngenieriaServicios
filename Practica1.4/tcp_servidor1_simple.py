import socket
import sys


PUERTO_DEFECTO = 9999
PUERTO = PUERTO_DEFECTO
if len(sys.argv) > 1:
    try:
        PUERTO = int(sys.argv[1])
        print(f"Usando puerto especificado por línea de comandos: {PUERTO}")
    except ValueError:
        print(f"Advertencia: El argumento '{sys.argv[1]}' no es un número. Usando puerto por defecto: {PUERTO_DEFECTO}")
else:
    print(f"No se especificó puerto. Usando puerto por defecto: {PUERTO_DEFECTO}")

# Creación del socket de escucha
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
# Podríamos haber omitido los parámetros, pues por defecto `socket()` en python
# crea un socket de tipo TCP
# Asignarle puerto

try:
    s.bind(("", PUERTO))  
except socket.error as msg:
    print("Error al asignar el puerto: " + str(msg))
    sys.exit(1)

s.listen(5)  # Máximo de clientes en la cola de espera al accept()

# Bucle principal de espera por clientes
while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s, %d" % origen)
    continuar = True
    # Bucle de atención al cliente conectado
    while continuar:
        datos = sd.recv(5)  # Observar que se lee del socket sd, no de s
        datos = datos.decode("ascii")  # Pasar los bytes a caracteres
                # En este ejemplo se asume que el texto recibido es ascii puro
        if datos=="":  # Si no se reciben datos, es que el cliente cerró el socket
            print("Conexión cerrada de forma inesperada por el cliente")
            sd.close()
            continuar = False
        elif datos=="FINAL":
            print("Recibido mensaje de finalización")
            sd.close()
            continuar = False
        else:
            print("Recibido mensaje: %s" % datos)