const btnadd = document.getElementById("btn-add");
const modal = document.getElementById("cmodal");

btnadd.addEventListener("click", () => {
    modal.classList.add("active");
});

// close modal if click outside modal
window.addEventListener("click", (e) => {
  if (e.target == modal) {
    modal.classList.remove("active");
  } else if (e.target == editModal) {
    editModal.classList.remove("active");
  }
});

// close modal if press the x button
const closebtn = document.querySelector(".close-btn");
closebtn.addEventListener("click", () => {
  modal.classList.remove("active");
});

const cancelModalBtn = document.querySelector(".btn-cancel");
cancelModalBtn.addEventListener("click", () => {
  modal.classList.remove("active");
});

let urlactual = window.location.href;
const partesURL = urlactual.split('?buscar=');
const apiUrl = partesURL[0];


const editRowBtn = document.querySelectorAll(".btn-edit-row");
editRowBtn.forEach((btn) => {
  btn.addEventListener("click", (event) => {
    const recordId = event.currentTarget.dataset.id;

    fetch(`${apiUrl}${recordId}`, { method: "GET" })
      .then((response) => response.json())
      .then((data) => {

        editModalForm.elements["cedula"].value = data.info_personal.cedula;
        editModalForm.elements["nombres"].value = data.info_personal.nombres;
        editModalForm.elements["apellidos"].value = data.info_personal.apellidos;
        editModalForm.elements["celular"].value = data.info_personal.celular;
        editModalForm.elements["correo"].value = data.info_personal.correo;
        editModalForm.elements["profesion"].value = data.profesion;

        editModalForm.dataset.id = recordId;

        editModal.classList.add("active");
      });
  });
});





const closeEditModalBtn = document.querySelector(".close-edit-btn");
closeEditModalBtn.addEventListener("click", () => {
  editModal.classList.remove("active");
});

const deleteRowBtn = document.querySelectorAll(".btn-delete-row");
deleteRowBtn.forEach((btn) => {
  const recordId = btn.dataset.id;
  btn.addEventListener("click", () => {
    const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    const headers = new Headers();
    headers.append("Content-Type", "application/json");
    headers.append("X-CSRFToken", csrfToken);
    fetch(`${apiUrl}${recordId}`, {
      method: "DELETE",
      headers: headers
    }).then(response => {
      location.reload();
    })
  });
});

const editModal = document.getElementById("edit-modal");

const editModalForm = document.getElementById("edit-modal-form");

document.getElementById("edit-modal-form").addEventListener("submit", function(event) {
  console.log("ejecutando")
  event.preventDefault(); // Evitar el envío del formulario por defecto
  const url_actual = window.location.href;
  const partesURL = url_actual.split('?buscar=');
  const apiUrl = partesURL[0];
  const recordId = event.target.dataset.id;

  // Obtener los datos del formulario y convertirlos a JSON
  const formData = new FormData(document.getElementById("edit-modal-form"));
  const jsonData = {};
  for (let [key, value] of formData) {
    jsonData[key] = value;
  }
  const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
  // Convertir los datos a JSON y establecer el encabezado "Content-Type"
  const body = JSON.stringify(jsonData);
  const headers = new Headers();
  headers.append("Content-Type", "application/json");
  headers.append("X-CSRFToken", csrfToken);

  fetch(`${apiUrl + recordId.toString()}`, {
    method: "PUT",
    body: body,
    headers: headers
  }).then(response => {
    location.reload();
  })
  editModal.classList.remove("active");
});
