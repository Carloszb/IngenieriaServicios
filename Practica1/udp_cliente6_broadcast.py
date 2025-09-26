"""
udp_cliente6_broadcast.py - Cliente de descubrimiento por broadcast

El cliente:
1. Envía un broadcast "BUSCANDO HOLA" al puerto 12345
2. Recibe respuestas de servidores con timeout
3. Se conecta al primer servidor que responda y le envía "HOLA"
4. Muestra la respuesta final del servidor
"""

import socket
import sys
import time

def obtener_direccion_broadcast():
    """
    Uso 255.255.255.255 (broadcast global)
    """
    return '255.255.255.255'

def main():
    # Procesa los argumentos de la línea de comandos
    if len(sys.argv) > 2:
        print("Uso: python udp_cliente6_broadcast.py [puerto_broadcast]")
        sys.exit(1)
    elif len(sys.argv) == 1:
        puerto_broadcast = 12345  # Puerto por defecto
    else:
        puerto_broadcast = int(sys.argv[1])
    
    # Crear el socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Habilitar el modo broadcast
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    # Vincular a cualquier puerto disponible
    sock.bind(('', 0))
    
    print("=== Cliente de Descubrimiento por Broadcast ===")
    print(f"Buscando servidores en puerto {puerto_broadcast}...")
    
    # Paso 1: Enviar broadcast "BUSCANDO HOLA"
    direccion_broadcast = obtener_direccion_broadcast()
    mensaje_broadcast = "BUSCANDO HOLA"
    
    print(f"Enviando broadcast a {direccion_broadcast}:{puerto_broadcast}: '{mensaje_broadcast}'")
    sock.sendto(mensaje_broadcast.encode('utf-8'), (direccion_broadcast, puerto_broadcast))
    
    # Paso 2: Recibir respuestas con timeout
    servidores_encontrados = []
    primer_servidor = None
    timeout = 3.0  # 3 segundos para esperar respuestas
    
    sock.settimeout(timeout)
    print(f"Esperando respuestas durante {timeout} segundos...")
    
    start_time = time.time()
    while True:
        try:
            datos, direccion = sock.recvfrom(1024)
            respuesta = datos.decode('utf-8').strip()
            
            print(f"Respuesta recibida de {direccion[0]}:{direccion[1]}: '{respuesta}'")
            
            if respuesta == "AQUI ESTOY":
                servidores_encontrados.append(direccion[0])
                
                # Guardar la IP del primer servidor que responda
                if primer_servidor is None:
                    primer_servidor = direccion[0]
                    print(f"✓ Primer servidor encontrado: {primer_servidor}")
            
            # Verificar si el timeout ha expirado manualmente
            if time.time() - start_time > timeout:
                break
                
        except socket.timeout:
            print("Timeout alcanzado, no se esperan más respuestas")
            break
        except Exception as e:
            print(f"Error recibiendo respuestas: {e}")
            break
    
    # Mostrar resumen de servidores encontrados
    print(f"\n=== Resumen del Descubrimiento ===")
    print(f"Servidores encontrados: {len(servidores_encontrados)}")
    for i, ip in enumerate(servidores_encontrados, 1):
        print(f"  {i}. {ip}")
    
    # Paso 3 y 4: Si hay servidores, probar el servicio con el primero
    if primer_servidor:
        print(f"\n=== Probando Servicio con {primer_servidor} ===")
        
        try:
            # Enviar "HOLA" al primer servidor
            mensaje_hola = "HOLA"
            print(f"Enviando '{mensaje_hola}' a {primer_servidor}:{puerto_broadcast}")
            
            sock.settimeout(5.0)  # Timeout más largo para la comunicación directa
            sock.sendto(mensaje_hola.encode('utf-8'), (primer_servidor, puerto_broadcast))
            
            # Esperar respuesta
            datos, direccion = sock.recvfrom(1024)
            respuesta_servicio = datos.decode('utf-8')
            
            print(f"✓ Respuesta del servicio: '{respuesta_servicio}'")
            print(f"✓ Comunicación exitosa con el servidor {direccion[0]}")
            
        except socket.timeout:
            print("✗ Timeout esperando respuesta del servicio")
        except Exception as e:
            print(f"✗ Error comunicándose con el servidor: {e}")
    else:
        print("\n✗ No se encontraron servidores disponibles")
        print("Asegúrate de que hay al menos un servidor ejecutándose con:")
        print(f"  python3 udp_servidor6_broadcast.py {puerto_broadcast}")
    
    sock.close()
    print("\nCliente finalizado")

if __name__ == "__main__":
    main()