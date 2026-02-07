# MovieLand - Tienda de Películas

Plataforma web para la gestión y visualización de un catálogo de películas mediante una API REST.

---

## 👤 Información del Estudiante

- **Nombre y apellidos:** Nicole Beeckmans Barrientos
- **Número de alumno:** *(ponlo aquí)*
- **GitHub:** [@nicolebee23](https://github.com/nicolebee23)

---

## 📝 Descripción

MovieLand es una API REST desarrollada con **FastAPI** y **Python** que permite gestionar un catálogo de películas mediante operaciones CRUD (Crear, Leer, Actualizar, Eliminar). El acceso a datos se realiza **sin ORM**, conectándose directamente a una base de datos **MySQL** mediante sentencias SQL y el conector `mysql-connector-python`. La validación de datos se gestiona con **Pydantic** usando `Field` y `field_validator`. El frontend está construido con HTML5, CSS3, JavaScript y Bootstrap 5.

---

## 🛠️ Tecnologías

- **Backend:** Python 3.13, FastAPI, Pydantic, mysql-connector-python
- **Frontend:** HTML5, CSS3, JavaScript ES6+, Bootstrap 5
- **Base de datos:** MySQL 8.0
- **Servidor:** Uvicorn

---

## 📁 Estructura del Proyecto

```
MOVIELAND/
├── app/
│   ├── main.py                  # Aplicación FastAPI (endpoints + modelos Pydantic)
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css       # Estilos personalizados
│   │   ├── img/                 # Imágenes
│   │   └── js/
│   │       └── main.js          # Lógica del frontend
│   └── templates/
│       └── pages/
│           └── index.html       # Interfaz web
├── docs/
│   └── init_database.sql        # Script de inicialización de la base de datos
├── requirements.txt             # Dependencias de Python
└── README.md                    # Este archivo
```

---

## 🚀 Cómo ejecutar la aplicación

### 1. Configurar variables de entorno

Copia el archivo `.env.example` a `.env` y configura tus credenciales de base de datos:

```bash
cp .env.example .env
```

Edita `.env` con tus valores:

```
DB_HOST=localhost
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=movieland_db
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Inicializar la base de datos

Abre MySQL y ejecuta el script:

```bash
mysql -u root -p < docs/init_database.sql
```

### 4. Ejecutar la aplicación

```bash
uvicorn app.main:app --reload
```

### 5. Acceder

- **Interfaz web:** http://localhost:8000
- **Documentación API (Swagger):** http://localhost:8000/docs
- **Documentación alternativa (ReDoc):** http://localhost:8000/redoc

---

## 🔌 Endpoints de la API

| Método   | Endpoint                  | Descripción                        |
|----------|---------------------------|------------------------------------|
| GET      | `/`                       | Muestra la interfaz web            |
| GET      | `/api/peliculas/{id}`     | Obtiene una película por ID        |
| POST     | `/api/peliculas`          | Crea una nueva película            |
| PUT      | `/api/peliculas/{id}`     | Actualiza una película existente   |
| DELETE   | `/api/peliculas/{id}`     | Elimina una película               |

---

## ✅ Validación con Pydantic

El modelo `Pelicula` aplica las siguientes validaciones:

- **titulo:** obligatorio, entre 1 y 200 caracteres, no puede ser solo espacios
- **genero:** obligatorio, entre 1 y 100 caracteres, no puede ser solo espacios
- **año:** obligatorio, entre 1888 y 2026
- **director:** obligatorio, entre 1 y 150 caracteres, no puede ser solo espacios
- **precio:** obligatorio, mayor que 0 y máximo 999.99, se redondea a 2 decimales
- **duracion:** opcional, si se informa debe estar entre 1 y 1440 minutos
- **sinopsis:** opcional, máximo 1000 caracteres

---

## � Mejoras de Seguridad y Rendimiento

### Seguridad
- ✅ **Variables de entorno**: Las credenciales de base de datos se cargan desde `.env` (no hardcodeadas)
- ✅ **CORS habilitado**: Permite solicitudes desde diferentes dominios
- ✅ **Manejo de errores mejorado**: Errores sensibles no se muestran al cliente
- ✅ **Logging**: Se registran las operaciones importantes para debugging

### Validación de Datos
- ✅ **Verificación de existencia en PUT**: Solo actualiza si la película existe
- ✅ **Verificación de existencia en DELETE**: Solo elimina si la película existe
- ✅ **Validación de resultados**: Confirma que las operaciones fueron exitosas

### Rendimiento
- ✅ **Paginación**: Soporta parámetros `page` y `limit` para listar películas
- ✅ **Búsqueda**: Parámetro `buscar` para filtrar por título, género o director
- ✅ **Requirements.txt optimizado**: Solo dependencias necesarias

### Documentación
- ✅ **Swagger UI**: Documentación automática en `/docs`
- ✅ **ReDoc**: Documentación alternativa en `/redoc`

---

## �📄 Licencia

Proyecto desarrollado con fines educativos en ILERNA (DAW).