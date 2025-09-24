'''
Ejercicio 3 (continuación)

Modifica el cliente y guárdalo con el nombre udp_cliente3_espera_ok.py para que tras cada datagrama enviado espere la confirmación, pero limitando el tiempo de espera como se mostró en el código anterior.

Ejecuta los nuevos cliente y servidor y comprueba cómo cuando el servidor “decide” simular la pérdida de un paquete, el cliente detecta correctamente la no recepción del datagrama.

Comenta el código fuente de ambos programas y envíalos a través de la plataforma.

'''

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
sock.settimeout(1)  # Establece un tiempo de espera de 2 segundos
server_address = (servidor, puerto)
print(f"Enviando mensajes a {servidor} en el puerto {puerto}")
contador = 1  # Inicializa el contador de mensajes

while True:
    mensaje = input("Introduce el mensaje a enviar (o 'FIN' para salir): ")
    datagrama = f"{contador}: {mensaje}"  # Añade el número de mensaje al principio
    while True:
        try:
            sock.sendto(datagrama.encode(), server_address)
            # Espera la confirmación del servidor
            datos, _ = sock.recvfrom(4096)
            print(f"Confirmación recibida: {datos.decode()}")
            break  # Sale del bucle si se recibe la confirmación
        except socket.timeout:
            print("No se recibió confirmación, reenviando el mensaje...")
    if mensaje == "FIN":
        break
    contador += 1  # Incrementa el contador
    
sock.close()