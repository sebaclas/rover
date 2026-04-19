## Why

El Rover necesita conectividad a internet para permitir el control remoto y la transmision de datos. EL Rover tendrá 2 ESP, la principal que leerá sensores y actuadores y la la de la cámara. Ambas ESP necesitan conexion a Internet. Ahora implementamos la conexion a la ESP principal. Configurar una conexión automática y robusta es fundamental para la autonomía del sistema.

## What Changes

- Creación de un archivo de configuración de credenciales (`secrets.py`) para separar la seguridad del código lógico.
- Implementación de un módulo de gestión de red (`wifi.py`) para manejar la conexión, reconexión y estados de red.
- Modificación del arranque del sistema (`boot.py`) para iniciar la conexión WiFi de forma automática.
- Implementación de una prueba de conectividad básica.

## Capabilities

### New Capabilities
- `wifi-connectivity`: Proporciona una interfaz para conectar la placa a una red WiFi, manejar timeouts y verificar el estado de la conexión.
- `secrets-management`: Estructura para almacenar de forma segura (y ocultar de git en el futuro) las credenciales de red.

### Modified Capabilities
- `boot-sequence`: El proceso de arranque ahora incluirá la inicialización de la red como paso prioritario.

## Impact

- **Código**: Afecta a `boot.py` y requiere la creación de nuevos archivos `.py`.
- **Seguridad**: Introduce el manejo de credenciales (SSID/PWD).
- **Consumo**: El uso de WiFi incrementará el consumo de energía de la placa.
