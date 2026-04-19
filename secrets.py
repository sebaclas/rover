# secrets.py - Credenciales de red para el Rover
# ¡OJO! No compartas este archivo con nadie ni lo subas a repositorios públicos.

secrets = {
    'ssid': 'Flia_Clasen_2.4G',
    'password': 'bacopia1',
    
    # Configuración de IP (deja en None para usar DHCP)
    'static_ip': None, # Ej: '192.168.1.100'
    'gateway': None,   # Ej: '192.168.1.1'
    'subnet': '255.255.255.0',
    'dns': '8.8.8.8'
}
