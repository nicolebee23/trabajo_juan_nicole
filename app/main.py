from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import mysql.connector

app = FastAPI(title="MovieLand API")

# Configuración de la base de datos
db_config = {
    "host": "localhost",
    "user": "movieland_user",
    "password": "movieland1234",
    "database": "movieland_db"
}

# Función para obtener conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Motor de plantillas
templates = Jinja2Templates(directory="app/templates")

# --- READ: Mostrar todas las películas (HTML) ---
@app.get("/", response_class=HTMLResponse)
async def listar(request: Request):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM peliculas")
    peliculas = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return templates.TemplateResponse("pages/index.html", {
        "request": request,
        "peliculas": peliculas
    })

# --- CREATE: Agregar película ---
@app.post("/api/peliculas")
async def crear_pelicula(
    titulo: str = Form(...),
    genero: str = Form(...),
    año: int = Form(...),
    director: str = Form(...),
    precio: float = Form(...),
    duracion: int = Form(None),
    sinopsis: str = Form(None)
):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    sql = """INSERT INTO peliculas (titulo, genero, año, director, precio, duracion, sinopsis) 
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    valores = (titulo, genero, año, director, precio, duracion, sinopsis)
    
    cursor.execute(sql, valores)
    conn.commit()
    pelicula_id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return JSONResponse({"success": True, "id": pelicula_id, "message": "Película agregada exitosamente"})

# --- READ: Obtener una película por ID ---
@app.get("/api/peliculas/{pelicula_id}")
def obtener_pelicula(pelicula_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM peliculas WHERE id = %s", (pelicula_id,))
    pelicula = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if pelicula:
        return JSONResponse(pelicula)
    return JSONResponse({"error": "Película no encontrada"}, status_code=404)

# --- UPDATE: Editar película ---
@app.post("/api/peliculas/{pelicula_id}/editar")
async def editar_pelicula(
    pelicula_id: int,
    titulo: str = Form(...),
    genero: str = Form(...),
    año: int = Form(...),
    director: str = Form(...),
    precio: float = Form(...),
    duracion: int = Form(None),
    sinopsis: str = Form(None)
):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    sql = """UPDATE peliculas 
             SET titulo=%s, genero=%s, año=%s, director=%s, precio=%s, duracion=%s, sinopsis=%s 
             WHERE id=%s"""
    valores = (titulo, genero, año, director, precio, duracion, sinopsis, pelicula_id)
    
    cursor.execute(sql, valores)
    conn.commit()
    cursor.close()
    conn.close()
    
    return JSONResponse({"success": True, "message": "Película actualizada exitosamente"})

# --- DELETE: Eliminar película ---
@app.post("/api/peliculas/{pelicula_id}/eliminar")
async def eliminar_pelicula(pelicula_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM peliculas WHERE id = %s", (pelicula_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return JSONResponse({"success": True, "message": "Película eliminada exitosamente"})

# --- API: Obtener todas las películas (JSON) ---
@app.get("/api/peliculas")
def get_peliculas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM peliculas")
    peliculas = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return {"peliculas": peliculas, "total": len(peliculas)}