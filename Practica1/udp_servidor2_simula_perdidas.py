'''
Modifica el servidor anterior para que, tras recibir el datagrama, decida aleatoriamente con una probabilidad del 50% si simulará no haberlo recibido. En este caso imprimirá en pantalla “Simulando paquete perdido”, en otro caso imprimirá en pantalla el contenido del datagrama tal como hacía antes. Para generar números aleatorios usar el módulo random, por ejemplo la función randint(). Guarda el programa con el nombre udp_servidor2_simula_perdidas.py.
Ademas, comenta lo que hace cada cosa'''

import socket
import sys
import random  # Importa el módulo random para generar números aleatorios

# Procesa los argumentos de la línea de comandos
if len(sys.argv) > 2:
    print("Uso: python udp_servidor2_simula_perdidas.py [puerto]")
    sys.exit(1)
elif len(sys.argv) == 1:
    puerto = 9999
else:
    puerto = int(sys.argv[1])
    
# Crear el socket UDP
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind(('localhost', puerto))
print(f"Servidor UDP escuchando en el puerto {puerto}") # Indica que el servidor está listo para recibir mensajes

while True:
    data, direccion = servidor.recvfrom(1024)  # Espera a recibir un datagrama de hasta 1024 bytes
    # Genera un número aleatorio entre 0 y 1 para decidir si simular la pérdida del paquete
    if random.randint(0, 1) == 0:
        print("Simulando paquete perdido")  # Simula la pérdida del paquete
    else:
        print(f"Recibido {data.decode()} de {direccion}")  # Muestra el contenido del datagrama recibido
        servidor.sendto(b"ACK", direccion)  # Envía un acuse de recibo al cliente
        
# El servidor continúa escuchando indefinidamente