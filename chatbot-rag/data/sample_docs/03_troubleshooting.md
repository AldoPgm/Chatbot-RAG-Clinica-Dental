# Troubleshooting — Problemas Comunes y Soluciones de BillEasy

## Problemas de Instalación

### Error: "No se puede instalar .NET Framework"
**Síntoma**: El instalador muestra un error al intentar instalar .NET Framework 4.8.

**Solución**:
1. Descarga .NET Framework 4.8 manualmente desde https://dotnet.microsoft.com/download
2. Instálalo por separado antes de instalar BillEasy
3. Reinicia tu computadora
4. Ejecuta el instalador de BillEasy nuevamente

### Error: "Acceso denegado" durante la instalación
**Síntoma**: El instalador no puede escribir archivos en la carpeta de destino.

**Solución**:
1. Haz clic derecho en el instalador
2. Selecciona "Ejecutar como administrador"
3. Si el problema persiste, cambia la carpeta de instalación a una ubicación con permisos (ej: `D:\BillEasy`)

### La aplicación no inicia después de instalar
**Síntoma**: Al hacer doble clic en BillEasy, no pasa nada o se cierra inmediatamente.

**Solución**:
1. Verifica que tienes los requisitos mínimos del sistema
2. Ve a `C:\Program Files\BillEasy\logs` y revisa el archivo `error.log`
3. Intenta ejecutar como administrador
4. Si hay un error de DLL faltante, reinstala Visual C++ Redistributable 2019+
5. Contacta soporte con el archivo de log adjunto

## Problemas de Facturación

### La numeración de facturas se saltó un número
**Síntoma**: Las facturas pasan de FAC-00045 a FAC-00047, faltando el 00046.

**Causa**: Probablemente se creó y eliminó una factura borrador.

**Solución**:
1. Ve a **Configuración → Numeración**
2. Haz clic en "Ver historial de numeración"
3. Verifica si el número fue usado por un borrador eliminado
4. Si necesitas ajustar, haz clic en "Configurar próximo número"
5. **Nota**: En algunos países, la ley no permite saltar números. Consulta con tu contador.

### No puedo editar una factura ya emitida
**Síntoma**: Los campos de la factura están bloqueados.

**Explicación**: Por regulaciones fiscales, las facturas emitidas no pueden modificarse.

**Solución**:
1. Crea una **Nota de Crédito** para anular la factura incorrecta
2. Emite una nueva factura con los datos correctos
3. Ve a **Facturación → Nueva Nota de Crédito → Seleccionar factura a anular**

### La factura no se envía por email
**Síntoma**: Al hacer clic en "Enviar por email", nada sucede o aparece un error.

**Solución**:
1. Verifica la configuración SMTP en **Configuración → Email**:
   - Servidor SMTP: `smtp.gmail.com` (Gmail) o tu servidor
   - Puerto: 587 (TLS) o 465 (SSL)
   - Usuario: tu email completo
   - Contraseña: usa una contraseña de aplicación, no tu contraseña normal
2. Haz clic en "Enviar email de prueba"
3. Revisa la carpeta de spam del destinatario
4. Si usas Gmail, habilita "Acceso de apps menos seguras" o genera una contraseña de aplicación

## Problemas de Rendimiento

### BillEasy se pone lento con muchas facturas
**Síntoma**: La aplicación tarda en cargar o responder cuando hay miles de facturas.

**Solución**:
1. Ve a **Configuración → Rendimiento**
2. Activa "Carga diferida de historial"
3. Configura "Mostrar facturas de los últimos X meses" (recomendado: 6 meses)
4. Haz clic en "Optimizar base de datos" (esto puede tardar unos minutos)
5. Si el problema persiste, considera archivar facturas antiguas: **Archivo → Archivar Período**

### El PDF de la factura tarda mucho en generarse
**Síntoma**: Al exportar a PDF, la generación tarda más de 30 segundos.

**Solución**:
1. Verifica que el logo no sea una imagen muy pesada (máximo 500 KB recomendado)
2. Reduce la resolución del logo a 300x300 píxeles
3. Ve a **Configuración → PDF → Calidad** y selecciona "Normal" en vez de "Alta"
4. Si tienes muchos productos en la factura, verifica que no haya imágenes de producto adjuntas

## Problemas de Conexión

### Error: "No se puede conectar al servidor de licencias"
**Síntoma**: BillEasy muestra un error de conexión al iniciar.

**Solución**:
1. Verifica tu conexión a internet
2. Si usas un proxy corporativo, configúralo en **Configuración → Red → Proxy**:
   - Servidor proxy: tu.proxy.com
   - Puerto: 8080
   - Autenticación si es necesaria
3. Agrega `licencias.billeasy.com` a la lista blanca de tu firewall
4. Si estás offline, BillEasy funciona en modo offline por hasta 30 días

### Error de sincronización con BillEasy Cloud
**Síntoma**: Los datos no se sincronizan entre la versión de escritorio y la nube.

**Solución**:
1. Verifica tu conexión a internet
2. Ve a **Herramientas → Estado de Sincronización**
3. Si dice "Conflicto detectado", haz clic en "Resolver conflictos"
4. Elige cuál versión mantener (local o nube)
5. Haz clic en "Forzar sincronización completa"
6. Si el error persiste, contacta soporte con el ID de sincronización

## Problemas de Impresión

### La factura se imprime cortada
**Síntoma**: Al imprimir, parte del contenido queda fuera de la página.

**Solución**:
1. Ve a **Configuración → Impresión**
2. Selecciona el tamaño de papel correcto (A4, Carta, etc.)
3. Ajusta los márgenes (mínimo recomendado: 15mm)
4. Usa la opción "Vista previa" antes de imprimir
5. Si tienes una impresora térmica (ticket), selecciona la plantilla "Ticket POS"

## Contactar Soporte

Si ninguna de las soluciones anteriores resuelve tu problema:

- **Email**: soporte@billeasy.com (respuesta en menos de 24 horas hábiles)
- **Chat en vivo**: Disponible en https://billeasy.com de lunes a viernes, 9:00–18:00
- **Teléfono**: +54 11 4567-8900 (Argentina) / +52 55 1234-5678 (México)
- **Base de conocimiento**: https://help.billeasy.com

Al contactar soporte, incluye:
1. Tu número de licencia
2. Versión de BillEasy (Ayuda → Acerca de)
3. Sistema operativo y versión
4. Descripción detallada del problema
5. Capturas de pantalla si es posible
6. Archivo de log (`Ayuda → Exportar Logs`)
