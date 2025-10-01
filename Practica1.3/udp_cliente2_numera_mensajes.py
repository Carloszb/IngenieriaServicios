import socket
import sys

# Procesa los argumentos de la línea de comandos
if len(sys.argv) > 3:
    print("Uso: python udp_cliente2_numera_mensajes.py [host] [puerto]")
    sys.exit(1)
elif len(sys.argv) == 1:
    servidor = 'localhost'  # Host por defecto
    puerto = 9999          # Puerto por defecto
elif len(sys.argv) == 2:
    servidor = sys.argv[1] # Host proporcionado por el usuario
    puerto = 9999          # Puerto por defecto
else:
    servidor = sys.argv[1] # Host proporcionado por el usuario
    puerto = int(sys.argv[2]) # Puerto proporcionado por el usuario

# Crear el socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (servidor, puerto)
print(f"Enviando mensajes a {servidor} en el puerto {puerto}")

contador = 1  # Inicializa el contador de mensajes

while True:
    mensaje = input("Introduce el mensaje a enviar (o 'FIN' para salir): ")
    datagrama = f"{contador}: {mensaje}"  # Añade el número de mensaje al principio
    sock.sendto(datagrama.encode(), server_address)
    if mensaje == "FIN":
        break
    contador += 1  # Incrementa el contador

sock.close()