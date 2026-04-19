import wifi_manager

print("--- Iniciando secuencia de arranque ---")

try:
    wifi_manager.connect()
except Exception as e:
    print("Error al conectar WiFi al arrancar:", e)
    print("Continuando sin conexión...")
