# Guía de Conexión, Desarrollo y Despliegue (MicroPython)

Este documento contiene los pasos necesarios para conectar la placa ESP32-S3 a tu ordenador, activar el entorno de desarrollo y transferir código utilizando la consola.

---

## 1. Activar el Entorno Virtual (`.venv`)

El proyecto cuenta con un entorno virtual local donde están instaladas las dependencias de desarrollo (como `mpremote`). Dependiendo de la consola que uses en VS Code, ejecuta uno de los siguientes comandos para activarlo:

* **Si usas PowerShell** (terminal por defecto en Windows):
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
* **Si usas Command Prompt (CMD)**:
  ```cmd
  .venv\Scripts\activate.bat
  ```
* **Si usas Git Bash**:
  ```bash
  source .venv/Scripts/activate
  ```

Una vez activado, verás el prefijo `(.venv)` en tu terminal. Si por algún motivo necesitas reinstalar la herramienta principal de comunicación, ejecuta:
```bash
pip install mpremote
```

---

## 2. Conectar la Placa y Detectar el Puerto COM

1. Conecta la placa ESP32-S3 a tu PC mediante un puerto USB. Asegúrate de usar un cable que soporte **transferencia de datos** (no solo carga).
2. Para identificar el puerto asignado por Windows:
   * Haz clic derecho en el botón de Inicio de Windows y abre el **Administrador de dispositivos**.
   * Despliega la sección **Puertos (COM y LPT)**.
   * Identifica el puerto COM correspondiente a tu placa (por ejemplo, `COM7`).

---

## 3. Acceder a la Consola en Vivo (REPL)

La consola interactiva (REPL) te permite ver los mensajes de diagnóstico de la placa (`print`), depurar errores en tiempo real y ejecutar código MicroPython al vuelo.

Para conectarte:
```bash
mpremote connect COM7 repl
```
*(Reemplaza `COM7` por tu puerto si este llegara a cambiar).*

### Atajos útiles en el REPL:
* **`Ctrl + C`**: Interrumpe la ejecución del programa que está corriendo actualmente en la placa.
* **`Ctrl + D`**: Realiza un reinicio rápido por software (*Soft Reset*). Esto vuelve a cargar y ejecutar [main.py](main.py).
* **`Ctrl + ]`** (o `Ctrl + Alt + ]` / `Ctrl + 5` dependiendo de la distribución de tu teclado): Sale del entorno REPL y vuelve a la terminal de tu PC.

---

## 4. Subir Código a la Placa

Para subir archivos locales a la memoria interna de la ESP32, puedes usar el comando `cp` de `mpremote`. El símbolo `:` al final de los comandos representa la raíz del sistema de archivos de la placa.

* **Subir un archivo individual** (por ejemplo, [main.py](main.py)):
  ```bash
  mpremote connect COM7 cp main.py :main.py
  ```

* **Comandos para subir los archivos principales del proyecto**:
  ```bash
  mpremote connect COM7 cp main.py :
  mpremote connect COM7 cp wifi_manager.py :
  mpremote connect COM7 cp web_monitor.py :
  mpremote connect COM7 cp secrets.py :
  mpremote connect COM7 cp rover.py :
  mpremote connect COM7 cp index.html :
  ```
