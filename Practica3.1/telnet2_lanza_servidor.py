import telnetlib
import time

HOST = "10.38.10.100"
user = "uo288967"
password = "Amefer03."

tn = telnetlib.Telnet(HOST)

tn.read_until(b"login: ")
tn.write(user.encode('utf-8') + b"\n")
tn.read_until(b"Password: ")
tn.write(password.encode('utf-8') + b"\n")

# Espera hasta que aparezca el prompt del shell remoto ($)
tn.read_until(b"$")

# Envía el comando ps -ef
tn.write(b"ps -ef\n")

# Usa read_until() para esperar al próximo prompt y capturar la salida completa
respuesta = tn.read_until(b"$").decode('utf-8', errors='replace')

# Comprueba si la salida contiene el nombre del servidor UDP
if "udp_servidor3_con_ok.py" in respuesta:
    print("El servidor ya está en ejecución.")
else:
    print("El servidor no está en ejecución. Lanzando servidor...")
    # Envía el comando para lanzarlo en background con nohup
    tn.write(b"nohup python3 udp_servidor3_con_ok.py &\n")
    # Espera a que aparezca el prompt otra vez
    tn.read_until(b"$")
    print("Servidor lanzado correctamente.")

    # 7️⃣ Espera un segundo para dar tiempo a que el servidor arranque
    time.sleep(1)

# 8️⃣ Envía el comando exit para cerrar el shell remoto
tn.write(b"exit\n")

# 9️⃣ Recoge la respuesta final del servidor con read_all() y muéstrala
salida_final = tn.read_all().decode('utf-8', errors='replace')
print("=== Respuesta completa del servidor ===")
print(salida_final)
