## 1. Fundamentos de Red y Seguridad

- [x] 1.1 Crear archivo `secrets.py` con estructura para SSID, Password e IP estática/DHCP.
- [x] 1.2 Implementar el módulo `wifi_manager.py` con la función `connect()` que maneje timeout y reintentos.

## 2. Integración y Automatización

- [x] 2.1 Modificar `boot.py` para importar `wifi_manager` e intentar la conexión al encender la placa.
- [x] 2.2 Asegurar que el fallo en la conexión no detenga la ejecución de la placa (manejo de excepciones).

## 3. Pruebas de Sistema

- [x] 3.1 Crear script `test_wifi.py` para realizar una petición HTTP a un servidor público (ej. google.com o micropython.org) y mostrar el resultado.
- [x] 3.2 Verificar que el Rover mantiene la IP asignada (sea DHCP o estática).
