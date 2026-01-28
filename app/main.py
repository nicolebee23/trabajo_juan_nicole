from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import mysql.connector

app = FastAPI(title="MovieLand API")

db_config = {
    "host": "localhost",
    "user": "movieland_user",
    "password": "movieland1234",
    "database": "movieland_db"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Modelo para recibir datos JSON
class Pelicula(BaseModel):
    titulo: str
    genero: str
    año: int
    director: str
    precio: float
    duracion: int = None
    sinopsis: str = None

@app.get("/", response_class=HTMLResponse)
async def listar(request: Request):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM peliculas ORDER BY id DESC")
    peliculas = cursor.fetchall()
    cursor.close()
    conn.close()
    return templates.TemplateResponse("pages/index.html", {"request": request, "peliculas": peliculas})

# Obtener una película por ID (para rellenar el modal)
@app.get("/api/peliculas/{pelicula_id}")
async def obtener_pelicula(pelicula_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM peliculas WHERE id = %s", (pelicula_id,))
    pelicula = cursor.fetchone()
    cursor.close()
    conn.close()
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return pelicula

@app.post("/api/peliculas")
async def crear_pelicula(pelicula: Pelicula):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO peliculas (titulo, genero, año, director, precio, duracion, sinopsis) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (pelicula.titulo, pelicula.genero, pelicula.año, pelicula.director, pelicula.precio, pelicula.duracion, pelicula.sinopsis))
    conn.commit()
    cursor.close()
    conn.close()
    return {"success": True, "message": "Película agregada"}

@app.put("/api/peliculas/{pelicula_id}")
async def actualizar_pelicula(pelicula_id: int, pelicula: Pelicula):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "UPDATE peliculas SET titulo=%s, genero=%s, año=%s, director=%s, precio=%s, duracion=%s, sinopsis=%s WHERE id=%s"
    cursor.execute(sql, (pelicula.titulo, pelicula.genero, pelicula.año, pelicula.director, pelicula.precio, pelicula.duracion, pelicula.sinopsis, pelicula_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"success": True, "message": "Película actualizada"}

@app.delete("/api/peliculas/{pelicula_id}")
async def eliminar_pelicula(pelicula_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM peliculas WHERE id = %s", (pelicula_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"success": True, "message": "Película eliminada"}