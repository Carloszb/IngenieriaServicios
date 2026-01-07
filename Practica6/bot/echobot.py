# coding: utf-8
import sys
import logging
import ssl
from getpass import getpass
from slixmpp import ClientXMPP

class MiBot(ClientXMPP):
    def __init__(self, jid, clave):
        # --- Constructor (Sección 5.2.2) ---
        super().__init__(jid, clave)

        # --- Registro de eventos (Sección 5.2.3) ---
        self.add_event_handler("session_start", self.callback_para_session_start)
        self.add_event_handler("message", self.callback_para_message)

        # --- Ejercicio 8: Registro de eventos de estado de chat (XEP-0085) ---
        self.add_event_handler("chatstate_active", self.on_active)
        self.add_event_handler("chatstate_composing", self.on_composing)
        self.add_event_handler("chatstate_paused", self.on_paused)
        self.add_event_handler("chatstate_inactive", self.on_inactive)

    async def callback_para_session_start(self, evento):
        # --- Callback de inicio (Sección 5.2.4) ---
        print("Bot conectado. Enviando presencia...")
        self.send_presence()
        await self.get_roster()

    async def callback_para_message(self, evento):
        # --- Callback de mensajes (Modificado para Ejercicio 9) ---
        if evento['type'] in ('chat', 'normal'):
            cuerpo = evento['body']
            remitente = evento['from']
            
            # Verificar que el mensaje tenga contenido
            if cuerpo:
                print(f"Mensaje recibido de {remitente}: {cuerpo}")
                
                # --- Ejercicio 9: Lógica de calculadora ---
                if cuerpo.startswith("="):
                    # Extraer la expresión (quitando el '=')
                    expresion = cuerpo[1:]
                    try:
                        # ADVERTENCIA: eval() es peligroso en producción, 
                        # pero aceptable para este ejercicio práctico.
                        resultado = str(eval(expresion))
                        cuerpo_respuesta = f"Resultado: {resultado}"
                    except Exception as e:
                        cuerpo_respuesta = f"Error al calcular: {e}"
                else:
                    # Comportamiento anterior (Eco)
                    cuerpo_respuesta = "¿%s?" % cuerpo
                
                # --- Sección 5.2.6: Respondiendo al remitente manualmente ---
                msg = self.Message()           # Crear mensaje vacío
                msg["to"] = remitente          # Asignar destinatario
                msg["type"] = "chat"           # Tipo de mensaje
                msg["body"] = cuerpo_respuesta # El cuerpo calculado o el eco
                
                # --- Corrección para mantener chatstates en Pidgin ---
                msg["chat_state"] = "active"   # Indicamos que estamos activos
                
                msg.send()                     # Envío
                
                print(f"Respuesta enviada: {cuerpo_respuesta}")

    # --- Ejercicio 8: Callbacks para estados de chat ---
    
    async def on_active(self, evento):
        print(f"{evento['from'].bare} está activo")

    async def on_composing(self, evento):
        print(f"{evento['from'].bare} está escribiendo...")

    async def on_paused(self, evento):
        print(f"{evento['from'].bare} ha parado de escribir")

    async def on_inactive(self, evento):
        print(f"{evento['from'].bare} está inactivo")


# --- Programa Principal (Sección 5.2.5) ---
if __name__ == '__main__':
    # Configuración de logs
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)-8s %(message)s')

    print("--- Configuración del Bot ---")
    
    # 1. Obtener credenciales
    jid = input("Introduce el JID del bot (ej: bot@ingserv02): ")
    clave = getpass("Introduce la contraseña del bot: ")
    ip_servidor = input("Introduce la IP del servidor (o 'localhost'): ")

    # 2. Instanciar el cliente
    bot = MiBot(jid, clave)

    # 3. Configurar SSL (Contexto personalizado)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    bot.ssl_context = ssl_context

    # Registrar plugins
    bot.register_plugin('xep_0030') # Service Discovery
    bot.register_plugin('xep_0085') # Chat States

    # 4. Conectar al servidor
    print(f"Conectando a {ip_servidor} en el puerto 5222...")
    if ip_servidor:
        bot.connect((ip_servidor, 5222))
    else:
        bot.connect()

    # 5. Iniciar el bucle de eventos
    print("Bot iniciado. Presiona Ctrl+C para salir.")
    try:
        bot.process(forever=True)
    except KeyboardInterrupt:
        print("\nDeteniendo el bot...")
        bot.disconnect()
