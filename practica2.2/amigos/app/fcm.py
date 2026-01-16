import firebase_admin
from firebase_admin import credentials, messaging
import os

# Buscamos el archivo JSON en la misma carpeta donde está este script (app/)
cred_path = os.path.join(os.path.dirname(__file__), "serviceAccount.json")
cred_object = None

try:
    if os.path.exists(cred_path):
        cred_object = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred_object)
        print(f"FCM: Inicializado correctamente con {cred_path}")
    else:
        print(f"FCM Error: No se encuentra el archivo {cred_path}")
except Exception as e:
    print(f"FCM Error al inicializar: {e}")
    cred_object = None

def notificar_amigos(tokens, body):
    """
    Envía una notificación a una lista de tokens.
    """
    # Si no hay credenciales o la lista está vacía, no hacemos nada
    if not cred_object:
        print("FCM Warning: No hay credenciales, no se envía nada.")
        return
    if not tokens:
        print("FCM Info: Lista de tokens vacía.")
        return

    try:
        # Creamos el payload de la notificación
        notification = messaging.Notification(
            title="Amigos",
            body=body
        )
        
        # Preparamos el mensaje multicast
        message = messaging.MulticastMessage(
            notification=notification,
            tokens=tokens
        )
        
        # Enviamos
        response = messaging.send_each_for_multicast(message)
        print(f"FCM: Envio exitoso. {response.success_count} mensajes enviados.")
        
        if response.failure_count > 0:
            print(f"FCM Warning: {response.failure_count} mensajes fallaron.")
            
    except Exception as e:
        print(f"FCM Error al enviar notificación: {e}")
