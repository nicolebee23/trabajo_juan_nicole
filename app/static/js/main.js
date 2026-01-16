let modoEdicion = false;
let peliculaIdActual = null;

// Abrir modal para agregar
function abrirModalAgregar() {
  modoEdicion = false;
  peliculaIdActual = null;
  document.getElementById("modalPeliculaLabel").innerHTML =
    '<i class="bi bi-film me-2"></i>Agregar Película';
  document.getElementById("formPelicula").reset();
  document.getElementById("peliculaId").value = "";
}

// Editar película
async function editarPelicula(id) {
  modoEdicion = true;
  peliculaIdActual = id;

  try {
    const response = await fetch(`/api/peliculas/${id}`);
    const pelicula = await response.json();

    document.getElementById("peliculaId").value = pelicula.id;
    document.getElementById("titulo").value = pelicula.titulo;
    document.getElementById("genero").value = pelicula.genero;
    document.getElementById("año").value = pelicula.año;
    document.getElementById("director").value = pelicula.director;
    document.getElementById("precio").value = pelicula.precio;
    document.getElementById("duracion").value = pelicula.duracion || "";
    document.getElementById("sinopsis").value = pelicula.sinopsis || "";

    document.getElementById("modalPeliculaLabel").innerHTML =
      '<i class="bi bi-pencil-square me-2"></i>Editar Película';

    const modal = new bootstrap.Modal(document.getElementById("modalPelicula"));
    modal.show();
  } catch (error) {
    alert("Error al cargar la película");
    console.error(error);
  }
}

// Guardar película (crear o actualizar)
async function guardarPelicula() {
  const form = document.getElementById("formPelicula");

  if (!form.checkValidity()) {
    form.reportValidity();
    return;
  }

  const formData = new FormData(form);
  let url, metodo;

  if (modoEdicion) {
    url = `/api/peliculas/${peliculaIdActual}/editar`;
    metodo = "POST";
  } else {
    url = "/api/peliculas";
    metodo = "POST";
  }

  try {
    const response = await fetch(url, {
      method: metodo,
      body: formData,
    });

    const data = await response.json();

    if (data.success) {
      alert(data.message);
      location.reload(); // Recargar la página para ver los cambios
    } else {
      alert("Error al guardar la película");
    }
  } catch (error) {
    alert("Error al guardar la película");
    console.error(error);
  }
}

// Eliminar película
async function eliminarPelicula(id) {
  if (!confirm("¿Estás seguro de que deseas eliminar esta película?")) {
    return;
  }

  try {
    const response = await fetch(`/api/peliculas/${id}/eliminar`, {
      method: "POST",
    });

    const data = await response.json();

    if (data.success) {
      alert(data.message);
      location.reload(); // Recargar la página para ver los cambios
    } else {
      alert("Error al eliminar la película");
    }
  } catch (error) {
    alert("Error al eliminar la película");
    console.error(error);
  }
}