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
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind(('localhost', puerto))
print(f"Servidor UDP escuchando en el puerto {puerto}")

while True:
    data, direccion = servidor.recvfrom(1024)
    print(f"Recibido {data.decode()} de {direccion}")
    servidor.sendto(b"ACK", direccion)