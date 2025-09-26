"""
Mejora implementada:
- Uso de connect() y recv() 
"""

import socket
import sys

# Procesa los argumentos de la línea de comandos
if len(sys.argv) > 3:
    print("Uso: python udp_cliente5_mejorado.py [host] [puerto]")
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

# *** MEJORA DE SEGURIDAD ***
# Usar connect() para "asociar" el socket con el servidor específico
# Esto hace que recv() solo acepte datagramas de esta dirección
sock.connect(server_address)

print(f"Enviando mensajes a {servidor} en el puerto {puerto}")
print("(Usando connect() para mayor seguridad - solo acepta datagramas del servidor autorizado)")
contador = 1  # Inicializa el contador de mensajes

while True:
    mensaje = input("Introduce el mensaje a enviar (o 'FIN' para salir): ")
    datagrama = f"{contador}: {mensaje}"  # Añade el número de mensaje al principio
    timeout = 0.25  # Timeout inicial en segundos
    sock.settimeout(timeout)
    enviado = False
    while True:
        try:
            # *** MEJORA DE SEGURIDAD ***
            # Usar send() en lugar de sendto() (ya hicimos connect())
            sock.send(datagrama.encode())
            
            # *** MEJORA DE SEGURIDAD ***
            # Usar recv() en lugar de recvfrom()
            # recv() automáticamente descarta datagramas que no vengan
            # de la dirección especificada en connect()
            datos = sock.recv(4096)
            
            respuesta = datos.decode()
            print(f"Confirmación recibida: {respuesta}")
            enviado = True
            break  # Sale del bucle si se recibe la confirmación
        except socket.timeout:
            if timeout >= 2.0:
                print("Puede que el servidor esté caído. Inténtelo más tarde")
                sock.close()
                sys.exit(1)
            timeout *= 2
            print(f"No se recibió confirmación, reenviando el mensaje... (timeout={timeout:.2f}s)")
            sock.settimeout(timeout)
    if mensaje == "FIN":
        break
    if enviado:
        contador += 1  # Incrementa el contador solo si se recibió OK

sock.close()