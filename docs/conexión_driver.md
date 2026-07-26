Así queda el flujo de señal: la ESP32 habla por I2C con el PCA9685, y este le entrega 4 señales PWM al DRV8833 para manejar ambos motores.

**Mapeo de pines exacto:**

| ESP32                | →   | PCA9685 |
| ----------------------| -----| ---------|
| 3.3V                 | →   | VCC     |
| GND                  | →   | GND     |
| GPIO21 (por defecto) | →   | SDA     |
| GPIO22 (por defecto) | →   | SCL     |

| PCA9685 | → | DRV8833 |
|---|---|---|
| CH0 | → | AIN1 |
| CH1 | → | AIN2 |
| CH2 | → | BIN1 |
| CH3 | → | BIN2 |

No necesitas conectar el pin **V+** del PCA9685 a nada: ese terminal solo distribuye alimentación a servos, no a las señales PWM en sí. Con VCC alimentado ya tenés las 16 salidas activas.

**Puntos críticos que no se ven en el diagrama pero son clave:**

1. **GND común obligatorio**: la ESP32, el PCA9685, el DRV8833 y la fuente de los motores tienen que compartir el mismo GND (referencia común). Si no, las señales de control no van a funcionar correctamente aunque todo esté "conectado".

2. **No alimentes los motores desde la ESP32**: el pin VM del DRV8833 debe ir a una fuente externa (batería o fuente de pared) acorde a tus motores, normalmente entre 4V y 10.8V. La ESP32 no puede entregar la corriente que consumen motores DC.

3. **Pin STBY**: si tu módulo DRV8833 trae ese pin expuesto, debe estar en HIGH (3.3V) para que el driver funcione; si está en LOW, los motores quedan en reposo. Muchas placas genéricas lo traen ya puenteado a VCC con una resistencia pull-up, pero conviene revisarlo con el multímetro o la serigrafía de tu placa puntual.

4. **Control de dirección y velocidad (modo IN/IN)**: con este esquema, cada motor usa dos canales PWM. Para girar en un sentido, PWMeas una entrada y dejás la otra en 0; para el sentido contrario, invertís cuál PWMeas. Con ambas en 0 el motor queda en "coast" (libre), y con ambas al 100% queda en frenado activo.

5. **Frecuencia del PCA9685**: por defecto suele configurarse a 50 Hz (pensado para servos). Para motores DC conviene subirla a algo como 1000-1500 Hz para evitar el zumbido audible del motor.


![Diagrama de cableado](assets/esp32_pca9685_drv8833_wiring.png)


```mermaid
graph TD
    %% Fuente de Alimentación
    subgraph Power["Fuente de Alimentación (5V)"]
        VCC_5V["+5V DC"]
        GND_PWR["GND"]
    end

    %% Módulo PCA9685
    subgraph PCA9685["PCA9685 (PWM Controller)"]
        PCA_PWM0["PWM Pin 0"]
        PCA_PWM1["PWM Pin 1"]
        PCA_PWM2["PWM Pin 2"]
        PCA_PWM3["PWM Pin 3"]
        PCA_VCC["VCC / V+ (5V)"]
        PCA_GND["GND"]
    end

    %% DRV8833
    subgraph DRV8833["Módulo DRV8833"]
        DRV_VM["VM (Power)"]
        DRV_GND1["GND"]
        DRV_GND2["GND"]
        DRV_STBY["STBY (Standby)"]
        
        DRV_AIN1["AIN1"]
        DRV_AIN2["AIN2"]
        DRV_BIN1["BIN1"]
        DRV_BIN2["BIN2"]
        
        DRV_AO1["AO1"]
        DRV_AO2["AO2"]
        DRV_BO1["BO1"]
        DRV_BO2["BO2"]
    end

    %% Motores DC
    subgraph Motors["Motores DC"]
        MotorA["Motor A"]
        MotorB["Motor B"]
    end

    %% Conexiones de Alimentación
    VCC_5V --> DRV_VM
    VCC_5V --> DRV_STBY
    VCC_5V --> PCA_VCC
    
    GND_PWR --> DRV_GND1
    GND_PWR --> PCA_GND

    %% Señales PCA9685 -> DRV8833
    PCA_PWM0 --> DRV_AIN1
    PCA_PWM1 --> DRV_AIN2
    PCA_PWM2 --> DRV_BIN1
    PCA_PWM3 --> DRV_BIN2

    %% Conexión hacia Motores
    DRV_AO1 --> MotorA
    DRV_AO2 --> MotorA
    DRV_BO1 --> MotorB
    DRV_BO2 --> MotorB
```