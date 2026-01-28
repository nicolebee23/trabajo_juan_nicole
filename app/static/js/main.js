let modalPelicula;

document.addEventListener("DOMContentLoaded", () => {
  modalPelicula = new bootstrap.Modal(document.getElementById("modalPelicula"));
});

function abrirModalAgregar() {
  document.getElementById("modalPeliculaLabel").textContent = "Agregar Película";
  document.getElementById("formPelicula").reset();
  document.getElementById("peliculaId").value = "";
  modalPelicula.show();
}

async function editarPelicula(id) {
  try {
    const response = await fetch(`/api/peliculas/${id}`);
    if (!response.ok) throw new Error("No se pudo obtener la película");
    const pelicula = await response.json();

    document.getElementById("peliculaId").value = pelicula.id;
    document.getElementById("titulo").value = pelicula.titulo;
    document.getElementById("genero").value = pelicula.genero;
    document.getElementById("año").value = pelicula.año;
    document.getElementById("director").value = pelicula.director;
    document.getElementById("precio").value = pelicula.precio;
    document.getElementById("duracion").value = pelicula.duracion || "";
    document.getElementById("sinopsis").value = pelicula.sinopsis || "";

    document.getElementById("modalPeliculaLabel").textContent = "Editar Película";
    modalPelicula.show();
  } catch (error) {
    alert(error.message);
  }
}

async function guardarPelicula() {
  const id = document.getElementById("peliculaId").value;
  const datos = {
    titulo: document.getElementById("titulo").value,
    genero: document.getElementById("genero").value,
    año: parseInt(document.getElementById("año").value),
    director: document.getElementById("director").value,
    precio: parseFloat(document.getElementById("precio").value),
    duracion: document.getElementById("duracion").value ? parseInt(document.getElementById("duracion").value) : null,
    sinopsis: document.getElementById("sinopsis").value,
  };

  const url = id ? `/api/peliculas/${id}` : "/api/peliculas";
  const metodo = id ? "PUT" : "POST";

  try {
    const response = await fetch(url, {
      method: metodo,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos),
    });

    if (response.ok) {
      location.reload();
    } else {
      alert("Error al guardar");
    }
  } catch (error) {
    console.error(error);
  }
}

async function eliminarPelicula(id) {
  if (!confirm("¿Eliminar esta película?")) return;
  try {
    const response = await fetch(`/api/peliculas/${id}`, { method: "DELETE" });
    if (response.ok) location.reload();
  } catch (error) {
    console.error(error);
  }
}