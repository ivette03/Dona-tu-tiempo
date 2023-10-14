document.addEventListener("DOMContentLoaded", function() {
  const enviarBtn = document.getElementById("btn-agg");

  // Obtiene la lista de días (ul) y sus elementos (li)
  const listaDias = document.querySelector(".day");
  const dias = listaDias.querySelectorAll("li");

  // Agrega un event listener a cada elemento de la lista de días (li)
  dias.forEach(dia => {
    dia.addEventListener("click", toggleSeleccion);
  });

  // Función para cambiar el estado de selección de un día
  function toggleSeleccion(event) {
    if (event.target.tagName === "LI") {
      const diaSeleccionado = event.target;
      diaSeleccionado.classList.toggle("selected");
    }
  }

  enviarBtn.addEventListener("click", function() {
    // Crear un array para almacenar los días seleccionados
    const diasSeleccionados = [];
    
    // Obtener todos los elementos con la clase "selected"
    const diasSeleccionadoslb = document.getElementsByClassName("selected");

    // Iterar sobre los elementos seleccionados y obtener sus atributos "data-day"
    for (let i = 0; i < diasSeleccionadoslb.length; i++) {
      diasSeleccionados.push(diasSeleccionadoslb[i].getAttribute("data-day"));
    }

    // Crear el formulario
    const form = document.getElementById("diasForm");

    // Crear un campo oculto para los días seleccionados
    const diasInput = document.createElement("input");
    diasInput.setAttribute("type", "hidden");
    diasInput.setAttribute("name", "dias_seleccionados");
    diasInput.setAttribute("value", JSON.stringify(diasSeleccionados));




    // Agregar el campo oculto al formulario
    form.appendChild(diasInput);

    // Enviar el formulario
    form.submit();
  });
});
