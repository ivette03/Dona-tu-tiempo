document.addEventListener('DOMContentLoaded', function () {
    var deleteButtons = document.querySelectorAll('.btn-delete-row');
    deleteButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            var elementId = button.getAttribute('data-element-id');
            var elementoAEliminar = document.getElementById('fila-' + elementId);
            if (elementoAEliminar) {
                elementoAEliminar.remove();
            }
            var mensajeEliminacionExitosa = document.getElementById('mensajeEliminacionExitosa');
            mensajeEliminacionExitosa.style.display = 'block';

            console.log('Eliminado exitosamente'); // Agrega esta línea para verificar si se ejecuta

            setTimeout(function () {
                mensajeEliminacionExitosa.style.display = 'none';
            }, 2000); // 2 segundos
        });
    });
});
