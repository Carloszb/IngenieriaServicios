import socket
import sys

if len(sys.argv) > 3:
    print("Uso: python udp_cliente1.py [host] [puerto]")
    sys.exit(1)
elif len(sys.argv) == 1:
    servidor = 'localhost'
    puerto = 9999
elif len(sys.argv) == 2:
    servidor = sys.argv[1]
    puerto = 9999
else:
    servidor = sys.argv[1]
    puerto = int(sys.argv[2])
    
# Crear el socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (servidor, puerto)
print(f"Enviando mensajes a {servidor} en el puerto {puerto}")

while True:
    mensaje = input("Introduce el mensaje a enviar (o 'FIN' para salir): ")
    sock.sendto(mensaje.encode(), server_address)
    if mensaje == "FIN":
        break

sock.close()