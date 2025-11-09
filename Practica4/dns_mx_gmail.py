import dns.resolver

# Dominio al que consultaremos los registros MX
dominio = "gmail.com"

print(f"Servidores MX para el dominio {dominio}:\n")

# Consulta de tipo MX
respuesta_mx = dns.resolver.resolve(dominio, "MX")

# Crear una lista con los resultados (preferencia, exchange)
mx_registros = []
for rdata in respuesta_mx:
    prioridad = rdata.preference
    servidor = str(rdata.exchange)
    mx_registros.append((prioridad, servidor))

# Ordenar por prioridad
mx_registros.sort(key=lambda x: x[0])

# Para cada servidor MX, obtener su IP (registro A)
for prioridad, servidor in mx_registros:
    try:
        respuesta_a = dns.resolver.resolve(servidor, "A")
        for ip in respuesta_a:
            print(f"{prioridad}\t{servidor}\t{ip.address}")
    except Exception as e:
        print(f"{prioridad}\t{servidor}\t❌ No se pudo resolver IP ({e})")
