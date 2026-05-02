(function($) {
    'use strict';

    let lastValue = "";

    function fillUserData(userId) {
        if (!userId || userId === "" || userId === "0") {
            $('#id_nombres, #id_apellidos, #id_grado, #id_seccion').val('');
            return;
        }
        
        console.log(">>> [POLLING ACTION] Cargando datos para Usuario ID:", userId);
        
        $.ajax({
            url: window.location.origin + `/auth/api/user-data/${userId}/`,
            method: 'GET',
            dataType: 'json',
            success: function(data) {
                console.log(">>> [AJAX SUCCESS] Datos:", data);
                $('#id_nombres').val(data.nombres || '');
                $('#id_apellidos').val(data.apellidos || '');
                $('#id_grado').val(data.grado || '');
                $('#id_seccion').val(data.seccion || '');
            },
            error: function(xhr) {
                console.error(">>> [AJAX ERROR] Status:", xhr.status);
            }
        });
    }

    function checkValueChange() {
        const userSelect = $('#id_user');
        if (userSelect.length === 0) return;

        const currentValue = userSelect.val();
        
        // Si el valor actual es diferente al último que procesamos
        if (currentValue !== lastValue) {
            console.log(">>> [POLLING] Cambio de valor detectado:", lastValue, "->", currentValue);
            lastValue = currentValue;
            fillUserData(currentValue);
        }
    }

    $(document).ready(function() {
        console.log("--- Admin Profile Autocomplete (v6 - Polling System) cargado ---");
        
        // Inicializar el valor actual (para evitar disparar al cargar si ya tiene valor)
        lastValue = $('#id_user').val() || "";

        // Revisar el valor cada 500 milisegundos (2 veces por segundo)
        // Esto es infalible porque no depende de que Select2 dispare eventos.
        setInterval(checkValueChange, 500);
        
        // Verificación rápida de los campos de destino
        console.log("Estado de campos destino:", {
            nombres: $('#id_nombres').length > 0,
            apellidos: $('#id_apellidos').length > 0,
            grado: $('#id_grado').length > 0,
            seccion: $('#id_seccion').length > 0
        });
    });

})(django.jQuery || jQuery);
