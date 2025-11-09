import dns.resolver

respuesta = dns.resolver.resolve('en.wikipedia.org')
print(respuesta[0].address)
print(respuesta.response)
print(respuesta.response.to_wire())
