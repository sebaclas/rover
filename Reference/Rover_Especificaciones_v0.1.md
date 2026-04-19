**ROVER AUTÓNOMO**

Documento de Especificaciones Técnicas

*Versión: 0.1 --- BORRADOR*

Fecha: Abril 2025

Estado: En desarrollo

**1. Resumen del Proyecto**

Este documento describe las especificaciones técnicas del rover autónomo
basado en ESP32-S3, diseñado para exploración y navegación autónoma con
capacidades de detección de obstáculos, control de movimiento y
transmisión de video en tiempo real.

> *📝 Documento vivo: las especificaciones se irán completando a medida
> que se definan los componentes y decisiones de diseño.*

**2. Arquitectura General del Sistema**

El sistema se compone de dos unidades de procesamiento principales:

1.  Unidad Principal (ESP32-S3): control de motores, navegación y
    sensores.

2.  Unidad de Cámara (ESP32-CAM): captura y transmisión de video vía
    WiFi.

**3. Especificaciones de Componentes**

**3.1 Unidad de Control Principal**

**NodeMCU WiFi Bluetooth ESP32-S3 --- 44 Pines + Base Screwshield**

  -------------------------- --------------------------------------------------------------
  **Parámetro**              Valor
  **Modelo**                 NodeMCU ESP32-S3
  **Pines**                  44 pines GPIO
  **Base**                   Screwshield (conexión por tornillo)
  **Firmware / Runtime**     MicroPython
  **Conectividad**           WiFi 802.11 b/g/n + Bluetooth 5.0 (LE)
  **Procesador**             Xtensa LX7 dual-core (hasta 240 MHz)
  **Memoria Flash**          Por definir según variante
  **PSRAM**                  Por definir según variante
  **Interfaces**             I2C, SPI, UART, PWM, ADC, DAC
  **Tensión de operación**   3.3 V (alimentación 5 V via USB o VIN)
  **Notas**                  La screwshield facilita conexiones robustas para prototipado
  -------------------------- --------------------------------------------------------------

> *📝 Decisión: se utilizará MicroPython como entorno de desarrollo
> principal para facilitar la iteración rápida.*

**3.2 Controlador PWM / Servos**

**PCA9685 --- Controlador 16 Canales I2C PWM**

  ---------------------------- -------------------------------------------------
  **Parámetro**                Valor
  **Modelo**                   PCA9685
  **Interfaz con MCU**         I2C
  **Canales PWM**              16 canales independientes
  **Resolución PWM**           12 bits (4096 pasos)
  **Frecuencia PWM**           24 Hz -- 1526 Hz (ajustable)
  **Tensión de lógica**        3.3 V / 5 V compatible
  **Tensión de servos (V+)**   Alimentación externa recomendada
  **Dirección I2C base**       0x40 (configurable via pines A0--A5)
  **Uso en el proyecto**       Control de motores de tracción y servo de sonar
  **Librería MicroPython**     Por definir
  ---------------------------- -------------------------------------------------

> *📝 Decisión: el PCA9685 libera los pines PWM del ESP32-S3 y permite
> controlar múltiples actuadores desde un solo bus I2C.*

**3.3 Sensor de Distancia**

**HC-SR04 --- Sensor Ultrasónico**

  -------------------------- -----------------------------------------------------------------------------
  **Parámetro**              Valor
  **Modelo**                 HC-SR04
  **Tecnología**             Ultrasonido
  **Rango de medición**      2 cm -- 400 cm
  **Resolución**             \~0.3 cm
  **Ángulo de detección**    \~15°
  **Tensión de operación**   5 V (Trigger y Echo --- ver nota)
  **Corriente**              \~15 mA
  **Pines**                  VCC, GND, Trigger, Echo
  **Montaje**                Sobre servo rotativo (ver sección 3.4)
  **Interfaz MCU**           GPIO (Trigger: salida, Echo: entrada con divisor de tensión o nivel lógico)
  -------------------------- -----------------------------------------------------------------------------

> *📝 Atención: el ESP32-S3 opera a 3.3 V. El pin Echo del HC-SR04
> entrega 5 V --- se requiere divisor de tensión o módulo con level
> shifter para proteger el GPIO.*

![ESP32-S3 con HC-SR04
conectado](fotos/sonar_esp32_v01.jpg){width="3.0in"
height="4.5007874015748035in"}

*Foto 1: ESP32-S3 en screwshield con HC-SR04 conectado (pines GPIO 9 y
10)*

**3.4 Servo de Orientación del Sonar**

  ------------------- ----------------------------------------------------
  **Parámetro**       Valor
  **Función**         Rotar el sensor HC-SR04 para barrido lateral
  **Tipo**            Micro servo
  **Rango de giro**   ±90° respecto al eje frontal (180° total)
  **Control**         Canal PWM del PCA9685 (Rango Extendido: 0.5 a 2.5ms)
  **Montaje**         Solidario al chasis, HC-SR04 fijo al eje del servo
  **Modelo servo**    SG90
  ------------------- ----------------------------------------------------

> *📝 Decisión: el servo de sonar se controla desde el PCA9685, evitando
> usar pines PWM directos del ESP32-S3.*

**3.5 Unidad de Cámara**

**ESP32-CAM --- Módulo WiFi/BT con Cámara OV2640 2MP**

  -------------------------------- -------------------------------------------------------
  **Parámetro**                    Valor
  **Modelo**                       ESP32-CAM (AI-Thinker o compatible)
  **MCU integrado**                ESP32 dual-core
  **Sensor de imagen**             OV2640 2MP
  **Resolución máxima**            1600 × 1200 (UXGA)
  **Modos de resolución**          QQVGA a UXGA
  **Formato de salida**            JPEG, BMP, RAW
  **Conectividad**                 WiFi 802.11 b/g/n
  **Alimentación**                 5 V / 3.3 V (ver datasheet)
  **Flash LED integrado**          Sí (LED blanco)
  **Interfaz con MCU principal**   WiFi (streaming) / UART (por definir)
  **Firmware**                     Por definir (Arduino / ESP-IDF / MicroPython parcial)
  **Uso en el proyecto**           Streaming de video en tiempo real
  -------------------------------- -------------------------------------------------------

> *📝 Pendiente: definir protocolo de comunicación entre ESP32-S3 y
> ESP32-CAM (streaming HTTP/RTSP via WiFi o UART para comandos).*

**4. Decisiones de Diseño**

  ----------------------------- -------------------------------------------------------------------------------------
  **Decisión**                  Justificación
  **MicroPython en ESP32-S3**   Desarrollo ágil, sintaxis accesible, buenas librerías para I2C y PWM
  **PCA9685 vía I2C**           Libera pines del MCU, permite múltiples servos/motores con un bus
  **Sonar sobre servo**         Permite barrido angular de obstáculos sin multiplexar varios sensores
  **ESP32-CAM separado**        Delega el procesamiento de imagen a una unidad dedicada, no satura el MCU principal
  ----------------------------- -------------------------------------------------------------------------------------

**5. Pendientes y Próximos Pasos**

-   Definir sistema de tracción (motores DC, paso a paso, servos de
    rotación continua).

-   Resolver adaptación de niveles lógicos 5V/3.3V para HC-SR04.

-   Definir protocolo de comunicación ESP32-S3 ↔ ESP32-CAM.

-   Especificar sistema de alimentación (baterías, reguladores,
    distribución de potencia).

-   Definir chasis y estructura mecánica.

-   Agregar diagrama de bloques del sistema.

**6. Asignación de Pines del ESP32-S3**

  -------------- ---------------------- ------------------------------------- ---------------
  **Pin GPIO**   **Función**            **Componente**                        **Dirección**
  **GPIO 4**     SDA (I2C Datos)        Bus I2C (PCA9685, etc)                Bidireccional
  **GPIO 5**     SCL (I2C Reloj)        Bus I2C (PCA9685, etc)                Salida (OUT)
  **GPIO 9**     TRIG (trigger sonar)   HC-SR04 (sonar ultrasonico)           Salida (OUT)
  **GPIO 10**    ECHO (eco sonar)       HC-SR04 (sonar ultrasonico)           Entrada (IN)
  **GPIO 48**    LED RGB NeoPixel       NeoPixel integrado en placa (1 LED)   Salida (OUT)
  -------------- ---------------------- ------------------------------------- ---------------

**7. Historial de Revisiones**

  ---------------------- -----------------------------------------------------------------------------------------------------
  **Versión**            Descripción
  **0.1 --- Abr 2025**   Creación inicial. Componentes principales definidos: ESP32-S3, PCA9685, HC-SR04 + servo, ESP32-CAM.
  ---------------------- -----------------------------------------------------------------------------------------------------
