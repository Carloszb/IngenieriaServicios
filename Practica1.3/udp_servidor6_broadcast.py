import socket
import sys

# Procesa los argumentos de la línea de comandos
if len(sys.argv) > 2:
    print("Uso: python udp_servidor6_broadcast.py [puerto]")
    sys.exit(1)
elif len(sys.argv) == 1:
    puerto = 12345  # Puerto por defecto para broadcast
else:
    puerto = int(sys.argv[1])

# Crear el socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Permitir la reutilización de la dirección (importante para broadcast)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Vincular el socket a todas las interfaces en el puerto especificado
sock.bind(('', puerto))

print(f"Servidor de broadcast escuchando en puerto {puerto}")
print("Esperando mensajes 'BUSCANDO HOLA' y 'HOLA'...")

while True:
    try:
        # Esperar a recibir un datagrama
        datos, direccion = sock.recvfrom(1024)
        mensaje = datos.decode('utf-8').strip()
        
        print(f"Mensaje recibido de {direccion}: '{mensaje}'")
        
        if mensaje == "BUSCANDO HOLA":
            # Responder al broadcast de descubrimiento
            respuesta = "AQUI ESTOY"
            sock.sendto(respuesta.encode('utf-8'), direccion)
            print(f"Respuesta de descubrimiento enviada a {direccion}: '{respuesta}'")
            
        elif mensaje == "HOLA":
            # Responder al saludo directo
            respuesta = f"¡Hola! Soy el servidor {sock.getsockname()[0]}:{puerto}"
            sock.sendto(respuesta.encode('utf-8'), direccion)
            print(f"Saludo enviado a {direccion}: '{respuesta}'")
            
        else:
            # Mensaje no reconocido
            respuesta = "Mensaje no reconocido. Usa 'BUSCANDO HOLA' o 'HOLA'"
            sock.sendto(respuesta.encode('utf-8'), direccion)
            print(f"Respuesta de error enviada a {direccion}")
            
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario")
        break
    except Exception as e:
        print(f"Error procesando mensaje: {e}")

sock.close()
print("Servidor finalizado")