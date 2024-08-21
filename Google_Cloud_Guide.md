
# Ejecución del Script en la Nube con Google Cloud

Este documento describe cómo configurar y ejecutar el script `send_messages.py` en la nube utilizando Google Cloud Run y Google Cloud Scheduler. Esta es una solución ideal para ejecutar tareas programadas automáticamente sin necesidad de mantener un servidor propio.

## Pasos para Configurar y Ejecutar en Google Cloud

### 1. Subir el Script a Google Cloud Storage

1. Accede a Google Cloud Console.
2. Navega a "Storage" y crea un bucket si no tienes uno.
3. Sube el archivo `send_messages.py` al bucket.

### 2. Crear un Contenedor Docker para Google Cloud Run

#### 1. Crear un Dockerfile

Crea un archivo llamado `Dockerfile` en el mismo directorio donde está tu script con el siguiente contenido:

```Dockerfile
# Usa una imagen base oficial de Python
FROM python:3.8-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos y el script al contenedor
COPY requirements.txt requirements.txt
COPY send_messages.py send_messages.py

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar el script
CMD ["python", "send_messages.py"]
```

#### 2. Crear el archivo `requirements.txt`

Crea un archivo `requirements.txt` con el siguiente contenido:

```txt
pywhatkit
sqlite3
```

#### 3. Construir la imagen de Docker

En la terminal, ejecuta:

```bash
docker build -t gcr.io/YOUR_PROJECT_ID/whatsapp-messaging .
```

#### 4. Subir la imagen a Google Container Registry

Sube la imagen construida al registro de contenedores de Google:

```bash
docker push gcr.io/YOUR_PROJECT_ID/whatsapp-messaging
```

### 3. Desplegar en Google Cloud Run

Despliega la aplicación en Google Cloud Run con el siguiente comando:

```bash
gcloud run deploy whatsapp-messaging --image gcr.io/YOUR_PROJECT_ID/whatsapp-messaging --platform managed --region YOUR_REGION --allow-unauthenticated
```

Durante el despliegue, selecciona "Allow unauthenticated invocations" para permitir que el servicio sea invocado por Google Cloud Scheduler.

### 4. Configurar Google Cloud Scheduler

#### 1. Crear un trabajo de Cloud Scheduler

1. Ve a Google Cloud Console y navega a "Cloud Scheduler".
2. Crea un nuevo trabajo con los siguientes detalles:
    - **Frecuencia:** `0 10 * * *` (esto ejecutará el trabajo todos los días a las 10:00 AM).
    - **URL de destino:** La URL de la aplicación desplegada en Google Cloud Run.
    - **Método:** `POST`.
    - **Autenticación:** Selecciona "Allow unauthenticated invocations" si no utilizaste autenticación.

2. Guarda y verifica que el trabajo está configurado para ejecutarse diariamente.

### Automatización Completa

Con esta configuración, tu script Python se ejecutará automáticamente cada día en Google Cloud Run, activado por Google Cloud Scheduler. Este enfoque te permite ejecutar tu script de manera programada y sin necesidad de mantener un servidor físico o virtual.

### Ventajas de esta Configuración:

- **Escalabilidad:** Google Cloud Run puede manejar la escalabilidad automáticamente.
- **Seguridad:** Al utilizar los servicios gestionados de Google, se garantiza un alto nivel de seguridad.
- **Facilidad de uso:** Una vez configurado, el proceso es totalmente automatizado.

## Consideraciones Finales

Este método es ideal para desarrolladores que desean automatizar procesos en la nube sin la complejidad de mantener infraestructura propia. Si tienes alguna pregunta o necesitas asistencia adicional, consulta la documentación de Google Cloud o abre una incidencia en el repositorio.
