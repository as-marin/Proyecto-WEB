document.addEventListener('DOMContentLoaded', function() {
    var cantidadInput = document.getElementById('idcantidad');

    cantidadInput.addEventListener('change', function() {
        var cantidad = parseInt(cantidadInput.value);

        if (cantidad <= 0 || cantidad > 9) {
            cantidadInput.value = ''; // Limpiar el campo si es menor o igual a 0
        }
    });
});