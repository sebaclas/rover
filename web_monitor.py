from microdot_asyncio import Microdot, send_file
from microdot_websocket import with_websocket
import uasyncio as asyncio
import json
import time

app = Microdot()
rover_instance = None

@app.route('/')
async def index(request):
    return send_file('index.html')

@app.route('/ws')
@with_websocket
async def telemetry(request, ws):
    print("Cliente WebSocket conectado")
    while True:
        # Recibir comandos del cliente
        try:
            # Usamos un timeout corto para no bloquear el bucle de telemetria
            message = await asyncio.wait_for(ws.receive(), timeout=0.1)
            data = json.loads(message)
            if 'command' in data:
                cmd = data['command']
                print(f"Comando recibido: {cmd}")
                handle_command(cmd)
            if 'servo' in data:
                angle = data['servo']
                print(f"Moviendo servo a: {angle}")
                if rover_instance:
                    rover_instance.set_servo_angle(int(angle) if angle is not None else 0)
        except asyncio.TimeoutError:
            pass
        except Exception as e:
            import sys
            print(f"WS Error: {e}")
            sys.print_exception(e)
            # No hacemos 'break' aquí para evitar que se caiga la conexión al dashboard por un mal input

        # Enviar telemetria (distancia del sonar y datos del MPU-6050)
        if rover_instance:
            dist = rover_instance.medir_distancia()
            mpu_data = rover_instance.leer_imu()
            payload = {'distancia': dist}
            if mpu_data:
                payload['mpu'] = mpu_data
            await ws.send(json.dumps(payload))
            
            # Pitido de alerta si detecta obstáculo a 5 cm o menos
            if 0 < dist <= 5.0:
                now = time.ticks_ms()
                if time.ticks_diff(now, rover_instance.last_warning_beep) > 2000:
                    rover_instance.last_warning_beep = now
                    asyncio.create_task(rover_instance.beep(1000, 150))
            
        await asyncio.sleep(0.2) # Frecuencia de actualizacion

def handle_command(cmd):
    if not rover_instance:
        return
        
    if cmd == 'UP':
        rover_instance.set_motores(80, 80)
        rover_instance.set_led(0, 255, 0) # Verde moviendo
    elif cmd == 'DOWN':
        rover_instance.set_motores(-80, -80)
        rover_instance.set_led(255, 165, 0) # Naranja reversa
    elif cmd == 'LEFT':
        rover_instance.set_motores(-50, 50)
    elif cmd == 'RIGHT':
        rover_instance.set_motores(50, -50)
    elif cmd == 'STOP':
        rover_instance.set_motores(0, 0)
        rover_instance.set_led(0, 0, 255) # Azul detenido

import ota

@app.route('/version')
async def get_version(request):
    try:
        with open('version.json', 'r') as f:
            return json.load(f)
    except:
        return {'version': 'unknown'}

@app.route('/update')
async def update(request):
    # Definir la URL del repo (puedes cambiarla por la tuya de GitHub Raw)
    REPO_URL = "https://raw.githubusercontent.com/sebaclas/rover/main"
    print("Disparando actualizacion OTA...")
    # Nota: run_ota reiniciara la placa si encuentra cambios
    ota.run_ota(REPO_URL)
    return {'status': 'updating'}

async def start_server(rover):
    global rover_instance
    rover_instance = rover
    print("Iniciando Web Server en puerto 80...")
    await app.start_server(host='0.0.0.0', port=80)
