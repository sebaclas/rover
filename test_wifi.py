import wifi_manager
import sys

# Compatibilidad para urequests/requests
try:
    import urequests as requests
except ImportError:
    try:
        import requests
    except ImportError:
        print("Error: No se encontro el modulo 'requests' o 'urequests'.")
        sys.exit()

def run_test():
    # Intentar conectar si no lo estamos
    if not wifi_manager.connect():
        print("No se pudo establecer la conexion WiFi.")
        return
    
    print("\n--- Probando conexion HTTP ---")
    try:
        url = "http://httpbin.org/ip"
        print("Peticion a:", url)
        response = requests.get(url)
        print("Estado HTTP:", response.status_code)
        print("Tu IP de Internet es:", response.text)
        response.close()
        print("\nPrueba de internet EXITOSA!")
    except Exception as e:
        print("Fallo en la prueba de internet:", e)

if __name__ == "__main__":
    run_test()
