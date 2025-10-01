import socket
import sys
import random  # Importa el módulo random para generar números aleatorios

# Procesa los argumentos de la línea de comandos
if len(sys.argv) > 2:
    print("Uso: python udp_servidor5_mejorado.py [puerto]")
    sys.exit(1)
elif len(sys.argv) == 1:
    puerto = 9999 # Puerto por defecto
else:
    puerto = int(sys.argv[1]) # Puerto proporcionado por el usuario
    
# Crea un socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', puerto))  # Vincula el socket a todas las interfaces en el puerto
print(f"Servidor UDP escuchando en el puerto {puerto}")

while True:
    # Espera a recibir un datagrama
    datos, direccion = sock.recvfrom(1024)  # Tamaño máximo del datagrama es 1024 bytes
    print(f"Mensaje recibido de {direccion}: {datos.decode()}")

    # Decide aleatoriamente si "pierde" el paquete o no (50% de probabilidad)
    if random.random() < 0.5:
        print("Paquete perdido, no se envía confirmación.")
        continue  # Simula la pérdida del paquete al no enviar respuesta

    # Si no se pierde el paquete, envía una confirmación "OK" al cliente
    respuesta = "OK"
    sock.sendto(respuesta.encode(), direccion)
    print(f"Confirmación enviada a {direccion}: {respuesta}")
    
# El servidor sigue funcionando indefinidamente