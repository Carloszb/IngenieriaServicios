##Escribe un servidor UDP que escuche en el puerto que se le pase por línea de comandos, o en el 9999 por defecto. El servidor estará en un bucle infinito en el que, para cada datagrama que llegue, imprimirá en pantalla el contenido del datagrama y la dirección de la cual proviene. Guárdalo como udp_servidor1.py

import socket
import sys

if len(sys.argv) > 2:
    print("Uso: python udp_servidor1.py [puerto]")
    sys.exit(1)
elif len(sys.argv) == 1:
    puerto = 9999
else:
    puerto = int(sys.argv[1])
    
# Crear el socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', puerto))
print(f"Servidor UDP escuchando en el puerto {puerto}")

while True:
    data, addr = sock.recvfrom(1024)
    print(f"Recibido {data.decode()} de {addr}")
    servidor.sendto(b"ACK", addr)