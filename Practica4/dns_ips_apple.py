import dns.resolver

dominio = 'apple.com'
respuesta = dns.resolver.resolve(dominio, 'A')

print(f"Direcciones IP asociadas a {dominio}:\n")
for ip in respuesta:
    print(ip.address)

print("\nRespuesta completa del servidor DNS:\n")
print(respuesta.response)
