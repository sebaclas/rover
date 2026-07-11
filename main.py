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
    

    if rover.oled_ready:
        rover.oled.fill(0)
        rover.oled.text("Rover Explorer", 0, 0)
        rover.oled.text("Iniciando...", 0, 16)
        rover.oled.text("WiFi: Conectando", 0, 32)
        rover.oled.show()
    
    # 2. Conectar WiFi (DHCP por defecto)
    connected = wifi_manager.connect()
    if not connected:
        print("Fallo conexion WiFi. Reintentando en 10s...")
        if rover.oled_ready:
            rover.oled.fill(0)
            rover.oled.text("Rover Explorer", 0, 0)
            rover.oled.text("WiFi: Fallido", 0, 16)
            rover.oled.text("Reintentando...", 0, 32)
            rover.oled.show()
        rover.set_led(255, 0, 0)
        await asyncio.sleep(10)
        machine.reset()
    
    # Obtener dirección IP de la placa
    import network
    ip = network.WLAN(network.STA_IF).ifconfig()[0]
    
    rover.set_led(0, 255, 0) # Verde: Conectado
    
    if rover.oled_ready:
        rover.oled.fill(0)
        rover.oled.text("Rover Listo!", 0, 0)
        rover.oled.text("WiFi: Conectado", 0, 16)
        rover.oled.text(f"IP: {ip}", 0, 32)
        rover.oled.text("Puerto: 80", 0, 48)
        rover.oled.show()
        
    print(f"Sistema listo! IP: {ip}")

    # Pitido de confirmación (inicialización completada con éxito)
    asyncio.create_task(rover.beep(2000, 150))

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