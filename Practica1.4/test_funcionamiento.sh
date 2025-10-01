#!/bin/bash

echo "=== Probando el funcionamiento de tcp_servidor4_oche_mejorado.py y tcp_cliente4_oche_mejorado.py ==="

# Cambiar al directorio correcto
cd /home/uo288967/IngenieriaServicios/Practica1.4

# Verificar que los archivos existen
if [ ! -f tcp_servidor4_oche_mejorado.py ]; then
    echo "ERROR: tcp_servidor4_oche_mejorado.py no existe"
    exit 1
fi

if [ ! -f tcp_cliente4_oche_mejorado.py ]; then
    echo "ERROR: tcp_cliente4_oche_mejorado.py no existe"
    exit 1
fi

echo "Archivos encontrados. Iniciando prueba..."

# Iniciar el servidor en segundo plano en puerto 9997
echo "Iniciando servidor en puerto 9997..."
python3 tcp_servidor4_oche_mejorado.py 9997 &
SERVER_PID=$!

# Esperar un poco para que el servidor se inicie
sleep 2

# Ejecutar el cliente
echo "Ejecutando cliente..."
python3 tcp_cliente4_oche_mejorado.py localhost 9997

# Terminar el servidor
echo "Terminando servidor..."
kill $SERVER_PID 2>/dev/null

echo "Prueba completada."