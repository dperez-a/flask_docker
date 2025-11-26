# README.md

## 📋 Descripción del Proyecto

Proyecto de contenedores con Docker y Docker Compose que implementa una API REST con Flask, base de datos MySQL y servidor NGINX como proxy inverso.

La aplicación devuelve un mensaje "Hola mundo" almacenado en MySQL a través de una API Flask gestionada por NGINX.

## 🏗️ Arquitectura

```
Cliente (navegador)
    ↓
NGINX (puerto 3232)
    ↓
Flask API (puerto 5000)
    ↓
MySQL (puerto 3306)
```

## 📁 Estructura del Proyecto

```
flask_docker/
├── app.py                 # Aplicación Flask con API REST
├── requirements.txt       # Dependencias de Python
├── nginx.conf            # Configuración de NGINX
├── Dockerfile            # Imagen Docker para Flask
├── docker-compose.yml    # Orquestación de servicios
└── README.md            # Este archivo
```

## 🔧 Requisitos Previos

- Docker instalado (versión 20.10 o superior)
- Docker Compose instalado (versión 2.0 o superior)

Verificar instalación:
```bash
docker --version
docker-compose --version
```

## 🚀 Cómo Ejecutar el Proyecto

### 1. Clonar o descargar el proyecto

Asegúrate de tener todos los archivos en la carpeta `flask_docker/`

### 2. Construir y levantar los contenedores

Desde la carpeta `flask_docker/`, ejecuta:

```bash
docker-compose up --build
```

Este comando:
- Construye la imagen de Flask desde el Dockerfile
- Descarga las imágenes de MySQL 8.0 y NGINX Alpine
- Crea y configura los contenedores
- Establece las redes y volúmenes necesarios
- Inicia todos los servicios

**Nota:** La primera vez puede tardar varios minutos en descargar las imágenes.

### 3. Verificar que la aplicación funciona

Una vez que veas el mensaje `Running on http://0.0.0.0:5000`, abre tu navegador y accede a:

```
http://localhost:3232
```

Deberías ver una respuesta JSON:
```json
[[1, "Hola mundo"]]
```

### 4. Ejecutar en segundo plano (opcional)

Si quieres que los contenedores se ejecuten en segundo plano:

```bash
docker-compose up -d
```

## 🛠️ Comandos Útiles

### Ver el estado de los contenedores

```bash
docker-compose ps
```

### Ver los logs en tiempo real

```bash
# Todos los servicios
docker-compose logs -f

# Un servicio específico
docker-compose logs -f api
docker-compose logs -f db
docker-compose logs -f nginx
```

### Detener los contenedores

```bash
docker-compose down
```

### Detener y eliminar volúmenes (borra la base de datos)

```bash
docker-compose down -v
```

### Reiniciar un servicio específico

```bash
docker-compose restart api
docker-compose restart db
docker-compose restart nginx
```

### Reconstruir la imagen de Flask

Si modificas el código de `app.py`:

```bash
docker-compose up --build api
```

### Acceder al contenedor de MySQL

```bash
docker exec -it mysql_db mysql -u root -p
# Password: example
```

Dentro de MySQL:
```sql
USE test_db;
SELECT * FROM greetings;
```

### Acceder al contenedor de Flask

```bash
docker exec -it flask_api /bin/bash
```

## 🔍 Verificación de Servicios

### Verificar que NGINX está funcionando

```bash
curl http://localhost:3232
```

### Verificar que Flask está funcionando (directamente)

```bash
curl http://localhost:5000
```

### Verificar conectividad entre contenedores

```bash
# Desde el contenedor de Flask, hacer ping a MySQL
docker exec -it flask_api ping db
```

## 📊 Puertos Utilizados

| Servicio | Puerto Interno | Puerto Expuesto | Descripción |
|----------|---------------|-----------------|-------------|
| Flask    | 5000          | 5000            | API REST    |
| NGINX    | 80            | 3232            | Proxy inverso |
| MySQL    | 3306          | -               | Base de datos |

## 💾 Persistencia de Datos

Los datos de MySQL se almacenan en un volumen Docker llamado `mysql_data`. Esto garantiza que:

- Los datos persisten entre reinicios de contenedores
- Los datos NO se pierden al hacer `docker-compose down`
- Los datos SOLO se eliminan con `docker-compose down -v`

### Ubicación del volumen

```bash
# Ver información del volumen
docker volume inspect flask_docker_mysql_data

# Listar todos los volúmenes
docker volume ls
```

## 🔧 Solución de Problemas

### Error: "Puerto ya en uso"

Si el puerto 3232 o 5000 está ocupado:

1. Cambiar el puerto en `docker-compose.yml`:
```yaml
ports:
  - "8080:80"  # Cambia 3232 por otro puerto
```

### Error: "Cannot connect to MySQL"

Espera unos segundos más. MySQL tarda en inicializarse. El healthcheck se encarga de esto, pero la primera vez puede tardar hasta 30 segundos.

### Ver qué está fallando

```bash
# Ver logs detallados
docker-compose logs

# Ver logs de MySQL
docker-compose logs db
```

### Reiniciar desde cero

```bash
# Eliminar todo y empezar de nuevo
docker-compose down -v
docker-compose up --build
```

## 🧪 Pruebas

### Probar la persistencia de datos

1. Levantar los servicios:
```bash
docker-compose up -d
```

2. Verificar que hay datos:
```bash
curl http://localhost:3232
```

3. Detener los contenedores:
```bash
docker-compose down
```

4. Volver a levantar:
```bash
docker-compose up -d
```

5. Verificar que los datos siguen ahí:
```bash
curl http://localhost:3232
```

### Probar la API con diferentes métodos

```bash
# GET request
curl http://localhost:3232

# Con formato legible
curl http://localhost:3232 | python -m json.tool
```

## 📝 Variables de Entorno

Las variables de entorno se configuran en `docker-compose.yml`:

```yaml
environment:
  DB_HOST: db
  DB_USER: root
  DB_PASSWORD: example
  DB_NAME: test_db
```

Para cambiarlas, modifica estos valores en el archivo `docker-compose.yml`.

## 🎯 Endpoints de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET    | `/`      | Devuelve todos los mensajes de la tabla greetings |

## 📚 Tecnologías Utilizadas

- **Python 3.11**: Lenguaje de programación
- **Flask**: Framework web para la API REST
- **MySQL 8.0**: Base de datos relacional
- **NGINX Alpine**: Servidor web y proxy inverso
- **Docker & Docker Compose**: Contenedorización y orquestación