import socket

# Dominio al que nos conectaremos
host = "www.wikipedia.org"
puerto = 80
recurso = "/"

print(f"Resolviendo {host}...\n")

# Obtener información de conexión (IPv4 e IPv6)
info = socket.getaddrinfo(host, puerto, proto=socket.IPPROTO_TCP)

for datos in info:
    familia, tipo, proto, canonico, direccion = datos
    print(f"Intentando conectar con {direccion}...")

    try:
        # Crear socket
        s = socket.socket(familia, tipo, proto)
        s.connect(direccion)

        # Construir y enviar la petición HTTP GET
        peticion = f"GET {recurso} HTTP/1.0\r\nHost: {host}\r\n\r\n"
        s.sendall(peticion.encode())

        # Recibir respuesta
        respuesta = b""
        while True:
            parte = s.recv(4096)
            if not parte:
                break
            respuesta += parte

        print("\n--- Respuesta del servidor ---\n")
        print(respuesta.decode(errors="ignore"))

        s.close()
        break  # salir después de una conexión exitosa

    except Exception as e:
        print(f"Error al conectar con {direccion}: {e}\n")
