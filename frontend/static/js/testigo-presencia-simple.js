/**
 * Script simple para verificación de presencia y habilitación de botón
 */

// Función simple para verificar presencia
async function verificarPresencia() {
    console.log('🔄 Verificando presencia...');
    
    try {
        // Obtener mesa seleccionada
        const selectorMesa = document.getElementById('mesa');
        if (!selectorMesa || !selectorMesa.value) {
            alert('Debe seleccionar una mesa primero');
            return;
        }

        const selectedOption = selectorMesa.options[selectorMesa.selectedIndex];
        if (!selectedOption || !selectedOption.dataset.mesa) {
            alert('Error al obtener datos de la mesa');
            return;
        }

        const mesaData = JSON.parse(selectedOption.dataset.mesa);
        console.log('Mesa seleccionada:', mesaData);

        // Llamar al API
        const response = await fetch('/api/testigo/registrar-presencia', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('access_token')
            },
            body: JSON.stringify({
                mesa_id: mesaData.id
            })
        });

        const result = await response.json();
        console.log('Respuesta del servidor:', result);

        if (result.success) {
            console.log('✅ Presencia verificada');
            
            // Habilitar botón directamente
            const btnNuevoFormulario = document.getElementById('btnNuevoFormulario');
            if (btnNuevoFormulario) {
                btnNuevoFormulario.disabled = false;
                btnNuevoFormulario.classList.remove('disabled');
                btnNuevoFormulario.title = 'Crear nuevo formulario E-14';
                btnNuevoFormulario.style.opacity = '1';
                console.log('✅ Botón habilitado');
            } else {
                console.error('❌ No se encontró el botón');
            }

            // Ocultar botón de verificar presencia
            const btnVerificar = document.getElementById('btnVerificarPresencia');
            if (btnVerificar) {
                btnVerificar.style.display = 'none';
            }

            // Mostrar mensaje de confirmación
            const alertaPresencia = document.getElementById('alertaPresenciaVerificada');
            if (alertaPresencia) {
                alertaPresencia.classList.remove('d-none');
            }

            // Actualizar fecha
            const fechaElement = document.getElementById('presenciaFecha');
            if (fechaElement) {
                const ahora = new Date();
                const opciones = { 
                    timeZone: 'America/Bogota',
                    year: 'numeric',
                    month: '2-digit',
                    day: '2-digit',
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit',
                    hour12: false
                };
                fechaElement.textContent = `Verificada el ${ahora.toLocaleString('es-CO', opciones)}`;
            }

            alert('Presencia verificada exitosamente');
        } else {
            console.error('❌ Error:', result.error);
            alert('Error: ' + result.error);
        }
    } catch (error) {
        console.error('❌ Error en verificarPresencia:', error);
        alert('Error al verificar presencia: ' + error.message);
    }
}

// Asegurar que el botón esté deshabilitado al cargar
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Script de presencia cargado');
    
    const btnNuevoFormulario = document.getElementById('btnNuevoFormulario');
    if (btnNuevoFormulario) {
        btnNuevoFormulario.disabled = true;
        btnNuevoFormulario.classList.add('disabled');
        btnNuevoFormulario.style.opacity = '0.6';
        console.log('🔒 Botón deshabilitado inicialmente');
    }
});
