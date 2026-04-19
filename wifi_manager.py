import network
import time
from secrets import secrets

def connect():
    sta_if = network.WLAN(network.STA_IF)
    
    if not sta_if.isconnected():
        print('Conectando a la red...', secrets['ssid'])
        sta_if.active(True)
        
        # Configurar IP estatica si esta definida
        if secrets.get('static_ip'):
            print('Configurando IP estatica:', secrets['static_ip'])
            sta_if.ifconfig((
                secrets['static_ip'], 
                secrets['subnet'], 
                secrets['gateway'], 
                secrets['dns']
            ))
            
        sta_if.connect(secrets['ssid'], secrets['password'])
        
        # Esperar a que se conecte con un timeout de 10 segundos
        timeout = 10
        start_time = time.time()
        while not sta_if.isconnected():
            if time.time() - start_time > timeout:
                print('\nError: Tiempo de espera agotado.')
                return False
            print('.', end='')
            time.sleep(0.5)
            
    print('\nConectado!')
    print('Datos de red (IP, Mascara, Gateway, DNS):', sta_if.ifconfig())
    
    # Sincronizar hora para HTTPS/OTA
    try:
        import ntptime
        print('Sincronizando hora via NTP...')
        ntptime.settime()
        print('Hora sincronizada.')
    except Exception as e:
        print('Error sincronizando hora:', e)
        
    return True

def disconnect():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(False)
    print('WiFi desactivado.')
