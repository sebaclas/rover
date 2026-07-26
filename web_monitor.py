from microdot_asyncio import Microdot, send_file
from microdot_websocket import with_websocket
import uasyncio as asyncio
import json
import time
import gc
import sys
import ota

app = Microdot()
rover_instance = None

@app.route('/')
async def index(request):
    return send_file('index.html', max_age=86400)

@app.route('/ws')
@with_websocket
async def telemetry(request, ws):
    print("Cliente WebSocket conectado")
    loop_count = 0
    while True:
        loop_count += 1
        # Reciclaje periódico de basura en el heap cada 10 ciclos (2 segundos)
        if loop_count % 10 == 0:
            gc.collect()

        # Recibir comandos del cliente
        try:
            message = await asyncio.wait_for(ws.receive(), timeout=0.1)
            data = json.loads(message)
            if 'command' in data:
                cmd = data['command']
                print(f"Comando recibido: {cmd}")
                await handle_command(cmd, data)
            if 'servo' in data:
                angle = data['servo']
                print(f"Moviendo servo a: {angle}")
                if rover_instance:
                    asyncio.create_task(rover_instance.set_servo_angle_smooth(int(angle) if angle is not None else 0))
        except asyncio.TimeoutError:
            pass
        except Exception as e:
            print(f"WS Error: {e}")
            sys.print_exception(e)

        # Enviar telemetria (distancia, datos IMU, RAM y estado de secuencia)
        if rover_instance:
            dist = rover_instance.medir_distancia()
            mpu_data = rover_instance.leer_imu()
            payload = {
                'distancia': dist,
                'ram_free': gc.mem_free(),
                'ram_alloc': gc.mem_alloc(),
                'sequence_status': getattr(rover_instance, 'sequence_status', {}),
                'speed_m_s': getattr(rover_instance, 'speed_m_s', 0.35),
                'global_speed': getattr(rover_instance, 'global_speed_pct', 80)
            }
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

async def handle_command(cmd, data=None):
    if not rover_instance:
        return

    # Si es un comando manual o STOP, cancelamos secuencias o giros activos
    if cmd in ['UP', 'DOWN', 'LEFT', 'RIGHT', 'STOP']:
        if rover_instance.active_turn_task and not rover_instance.active_turn_task.done():
            rover_instance.active_turn_task.cancel()
            rover_instance.active_turn_task = None
        if rover_instance.active_sequence_task and not rover_instance.active_sequence_task.done():
            rover_instance.active_sequence_task.cancel()
            rover_instance.active_sequence_task = None

    if cmd == 'UP':
        rover_instance.set_motores(-rover_instance.global_speed_pct, rover_instance.global_speed_pct) # Adelante
        rover_instance.set_led(0, 255, 0) # Verde moviendo
    elif cmd == 'DOWN':
        rover_instance.set_motores(rover_instance.global_speed_pct, -rover_instance.global_speed_pct) # Atrás
        rover_instance.set_led(255, 165, 0) # Naranja reversa
    elif cmd == 'LEFT':
        rover_instance.set_motores(50, 50) # Giro Izquierda
    elif cmd == 'RIGHT':
        rover_instance.set_motores(-50, -50) # Giro Derecha
    elif cmd == 'STOP':
        rover_instance.set_motores(0, 0)
        rover_instance.set_led(0, 0, 255) # Azul detenido
    elif cmd == 'TURN_LEFT_90':
        rover_instance.active_turn_task = asyncio.create_task(rover_instance.girar_grados(90))
    elif cmd == 'TURN_RIGHT_90':
        rover_instance.active_turn_task = asyncio.create_task(rover_instance.girar_grados(-90))
    elif cmd == 'EXECUTE_PROGRAM':
        steps = data.get('steps', []) if data else []
        cal_speed = float(data.get('speed_m_s', rover_instance.speed_m_s)) if data else None
        g_speed = int(data.get('global_speed', rover_instance.global_speed_pct)) if data else None
        if rover_instance.active_sequence_task and not rover_instance.active_sequence_task.done():
            rover_instance.active_sequence_task.cancel()
        rover_instance.active_sequence_task = asyncio.create_task(
            rover_instance.ejecutar_secuencia(steps, calibration_speed=cal_speed, global_speed=g_speed)
        )
    elif cmd == 'ABORT_PROGRAM':
        asyncio.create_task(rover_instance.abortar_secuencia())
    elif cmd == 'RUN_CALIBRATION_TEST':
        power = int(data.get('power', 80)) if data else 80
        if rover_instance.active_sequence_task and not rover_instance.active_sequence_task.done():
            rover_instance.active_sequence_task.cancel()
        rover_instance.active_sequence_task = asyncio.create_task(rover_instance.ejecutar_calibracion_5s(power))
    elif cmd == 'SET_CALIBRATION':
        if data and 'speed_m_s' in data:
            rover_instance.speed_m_s = float(data['speed_m_s'])
    elif cmd == 'SET_GLOBAL_SPEED':
        if data and 'global_speed' in data:
            rover_instance.global_speed_pct = int(data['global_speed'])

@app.route('/version')
async def get_version(request):
    try:
        with open('version.json', 'r') as f:
            return json.load(f)
    except:
        return {'version': 'unknown'}

@app.route('/update')
async def update(request):
    REPO_URL = "https://raw.githubusercontent.com/sebaclas/rover/main"
    print("Disparando actualizacion OTA asincrona...")
    asyncio.create_task(trigger_ota(REPO_URL))
    return {'status': 'updating'}

async def trigger_ota(repo_url):
    await asyncio.sleep(1) # Esperar a que se envie la respuesta HTTP al cliente
    gc.collect()
    ota.run_ota(repo_url)


async def start_server(rover):
    global rover_instance
    rover_instance = rover
    gc.collect()
    print(f"Iniciando Web Server en puerto 80... RAM libre: {gc.mem_free()} bytes")
    await app.start_server(host='0.0.0.0', port=80)

