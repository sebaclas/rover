# Convenciones y Calibración del IMU (MPU-6050)

Este documento define la orientación espacial, los sistemas de coordenadas y el comportamiento físico de las lecturas del acelerómetro y giroscopio **MPU-6050** integrado en el Rover.

---

## 1. Sistema de Coordenadas de Referencia

El sensor MPU-6050 está montado sobre la placa del rover configurando un **Sistema de Coordenadas Dextrógiro (Right-Handed Coordinate System)** alineado con el chasis del rover de la siguiente manera:

*   **Eje X (+X)**: Apunta hacia **Adelante** (hacia la trompa del rover). Lápiz de color verde en la interfaz web.
*   **Eje Y (+Y)**: Apunta hacia la **Izquierda** del rover. Lápiz de color rojo en la interfaz web.
*   **Eje Z (+Z)**: Apunta hacia **Arriba** (perpendicular a la superficie superior del rover).

```mermaid
%% Ejes del Rover visto desde arriba
graph TD
    subgraph Orientación del Rover (Vista Superior)
        Trompa[▲ Adelante / Trompa (+X)] --- Centro((Centro IMU))
        Izquierda[◀ Izquierda (+Y)] --- Centro
        Centro --- Derecha[Derecha (-Y)]
        Centro --- Cola[▼ Atrás / Cola (-X)]
        Centro -.-> Arriba((Arriba / +Z hacia afuera))
    end
```

---

## 2. Convenciones de Rotación (Regla de la Mano Derecha)

Siguiendo la regla de la mano derecha (apuntando el pulgar en el sentido positivo del eje y cerrando la mano para ver la rotación positiva):

| Movimiento | Eje de Rotación | Signo Positivo (+) | Signo Negativo (-) |
| :--- | :---: | :--- | :--- |
| **Pitch** (Cabeceo) | **Eje Y** | **Nose Up** (Levanta la trompa / se inclina hacia atrás) | **Nose Down** (Baja la trompa / se inclina hacia adelante) |
| **Roll** (Alabeo) | **Eje X** | **Inclinación Izquierda** (El lateral derecho sube, el izquierdo baja) | **Inclinación Derecha** (El lateral izquierdo sube, el derecho baja) |
| **Yaw** (Guiñada) | **Eje Z** | **Giro Antihorario (CCW)** (Rotación a la izquierda) | **Giro Horario (CW)** (Rotación a la derecha) |

### Confirmación de tus Observaciones:
1.  **Rotación Y positiva**: Levanta la trompa (Nose Up). **Correcto**.
2.  **Rotación X negativa**: El rover se inclina a la derecha / lateral izquierdo sube (Roll negativo). **Correcto**.
3.  **Rotación Z negativa**: El rover gira a la derecha (Yaw negativo / sentido de las agujas del reloj). **Correcto**.

---

## 3. Comportamiento del Acelerómetro

El acelerómetro mide la **aceleración propia** (la fuerza que experimenta la masa inercial de prueba respecto a la caída libre). 

### Estado Estático (En reposo en una superficie plana)
*   **Aceleración en Z ($a_z$)**: Mide **$\approx +0.98g$ a $+1.0g$** (positivo). Esto es correcto, ya que representa la fuerza normal ascendente ejercida por la superficie para contrarrestar la gravedad terrestre.
*   **Aceleración en X ($a_x$)** e **Y ($a_y$)**: Miden **$\approx 0.0g$** (pequeñas desviaciones debido a la calibración de montaje).

### Efecto de la Gravedad al Inclinarse (Pitch/Roll)
Cuando el rover se inclina, la gravedad terrestre proyecta una componente sobre los ejes X e Y:
*   **Inclinación hacia atrás (Trompa arriba / Pitch positivo)**: La gravedad tira de la masa hacia atrás. La fuerza de reacción que mide el acelerómetro en el eje X es hacia adelante, resultando en un valor de **$a_x$ negativo**.
    *   *Fórmula del Dashboard:* `let pitch = Math.atan2(-ax, ...)` -> Dado que $a_x$ es negativo, el pitch resultante en la pantalla es positivo.
*   **Inclinación hacia adelante (Trompa abajo / Pitch negativo)**: La gravedad tira de la masa hacia adelante. El acelerómetro mide un valor de **$a_x$ positivo**.

### Comportamiento Dinámico al Acelerar hacia Adelante
Cuando el rover acelera hacia adelante físicamente por acción de sus motores (o al empujarlo de forma manual):

1.  **Chasis Squat (Efecto Suspensión/Torque)**: Al arrancar hacia adelante, la fuerza del motor genera un torque que tiende a levantar levemente la parte frontal del rover (efecto "cabeceo" o levantar la trompa). Como vimos antes, levantar la trompa (Pitch positivo) proyecta la gravedad hacia atrás sobre el eje X, generando de inmediato una lectura de **$a_x$ negativa** de gran magnitud relativa (la gravedad de $9.8 \text{ m/s}^2$ domina rápidamente la señal).
2.  **Inercia de Empuje y Parada**: 
    *   Al empujar el rover hacia adelante para acelerarlo, la masa interna se va hacia atrás generando una fuerza positiva temporal.
    *   Sin embargo, al soltarlo o frenarlo (deceleración), la desaceleración es típicamente muy brusca y genera una fuerza inercial hacia adelante de gran magnitud, lo que se registra como un pico de **aceleración negativo** muy marcado.
    *   *Solución:* Para aislar la aceleración de movimiento puro del ruido y de la inclinación del chasis, se debe calibrar el sensor en reposo para eliminar el offset estático de montaje, y utilizar filtros (como un filtro de paso bajo o filtro complementario) para separar la gravedad de la aceleración lineal.

---

## 4. Notas de Calibración
El giroscopio suele tener un desfase (offset) de fábrica (por ejemplo, el eje Y puede registrar una rotación aparente de alrededor de $+9.3^\circ/\text{s}$ en reposo). 

> [!TIP]
> Para obtener mediciones de orientación estables en el dashboard, se implementará una rutina que tome una media de las primeras 100 lecturas en reposo al encender el rover para restar estos offsets fijos de las lecturas dinámicas.
