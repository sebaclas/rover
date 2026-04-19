import machine
import network
import urequests
import os
import json

class OTAUpdater:
    def __init__(self, repo_url):
        self.repo_url = repo_url # Base URL de GitHub Raw
        self.files = ['main.py', 'rover.py', 'web_monitor.py', 'index.html', 'version.json', 'pca9685.py', 'ota.py', 'wifi_manager.py', 'microdot_websocket.py']

    def check_for_update(self):
        """Compara la version local con la del servidor."""
        print("Buscando actualizaciones...")
        try:
            r = urequests.get(f"{self.repo_url}/version.json")
            online_version = r.json()['version']
            r.close()
            
            with open('version.json', 'r') as f:
                local_version = json.load(f)['version']
            
            if online_version != local_version:
                print(f"Nueva version disponible: {online_version}")
                return True
            print("Sistema actualizado.")
            return False
        except Exception as e:
            print(f"Error check_update: {e}")
            return False

    def update_and_reset(self):
        """Descarga todos los archivos y reinicia la placa."""
        print("Iniciando descarga de archivos...")
        for file in self.files:
            try:
                print(f"Descargando {file}...")
                r = urequests.get(f"{self.repo_url}/{file}")
                if r.status_code == 200:
                    with open(file, 'w') as f:
                        f.write(r.text)
                r.close()
            except Exception as e:
                print(f"Error descargando {file}: {e}")
                return False
        
        print("Actualizacion completada. Reiniciando...")
        machine.reset()

def run_ota(repo_url):
    updater = OTAUpdater(repo_url)
    if updater.check_for_update():
        updater.update_and_reset()
