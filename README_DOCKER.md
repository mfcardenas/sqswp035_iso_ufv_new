# 🐳 Docker Deployment Guide - ISO Standards Games

## 📦 Contenido del Empaquetado

Este Dockerfile empaqueta completamente la aplicación **ISO Standards Games** que incluye:

- **Servidor FastAPI** en el puerto **8001**
- **Tres juegos educativos:**
  - `QualityQuest` - ISO/IEC 25010 (Quality Attributes)
  - `RequirementRally` - ISO/IEC/IEEE 29148 (Requirements)
  - `UsabilityUniverse` - ISO 9241 (Usability)

## 🚀 Construcción y Ejecución

### Opción 1: Docker Build Directo

```bash
# Construir la imagen
docker build -t iso-standards-games .

# Ejecutar el contenedor
docker run -d -p 8001:8001 --name iso-standards-games iso-standards-games

# Ver logs
docker logs -f iso-standards-games
```

### Opción 2: Docker Compose (Recomendado)

```bash
# Iniciar la aplicación
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener la aplicación
docker-compose down
```

## 🌐 Acceso a la Aplicación

Una vez el contenedor esté corriendo, accede a:

- **Aplicación Principal**: http://localhost:8001
- **QualityQuest**: http://localhost:8001
- **RequirementRally**: http://localhost:8001/requirement-rally
- **UsabilityUniverse**: http://localhost:8001/usability-universe
- **API Docs**: http://localhost:8001/docs

## 🔧 Configuración

### Variables de Entorno

Puedes personalizar el comportamiento mediante variables de entorno:

```bash
docker run -d -p 8001:8001 \
  -e DEBUG=true \
  -e DEFAULT_LOCALE=es \
  -e LLM_PROVIDER=ollama \
  --name iso-standards-games \
  iso-standards-games
```

Variables disponibles:
- `APP_NAME`: Nombre de la aplicación (default: "ISO Standards Games")
- `DEBUG`: Modo debug (default: false)
- `DEFAULT_LOCALE`: Idioma por defecto - `en` o `es` (default: en)
- `LLM_PROVIDER`: Proveedor LLM - `ollama` o `azure` (default: ollama)
- `OLLAMA_BASE_URL`: URL del servidor Ollama (default: http://localhost:11434)
- `OLLAMA_MODEL`: Modelo de Ollama (default: qwen3)
- `DATABASE_URL`: URL de base de datos SQLite (default: sqlite:///./iso_standards_games.db)

### Persistencia de Datos

Para persistir la base de datos entre reinicios:

```bash
docker run -d -p 8001:8001 \
  -v $(pwd)/data:/app/data \
  -e DATABASE_URL=sqlite:///./data/iso_standards_games.db \
  --name iso-standards-games \
  iso-standards-games
```

## 🏗️ Arquitectura del Dockerfile

El Dockerfile usa **multi-stage build** para optimizar el tamaño:

1. **Stage Builder**: 
   - Instala Poetry y dependencias
   - Genera requirements.txt

2. **Stage Runtime**:
   - Copia solo los archivos necesarios
   - Imagen final optimizada
   - Python 3.9-slim como base

## 📊 Características del Contenedor

- **Puerto**: 8001
- **Host**: 0.0.0.0 (acepta conexiones externas)
- **Health Check**: Verifica cada 30s que el servidor responde
- **Restart Policy**: Se reinicia automáticamente en caso de fallo
- **Sin modificaciones**: El proyecto original NO se modifica

## 🛠️ Comandos Útiles

```bash
# Ver el estado del contenedor
docker ps

# Inspeccionar el contenedor
docker inspect iso-standards-games

# Acceder al shell del contenedor
docker exec -it iso-standards-games /bin/bash

# Ver uso de recursos
docker stats iso-standards-games

# Detener el contenedor
docker stop iso-standards-games

# Eliminar el contenedor
docker rm iso-standards-games

# Eliminar la imagen
docker rmi iso-standards-games
```

## 🔍 Troubleshooting

### El contenedor no inicia
```bash
# Ver logs detallados
docker logs iso-standards-games

# Verificar que el puerto 8001 no esté en uso
netstat -an | findstr :8001  # Windows
lsof -i :8001                # Linux/Mac
```

### No puedo acceder a la aplicación
```bash
# Verificar que el contenedor está corriendo
docker ps | findstr iso-standards-games

# Verificar health check
docker inspect --format='{{.State.Health.Status}}' iso-standards-games
```

### Problemas de conexión LLM
Por defecto, la aplicación funciona **sin LLM externo** usando las bases de datos de escenarios incluidas. Si deseas usar Ollama:

```bash
# Ollama debe estar accesible desde el contenedor
# Usa host.docker.internal en Windows/Mac
docker run -d -p 8001:8001 \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  --name iso-standards-games \
  iso-standards-games
```

## 📝 Notas Importantes

- ✅ El proyecto original **NO se modifica**
- ✅ Todos los frontends están incluidos
- ✅ Las bases de datos de escenarios están incluidas
- ✅ Funciona sin LLM externo (usa fallback)
- ✅ Puerto **8001** como especificado
- ✅ Imagen optimizada con multi-stage build

## 🎮 Verificación de Funcionamiento

Después de iniciar el contenedor, verifica:

1. **API Status**: http://localhost:8001
2. **API Docs**: http://localhost:8001/docs
3. **QualityQuest**: http://localhost:8001
4. **RequirementRally**: http://localhost:8001/requirement-rally
5. **UsabilityUniverse**: http://localhost:8001/usability-universe

Todos los endpoints deben responder correctamente.

## 📦 Información de la Imagen

- **Tamaño aproximado**: ~500-600 MB
- **Base**: python:3.9-slim
- **Dependencias**: FastAPI, Uvicorn, Pydantic, httpx, jinja2, python-i18n
- **Sin modificaciones al código original**

---

**¡Listo para desplegar! 🚀**
