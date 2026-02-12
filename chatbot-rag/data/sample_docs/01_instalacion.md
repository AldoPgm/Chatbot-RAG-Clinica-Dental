# Guía de Instalación — BillEasy v3.2

## Requisitos del Sistema

### Windows
- Windows 10 o superior (64-bit)
- 4 GB de RAM mínimo (8 GB recomendado)
- 500 MB de espacio en disco
- .NET Framework 4.8 o superior
- Conexión a internet para activación

### macOS
- macOS 12 (Monterey) o superior
- 4 GB de RAM mínimo
- 500 MB de espacio en disco
- Procesador Intel o Apple Silicon (M1/M2/M3)

### Linux
- Ubuntu 20.04+, Debian 11+, Fedora 36+
- 4 GB de RAM mínimo
- 500 MB de espacio en disco
- Python 3.10+ (para la versión CLI)

## Instalación en Windows

1. Descarga el instalador desde https://billeasy.com/descargas
2. Ejecuta `BillEasy-Setup-3.2.exe` como administrador
3. Acepta los términos de licencia
4. Selecciona la carpeta de instalación (por defecto: `C:\Program Files\BillEasy`)
5. Elige los componentes:
   - **BillEasy Core** (obligatorio) — Motor de facturación
   - **BillEasy Reports** (recomendado) — Módulo de reportes
   - **BillEasy Sync** (opcional) — Sincronización en la nube
6. Haz clic en "Instalar" y espera a que finalice
7. Al terminar, marca "Iniciar BillEasy" y haz clic en "Finalizar"

## Instalación en macOS

1. Descarga `BillEasy-3.2.dmg` desde https://billeasy.com/descargas
2. Abre el archivo DMG
3. Arrastra BillEasy a la carpeta Aplicaciones
4. La primera vez que abras la app, haz clic derecho → Abrir (por seguridad de macOS)
5. Ingresa tu clave de licencia cuando se solicite

## Instalación en Linux

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y billeasy

# Fedora
sudo dnf install billeasy

# Instalación manual
wget https://billeasy.com/descargas/billeasy-3.2-linux.tar.gz
tar -xzf billeasy-3.2-linux.tar.gz
cd billeasy-3.2
sudo ./install.sh
```

## Versión en la Nube (BillEasy Cloud)

Si prefieres no instalar nada, puedes usar BillEasy Cloud:

1. Ve a https://cloud.billeasy.com
2. Crea una cuenta con tu email empresarial
3. Elige tu plan (hay prueba gratuita de 14 días)
4. Configura tu empresa (nombre, RUT/CUIT, dirección fiscal)
5. ¡Comienza a facturar!

BillEasy Cloud incluye todas las funcionalidades de la versión de escritorio más:
- Acceso desde cualquier dispositivo
- Backups automáticos diarios
- Actualizaciones automáticas
- Soporte prioritario

## Activación de Licencia

1. Abre BillEasy
2. Ve a **Ayuda → Activar Licencia**
3. Ingresa tu clave de 25 caracteres (formato: XXXXX-XXXXX-XXXXX-XXXXX-XXXXX)
4. Haz clic en "Activar"
5. Si la activación falla, verifica tu conexión a internet o contacta soporte@billeasy.com

## Actualización

BillEasy busca actualizaciones automáticamente al iniciar. También puedes buscar manualmente:

1. Ve a **Ayuda → Buscar Actualizaciones**
2. Si hay una actualización disponible, haz clic en "Descargar e Instalar"
3. La aplicación se reiniciará automáticamente

**Nota importante**: Siempre haz un backup de tus datos antes de actualizar. Ve a **Archivo → Exportar Backup**.
