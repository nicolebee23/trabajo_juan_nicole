from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import Annotated, Optional
import mysql.connector
import os
from dotenv import load_dotenv
import logging

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MovieLand API", description="API REST para gestión de películas")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de base de datos desde variables de entorno
db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "movieland_user"),
    "password": os.getenv("DB_PASSWORD", "movieland1234"),
    "database": os.getenv("DB_NAME", "movieland_db")
}

def get_db_connection():
    """Obtiene una conexión a la base de datos"""
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as e:
        logger.error(f"Error de conexión a la base de datos: {e}")
        raise HTTPException(status_code=500, detail="Error al conectar a la base de datos")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# ---------- Modelo con validación completa de Pydantic ----------

class Pelicula(BaseModel):
    # Campo obligatorio: título entre 1 y 200 caracteres
    titulo: Annotated[str, Field(min_length=1, max_length=200, description="Título de la película")]
    # Campo obligatorio: género entre 1 y 100 caracteres
    genero: Annotated[str, Field(min_length=1, max_length=100, description="Género cinematográfico")]
    # Campo obligatorio: año entre 1888 (primera película de la historia) y 2026
    año: Annotated[int, Field(ge=1888, le=2026, description="Año de estreno")]
    # Campo obligatorio: director entre 1 y 150 caracteres
    director: Annotated[str, Field(min_length=1, max_length=150, description="Nombre del director")]
    # Campo obligatorio: precio mayor que 0 y máximo 999.99
    precio: Annotated[float, Field(gt=0, le=999.99, description="Precio en euros")]
    # Campo OPCIONAL: si se informa, debe estar entre 1 y 1440 minutos (24h)
    duracion: Annotated[int | None, Field(default=None, ge=1, le=1440, description="Duración en minutos")]
    # Campo OPCIONAL: si se informa, máximo 1000 caracteres
    sinopsis: Annotated[str | None, Field(default=None, max_length=1000, description="Descripción de la película")]

    # Validador personalizado: los campos de texto no pueden ser solo espacios
    @field_validator("titulo", "director", "genero")
    @classmethod
    def no_solo_espacios(cls, valor: str) -> str:
        if valor.strip() == "":
            raise ValueError("Este campo no puede estar vacío ni solo espacios")
        # Devuelve el valor sin espacios al principio ni al final
        return valor.strip()

    # Validador personalizado: redondea el precio a 2 decimales
    @field_validator("precio")
    @classmethod
    def precio_redondeado(cls, valor: float) -> float:
        return round(valor, 2)

# ---------- Exception handler para errores de validación ----------
# Cuando Pydantic falla, FastAPI devuelve un 422. Este handler lo captura
# y devuelve los mensajes de error de forma legible para el frontend.

@app.exception_handler(RequestValidationError)
async def handler_errores_validacion(request: Request, exc: RequestValidationError):
    errores = []
    for error in exc.errors():
        campo = error["loc"][-1]   # nombre del campo que falla
        mensaje = error["msg"]     # mensaje que genera Pydantic
        errores.append(f"{campo}: {mensaje}")
    return JSONResponse(
        status_code=422,
        content={"success": False, "errores": errores}
    )

# ---------- Endpoints ----------

@app.get("/", response_class=HTMLResponse)
async def listar(request: Request, page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100), buscar: Optional[str] = None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Construir consulta con búsqueda opcional
        if buscar:
            sql_search = f"%{buscar}%"
            cursor.execute(
                "SELECT * FROM peliculas WHERE titulo LIKE %s OR genero LIKE %s OR director LIKE %s ORDER BY id DESC",
                (sql_search, sql_search, sql_search)
            )
        else:
            cursor.execute("SELECT * FROM peliculas ORDER BY id DESC")
        
        todas_las_peliculas = cursor.fetchall()
        
        # Paginación
        total = len(todas_las_peliculas)
        offset = (page - 1) * limit
        peliculas = todas_las_peliculas[offset:offset + limit]
        total_pages = (total + limit - 1) // limit
        
        cursor.close()
        conn.close()
        
        return templates.TemplateResponse("pages/index.html", {
            "request": request,
            "peliculas": peliculas,
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "buscar": buscar or ""
        })
    except Exception as e:
        logger.error(f"Error en listar: {e}")
        return templates.TemplateResponse("pages/index.html", {
            "request": request,
            "peliculas": [],
            "error": str(e)
        })

# Obtener una película por ID (para rellenar el modal)
@app.get("/api/peliculas/{pelicula_id}")
async def obtener_pelicula(pelicula_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM peliculas WHERE id = %s", (pelicula_id,))
        pelicula = cursor.fetchone()
        cursor.close()
        conn.close()
        if not pelicula:
            raise HTTPException(status_code=404, detail="Película no encontrada")
        return pelicula
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener película {pelicula_id}: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener la película")

@app.post("/api/peliculas")
async def crear_pelicula(pelicula: Pelicula):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO peliculas (titulo, genero, año, director, precio, duracion, sinopsis) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (pelicula.titulo, pelicula.genero, pelicula.año, pelicula.director, pelicula.precio, pelicula.duracion, pelicula.sinopsis))
        conn.commit()
        pelicula_id = cursor.lastrowid
        cursor.close()
        conn.close()
        logger.info(f"Película creada: ID {pelicula_id}")
        return {"success": True, "message": "Película agregada", "id": pelicula_id}
    except Exception as e:
        logger.error(f"Error al crear película: {e}")
        raise HTTPException(status_code=500, detail="Error al crear la película")

@app.put("/api/peliculas/{pelicula_id}")
async def actualizar_pelicula(pelicula_id: int, pelicula: Pelicula):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verificar si la película existe
        cursor.execute("SELECT id FROM peliculas WHERE id = %s", (pelicula_id,))
        existe = cursor.fetchone()
        
        if not existe:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Película no encontrada")
        
        # Actualizar la película
        sql = "UPDATE peliculas SET titulo=%s, genero=%s, año=%s, director=%s, precio=%s, duracion=%s, sinopsis=%s WHERE id=%s"
        cursor.execute(sql, (pelicula.titulo, pelicula.genero, pelicula.año, pelicula.director, pelicula.precio, pelicula.duracion, pelicula.sinopsis, pelicula_id))
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Película actualizada: ID {pelicula_id}")
        return {"success": True, "message": "Película actualizada"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al actualizar película {pelicula_id}: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar la película")

@app.delete("/api/peliculas/{pelicula_id}")
async def eliminar_pelicula(pelicula_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si la película existe antes de eliminar
        cursor.execute("SELECT id FROM peliculas WHERE id = %s", (pelicula_id,))
        existe = cursor.fetchone()
        
        if not existe:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Película no encontrada")
        
        # Eliminar la película
        cursor.execute("DELETE FROM peliculas WHERE id = %s", (pelicula_id,))
        conn.commit()
        
        filas_afectadas = cursor.rowcount
        cursor.close()
        conn.close()
        
        if filas_afectadas == 0:
            raise HTTPException(status_code=500, detail="No se pudo eliminar la película")
        
        logger.info(f"Película eliminada: ID {pelicula_id}")
        return {"success": True, "message": "Película eliminada"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al eliminar película {pelicula_id}: {e}")
        raise HTTPException(status_code=500, detail="Error al eliminar la película")