# Ejercicio 4 - TCP Cliente y Servidor Mejorados

## Descripción

Este ejercicio implementa una función `recibe_mensaje()` que retorna líneas completas leídas del socket mediante la técnica de leer los bytes de uno en uno y concatenarlos hasta tener una línea completa.

## Archivos

- **tcp_servidor4_oche_mejorado.py**: Servidor TCP mejorado con la función `recibe_mensaje()`
- **tcp_cliente4_oche_mejorado.py**: Cliente TCP mejorado con la función `recibe_mensaje()`

## Función recibe_mensaje()

La función lee byte a byte del socket hasta encontrar el terminador de línea `\r\n`:

```python
def recibe_mensaje(socket_cliente):
    """
    Recibe un mensaje completo del socket leyendo byte a byte
    hasta encontrar una línea completa (terminada en \r\n).
    """
    mensaje = ""
    
    try:
        while True:
            # Leer un byte a la vez
            byte = socket_cliente.recv(1)
            
            # Si no se recibe nada, el cliente cerró la conexión
            if not byte:
                return None
                
            # Convertir byte a carácter
            try:
                char = byte.decode('utf-8')
            except UnicodeDecodeError:
                # Si hay error de decodificación, ignorar este byte
                continue
                
            # Añadir el carácter al mensaje
            mensaje += char
            
            # Verificar si hemos recibido una línea completa (\r\n)
            if mensaje.endswith('\r\n'):
                # Retornar la línea sin el \r\n
                return mensaje[:-2]
                
    except socket.error as e:
        print(f"Error al recibir mensaje: {e}")
        return None
```

## Características

1. **Lectura byte a byte**: Lee exactamente un byte cada vez usando `recv(1)`
2. **Concatenación hasta línea completa**: Acumula los caracteres hasta encontrar `\r\n`
3. **Manejo robusto de errores**: Detecta cuando el otro extremo cierra la conexión
4. **Decodificación segura**: Maneja errores de decodificación UTF-8
5. **Retorna líneas limpias**: Devuelve la línea sin el terminador `\r\n`

## Cómo ejecutar

### Prueba básica

Terminal 1 (Servidor):
```bash
python3 tcp_servidor4_oche_mejorado.py
```

Terminal 2 (Cliente):
```bash
python3 tcp_cliente4_oche_mejorado.py
```

### Prueba con puerto personalizado

Terminal 1 (Servidor):
```bash
python3 tcp_servidor4_oche_mejorado.py 8888
```

Terminal 2 (Cliente):
```bash
python3 tcp_cliente4_oche_mejorado.py localhost 8888
```

## Prueba de acumulación de mensajes

Para probar que la función maneja correctamente la acumulación de varios mensajes en el buffer del socket, se puede añadir un `time.sleep(1)` en el servidor después del `accept()`:

1. Editar `tcp_servidor4_oche_mejorado.py` y añadir al inicio:
   ```python
   import time
   ```

2. Después de la línea `print("Nuevo cliente conectado desde %s:%d" % origen)`, añadir:
   ```python
   time.sleep(1)  # Simular retardo para acumular mensajes
   ```

3. Ejecutar el servidor y cliente como se indica arriba.

El cliente enviará todos sus mensajes rápidamente, pero el servidor los procesará después del sleep. A pesar de que múltiples mensajes se acumulan en el buffer, la función `recibe_mensaje()` los procesará correctamente uno por uno.

## Ejemplo de salida

### Servidor:
```
No se especificó puerto. Usando puerto por defecto: 9999
Servidor listo y escuchando...

Esperando un cliente...
Nuevo cliente conectado desde 127.0.0.1:37006
Recibido: 'HOLA MUNDO!'. Enviando: '!ODNUM ALOH'
Recibido: 'PYTHON ES GENIAL.'. Enviando: '.LAINEG SE NOHTYP'
Recibido: '1234567890'. Enviando: '0987654321'
Recibido: 'FINALIZAR'. Enviando: 'RAZILANIF'
Conexión cerrada por el cliente.
```

### Cliente:
```
Usando por defecto: localhost:9999

Intentando conectar a localhost:9999...
Conexión exitosa.
CLIENTE: Enviado: 'HOLA MUNDO!'
CLIENTE: Recibido (invertido): '!ODNUM ALOH'
CLIENTE: Enviado: 'PYTHON ES GENIAL.'
CLIENTE: Recibido (invertido): '.LAINEG SE NOHTYP'
CLIENTE: Enviado: '1234567890'
CLIENTE: Recibido (invertido): '0987654321'
CLIENTE: Enviado: 'FINALIZAR'
CLIENTE: Recibido (invertido): 'RAZILANIF'

CLIENTE: Cerrando conexión.
```

## Ventajas de esta implementación

1. **Robustez**: No depende de `recv(n)` que puede recibir menos bytes de los solicitados
2. **Precisión**: Lee exactamente hasta encontrar el terminador de línea
3. **Manejo de mensajes largos**: No hay límite de tamaño del buffer
4. **Manejo de mensajes acumulados**: Procesa correctamente mensajes que se acumulan en el buffer
