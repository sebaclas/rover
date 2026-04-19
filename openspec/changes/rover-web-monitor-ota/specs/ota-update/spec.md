## ADDED Requirements

### Requirement: Verificación de Versión
El sistema DEBE ser capaz de comparar la versión local del software con una versión remota alojada en un servidor HTTP (p. ej. GitHub).

#### Scenario: Detección de actualización disponible
- **WHEN** el usuario solicita "Check for Updates" en la web
- **THEN** el sistema descarga el archivo version.json remoto y notifica si hay una versión superior

### Requirement: Descarga y Aplicación de Actualizaciones
El sistema DEBE permitir la descarga de archivos `.py` individuales desde el repositorio remoto para actualizar la lógica del rover.

#### Scenario: Actualización completa exitosa
- **WHEN** el usuario confirma la actualización
- **THEN** el rover descarga los archivos modificados, los sobreescribe en el sistema de archivos local y se reinicia automáticamente
