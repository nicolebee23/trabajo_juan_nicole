let modalPelicula;

document.addEventListener("DOMContentLoaded", () => {
  modalPelicula = new bootstrap.Modal(document.getElementById("modalPelicula"));
});

// ---------- Funciones de errores ----------

// Muestra los errores que devuelve Pydantic dentro del modal
function mostrarErrores(errores) {
  const divError = document.getElementById("divError");
  const listaErrores = document.getElementById("listaErrores");
  listaErrores.innerHTML = errores.map((e) => `<li>${e}</li>`).join("");
  divError.classList.remove("d-none");
}

// Esconde el bloque de errores
function limpiarErrores() {
  const divError = document.getElementById("divError");
  const listaErrores = document.getElementById("listaErrores");
  listaErrores.innerHTML = "";
  divError.classList.add("d-none");
}

// ---------- Modal: Agregar ----------

function abrirModalAgregar() {
  document.getElementById("modalPeliculaLabel").textContent = "Agregar Película";
  document.getElementById("formPelicula").reset();
  document.getElementById("peliculaId").value = "";
  limpiarErrores();
  modalPelicula.show();
}

// ---------- Modal: Editar ----------

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
    limpiarErrores();
    modalPelicula.show();
  } catch (error) {
    alert(error.message);
  }
}

// ---------- Guardar (crear o actualizar) ----------

async function guardarPelicula() {
  // Validación HTML5 del formulario antes de enviar
  const form = document.getElementById("formPelicula");
  if (!form.reportValidity()) return;

  // Limpiar cualquier error anterior
  limpiarErrores();

  const id = document.getElementById("peliculaId").value;
  const datos = {
    titulo: document.getElementById("titulo").value,
    genero: document.getElementById("genero").value,
    año: parseInt(document.getElementById("año").value),
    director: document.getElementById("director").value,
    precio: parseFloat(document.getElementById("precio").value),
    // Si duración está vacía, envía null (campo opcional)
    duracion: document.getElementById("duracion").value
      ? parseInt(document.getElementById("duracion").value)
      : null,
    // Si sinopsis está vacía, envía null (campo opcional)
    sinopsis: document.getElementById("sinopsis").value || null,
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
      // Todo bien → recarga la página para ver los cambios
      location.reload();
    } else if (response.status === 422) {
      // Error de validación de Pydantic → muestra los mensajes
      const errorData = await response.json();
      mostrarErrores(errorData.errores);
    } else {
      // Otro error inesperado
      mostrarErrores(["Error inesperado al guardar la película"]);
    }
  } catch (error) {
    console.error(error);
    mostrarErrores(["Error de conexión. Verifica que el servidor esté activo."]);
  }
}

// ---------- Eliminar ----------

async function eliminarPelicula(id) {
  if (!confirm("¿Eliminar esta película?")) return;
  try {
    const response = await fetch(`/api/peliculas/${id}`, { method: "DELETE" });
    if (response.ok) location.reload();
  } catch (error) {
    console.error(error);
  }
}