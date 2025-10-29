import getpass
import telnetlib

HOST = "10.38.10.100"
user = input("Enter your remote account: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)

tn.read_until(b"login: ")
tn.write(user.encode('utf-8') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('utf-8') + b"\n")

# Esperar hasta que aparezca el prompt del shell ($), descartando el mensaje de bienvenida
tn.read_until(b"$")

# Ejecutar el comando y leer su salida
tn.write(b"ls -la /home\n")
output = tn.read_until(b"$").decode('utf-8', errors='replace')

tn.write(b"exit\n")

print(output)
