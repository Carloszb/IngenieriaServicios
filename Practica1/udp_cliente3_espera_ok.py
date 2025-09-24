import socket
import sys
import random
import time

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
    if mensaje.upper() == "FIN":
        print("Saliendo del cliente.")
        break
    
    datagrama = f"{contador}: {mensaje}"
    sock.sendto(datagrama.encode('utf-8'), server_address)
    
    # Espera la respuesta del servidor con un tiempo de espera de 5 segundos
    try:
        sock.settimeout(5)
        data, server = sock.recvfrom(1024)
        respuesta_servidor = data.decode('utf-8')
        print(f"Respuesta del servidor: {respuesta_servidor}")
    except socket.timeout:
        print("El servidor no respondió en 5 segundos. Inténtalo de nuevo.")
    
    contador += 1
    
sock.close()