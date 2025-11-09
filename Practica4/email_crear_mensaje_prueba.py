import email.message
import email.policy
import email.utils

# Crear el mensaje principal
mensaje = email.message.EmailMessage()
mensaje['To'] = 'Desti Natario <destinatario@example.com>'
mensaje['From'] = 'Remi Tente <remitente@example.com>'
mensaje['Subject'] = 'Mensaje de prueba con adjunto'
mensaje['Date'] = email.utils.formatdate(localtime=True)
mensaje['Message-ID'] = email.utils.make_msgid()

# Cuerpo de texto
mensaje.set_content("Esto es una prueba con el logo ATC adjunto.\n\nSaludos.")

# Añadir adjunto (imagen logoatc.gif)
with open("logoatc.gif", "rb") as adjunto:
    contenido = adjunto.read()
    mensaje.add_attachment(contenido,
                           maintype='image',
                           subtype='gif',
                           filename='logoatc.gif')

# Mostrar el mensaje en formato MIME (texto completo)
binario = mensaje.as_bytes(policy=email.policy.default)
print(binario.decode("utf-8"))

