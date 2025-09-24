import socket
import sys

if len(sys.argv) > 3:
    print("Uso: python udp_cliente1.py [host] [puerto]")
    sys.exit(1)
elif len(sys.argv) == 1:
    host = 'localhost'
    puerto = 9999
elif len(sys.argv) == 2:
    host = sys.argv[1]
    puerto = 9999
else:
    host = sys.argv[1]
    puerto = int(sys.argv[2])
    
# Crear el socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (host, puerto)
print(f"Enviando mensajes a {host} en el puerto {puerto}")
contador = 1
while True:

    mensaje = input("Introduce el mensaje a enviar (o 'FIN' para salir): ")
    datagrama = f"{contador}: {mensaje}"
    sock.sendto(datagrama.encode(), server_address)
    if mensaje == "FIN":
        break
    contador+=1    
sock.close()