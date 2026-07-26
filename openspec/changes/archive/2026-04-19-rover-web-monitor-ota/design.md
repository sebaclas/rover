## Context

El proyecto Rover ESP32-S3 se encuentra en una fase donde la interacción física (cable USB) ralentiza la experimentación. Se requiere una solución inalámbrica para monitorear el sonar y controlar el movimiento. La placa ya cuenta con conexión WiFi funcional configurada en `wifi_manager.py`.

## Goals / Non-Goals

**Goals:**
- Implementar un servidor web asíncrono que no bloquee la lectura de sensores.
- Proveer telemetría de sonar con latencia de sub-segundo.
- Permitir el control de movimiento desde navegadores PC y móviles.
- Facilitar la actualización del código sin cables (OTA).

**Non-Goals:**
- No se implementará streaming de video en este cambio (delegado a la unidad ESP32-CAM).
- No se implementará persistencia de logs en flash (solo memoria volátil del dashboard).
- No se implementará control por joystick analógico (solo digital/teclado).

## Decisions

### 1. Servidor Web Asíncrono: Microdot
Se utilizará la librería **Microdot** debido a su soporte nativo para `uasyncio`. Esto permite que el bucle principal siga leyendo el sonar y controlando motores mientras se atienden peticiones HTTP.
- *Alternativa*: Sockets crudos (demasiado complejo de mantener) o TinyWeb (menos documentado).

### 2. Protocolo de Telemetría: WebSockets
Para la actualización continua de la distancia del sonar, se usarán WebSockets. Esto evita el overhead de múltiples peticiones HTTP GET y permite una respuesta inmediata ante obstáculos.
- *Alternativa*: HTTP Polling (lento y pesado para el MCU).

### 3. Abstracción de Hardware: Clase `Rover`
Se creará un módulo `rover.py` que encapsule el sonar y los motores. Esto facilita las pruebas y hace que `main.py` sea solo pegamento de lógica.

### 4. Sistema OTA: Script Custom (`ota.py`)
Dado que el proyecto es pequeño, un script que descargue archivos de una URL de GitHub Raw es suficiente. Se comparará un `version.json` local vs remoto.
- *Alternativa*: Senko (librería externa, pero un script custom nos da más control sobre qué archivos actualizar).

### 5. UI Embebida
La interfaz web (HTML, CSS, JS) se guardará como un string en un archivo o se leerá de un único archivo `index.html` para simplificar el manejo de rutas en Microdot.

## Risks / Trade-offs

- **[Riesgo] Interferencia WiFi/Motores** -> Los motores DC pueden generar ruido eléctrico que afecte al WiFi. *Mitigación*: Uso de capacitores de desacoplo y rutas de alimentación separadas (hardware) y re-conexión automática en software.
- **[Riesgo] OTA Fallido** -> Si se corta la conexión durante la descarga, el archivo puede quedar corrupto. *Mitigación*: Descargar a un archivo temporal `.new` y renombrar solo si la descarga es completa.
- **[Trade-off] Consumo de RAM** -> Mantener el servidor y WebSockets consume memoria. *Mitigación*: Limitar el número de clientes concurrentes a 1 o 2.
