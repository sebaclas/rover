## Context

El ESP32-S3 no tiene actualmente una configuración de red persistente. Para que el Rover sea funcional, debe conectarse a una red local al arrancar. Actualmente, el proyecto utiliza MicroPython en su versión v1.27.0.

## Goals / Non-Goals

**Goals:**
- Proporcionar conectividad automática al router WiFi local.
- Separar las credenciales (SSID/Password) del código fuente principal.
- Implementar un manejo de errores básico (reintentos ante fallas de conexión).
- Permitir la configuración de IP estática opcional para facilitar el acceso remoto.

**Non-Goals:**
- No se implementará un Portal Cautivo (WiFi Manager con AP) en esta fase inicial.
- No se implementará soporte para múltiples redes WiFi (solo una red principal).
- No se implementará comunicación segura (SSL/TLS) en esta etapa.

## Decisions

### 1. Almacenamiento de Credenciales (`secrets.py`)
**Decisión:** Usar un archivo Python simple con un diccionario.
**Razón:** Es el estándar en MicroPython. Permite importar las variables directamente (`from secrets import secrets`) y es más ligero que parsear JSON o .env en el chip.
**Alternativa:** Almacenar en un .txt o .json, pero requiere más código de parsing.

### 2. Lógica de Conexión en `boot.py`
**Decisión:** Invocar la conexión en `boot.py`.
**Razón:** Asegura que la red esté disponible antes de que `main.py` (la lógica del Rover) empiece a ejecutarse. Facilita la depuración desde el REPL ya que la placa estará conectada apenas el usuario vea el prompt `>>>`.

### 3. Configuración de Red (DHCP vs Estática)
**Decisión:** Implementar ambas opciones en `secrets.py`. Si se proveen datos de IP, se usa `ifconfig()`.
**Razón:** La flexibilidad permite al usuario elegir según su infraestructura de red local.

## Risks / Trade-offs

| Riesgo | Mitigación |
| :--- | :--- |
| **Bloqueo de arranque** | La función de conexión tendrá un timeout (ej. 10s). Si falla, el sistema continuará con `main.py` para no "brickear" la placa en un bucle infinito si el WiFi está apagado. |
| **Exposición de credenciales** | Se debe advertir al usuario no compartir el archivo `secrets.py`. |
| **Consumo de energía** | El WiFi estará activo permanentemente; esto es aceptable para un prototipo alimentado por batería o USB. |
