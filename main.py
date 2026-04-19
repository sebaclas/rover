import uasyncio as asyncio
import wifi_manager
from rover import Rover
import web_monitor
import machine

async def main():
    print("--- Rover Explorer Starting ---")
    
    # 1. Inicializar Hardware
    rover = Rover()
    rover.set_led(255, 0, 0) # Rojo: Iniciando
    
    # 2. Conectar WiFi (DHCP por defecto)
    connected = wifi_manager.connect()
    if not connected:
        print("Fallo conexion WiFi. Reintentando en 10s...")
        rover.set_led(255, 0, 0) # Rojo parpadeo?
        await asyncio.sleep(10)
        machine.reset()
    
    rover.set_led(0, 255, 0) # Verde: Conectado
    print("Sistema listo!")

    # 3. Lanzar Servidor Web (esto bloquea segun implementacion de Microdot app.run)
    # Sin embargo, Microdot.start_server es asincrona
    await web_monitor.start_server(rover)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Detenido por el usuario")
    except Exception as e:
        print(f"Error critico en main: {e}")
        machine.reset()