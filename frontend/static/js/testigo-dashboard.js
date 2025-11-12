/**
 * Dashboard del Testigo Electoral
 */
let currentUser = null;
let userLocation = null;
let selectedMesa = null;

document.addEventListener('DOMContentLoaded', function() {
    loadUserProfile();
    loadForms();
    
    // Configurar preview de imagen
    setupImagePreview();
});

async function loadUserProfile() {
    try {
        const response = await APIClient.getProfile();
        if (response.success) {
            currentUser = response.data;
            userLocation = response.data.ubicacion;
            
            // Cargar mesas disponibles
            if (userLocation && userLocation.puesto_codigo) {
                await loadMesas(userLocation.puesto_codigo);
            }
            
            // Mostrar información de la ubicación asignada
            if (userLocation) {
                document.getElementById('assignedLocation').innerHTML = `
                    <h6>${userLocation.puesto_nombre || userLocation.nombre_completo}</h6>
                    <p class="text-muted mb-1">Código: ${userLocation.puesto_codigo || 'N/A'}</p>
                    <p class="mb-0">Dirección: ${userLocation.direccion || 'N/A'}</p>
                `;
            }
        }
    } catch (error) {
        console.error('Error al cargar perfil:', error);
        Utils.showError('Error al cargar perfil: ' + error.message);
    }
}

async function loadMesas(puestoCodigo) {
    try {
        const response = await APIClient.getMesas(puestoCodigo);
        const mesas = response.data;
        
        const selector = document.getElementById('mesa');
        selector.innerHTML = '<option value="">Seleccione mesa...</option>';
        
        mesas.forEach(mesa => {
            const option = document.createElement('option');
            option.value = mesa.id;
            option.textContent = `Mesa ${mesa.mesa_codigo} - ${mesa.mesa_nombre || 'Sin nombre'}`;
            option.dataset.mesa = JSON.stringify(mesa);
            selector.appendChild(option);
        });
        
        // Si solo hay una mesa, seleccionarla automáticamente
        if (mesas.length === 1) {
            selector.value = mesas[0].id;
            cambiarMesa();
        }
    } catch (error) {
        console.error('Error loading mesas:', error);
        Utils.showError('Error cargando mesas del puesto');
    }
}

function cambiarMesa() {
    const selector = document.getElementById('mesa');
    const selectedOption = selector.options[selector.selectedIndex];
    
    if (selectedOption && selectedOption.dataset.mesa) {
        selectedMesa = JSON.parse(selectedOption.dataset.mesa);
        
        // Actualizar información de la mesa
        document.getElementById('assignedLocation').innerHTML = `
            <h6>${selectedMesa.mesa_nombre || selectedMesa.nombre_completo}</h6>
            <p class="text-muted mb-1">Mesa: ${selectedMesa.mesa_codigo}</p>
            <p class="text-muted mb-1">Puesto: ${selectedMesa.puesto_nombre || 'N/A'}</p>
            <p class="mb-0">Votantes registrados: ${Utils.formatNumber(selectedMesa.total_votantes_registrados || 0)}</p>
        `;
        
        // Recargar formularios de esta mesa
        loadForms();
    }
}

async function loadForms() {
    try {
        const response = await APIClient.getFormulariosE14();
        
        if (response.success) {
            updateFormsTable(response.data);
        } else {
            Utils.showError('Error al cargar formularios');
        }
    } catch (error) {
        console.error('Error al cargar formularios:', error);
        Utils.showError('Error al cargar formularios: ' + error.message);
    }
}

function updateFormsTable(forms) {
    const tbody = document.querySelector('#formsTable tbody');
    tbody.innerHTML = '';
    
    if (forms.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="text-center py-4">
                    <p class="text-muted">No hay formularios registrados</p>
                </td>
            </tr>
        `;
        return;
    }
    
    forms.forEach(form => {
        const row = document.createElement('tr');
        const estadoLabel = getEstadoLabel(form.estado);
        row.innerHTML = `
            <td>${form.tipo_eleccion_nombre || 'N/A'}</td>
            <td><span class="badge bg-${getStatusColor(form.estado)}">${estadoLabel}</span></td>
            <td>${Utils.formatNumber(form.total_votos)}</td>
            <td>${Utils.formatDate(form.created_at)}</td>
            <td>
                <button class="btn btn-sm btn-outline-primary" onclick="viewForm(${form.id})">Ver</button>
                ${form.estado === 'pendiente' ? `<button class="btn btn-sm btn-outline-warning" onclick="editForm(${form.id})">Editar</button>` : ''}
            </td>
        `;
        tbody.appendChild(row);
    });
}

function getStatusColor(estado) {
    const colors = {
        'pendiente': 'warning',
        'validado': 'success',
        'rechazado': 'danger'
    };
    return colors[estado] || 'secondary';
}

function getEstadoLabel(estado) {
    const labels = {
        'pendiente': 'Pendiente',
        'validado': 'Validado',
        'rechazado': 'Rechazado'
    };
    return labels[estado] || estado;
}

function showCreateForm() {
    // Verificar que haya una mesa seleccionada
    if (!selectedMesa) {
        Utils.showWarning('Por favor selecciona una mesa primero');
        return;
    }
    
    document.getElementById('e14Form').reset();
    document.getElementById('imagePreview').innerHTML = '<p class="text-muted">Seleccione una imagen del formulario E-14</p>';
    
    // Agregar campos básicos de partidos
    const container = document.getElementById('partidosContainer');
    container.innerHTML = '';
    addPartido();
    addPartido();
    
    new bootstrap.Modal(document.getElementById('formModal')).show();
}

function addPartido() {
    const container = document.getElementById('partidosContainer');
    const index = container.children.length;
    
    const div = document.createElement('div');
    div.className = 'row mb-2';
    div.innerHTML = `
        <div class="col-md-6">
            <input type="text" class="form-control" placeholder="Nombre del partido" name="partido_nombre_${index}">
        </div>
        <div class="col-md-4">
            <input type="number" class="form-control" placeholder="Votos" name="partido_votos_${index}" min="0" value="0">
        </div>
        <div class="col-md-2">
            <button type="button" class="btn btn-sm btn-outline-danger" onclick="this.parentElement.parentElement.remove()">
                Eliminar
            </button>
        </div>
    `;
    
    container.appendChild(div);
}

async function saveForm() {
    const form = document.getElementById('e14Form');
    
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    try {
        // Recopilar datos básicos
        const formData = new FormData(form);
        
        // Recopilar votos por partido
        const votosPartidos = [];
        document.querySelectorAll('input[name^="partido_"]').forEach(input => {
            const partidoId = parseInt(input.name.replace('partido_', ''));
            const votos = parseInt(input.value) || 0;
            
            if (votos > 0) {
                votosPartidos.push({
                    partido_id: partidoId,
                    votos: votos
                });
            }
        });
        
        // Recopilar votos por candidato
        const votosCandidatos = [];
        document.querySelectorAll('input[name^="candidato_"]').forEach(input => {
            const candidatoId = parseInt(input.name.replace('candidato_', ''));
            const votos = parseInt(input.value) || 0;
            
            if (votos > 0) {
                votosCandidatos.push({
                    candidato_id: candidatoId,
                    votos: votos
                });
            }
        });
        
        // Construir objeto de datos
        const data = {
            mesa_id: selectedMesa.id,
            tipo_eleccion_id: parseInt(formData.get('tipo_eleccion')),
            hora_apertura: formData.get('hora_apertura'),
            hora_cierre: formData.get('hora_cierre'),
            total_votantes_registrados: parseInt(formData.get('total_votantes_registrados')),
            total_votos: parseInt(formData.get('total_votos')),
            votos_validos: parseInt(formData.get('votos_validos')),
            votos_nulos: parseInt(formData.get('votos_nulos')),
            votos_blanco: parseInt(formData.get('votos_blanco')),
            tarjetas_no_marcadas: parseInt(formData.get('tarjetas_no_marcadas')),
            total_tarjetas: parseInt(formData.get('total_tarjetas')),
            observaciones: formData.get('observaciones') || '',
            votos_partidos: votosPartidos,
            votos_candidatos: votosCandidatos
        };
        
        // TODO: Manejar imagen del formulario
        // Por ahora solo guardamos los datos sin imagen
        
        const response = await APIClient.createFormularioE14(data);
        
        if (response.success) {
            Utils.showSuccess('Formulario E-14 guardado exitosamente');
            bootstrap.Modal.getInstance(document.getElementById('formModal')).hide();
            loadForms();
        } else {
            Utils.showError('Error: ' + response.message);
        }
        
    } catch (error) {
        console.error('Error saving form:', error);
        Utils.showError('Error al guardar formulario: ' + error.message);
    }
}

async function submitForm(formId) {
    if (!confirm('¿Está seguro de enviar este formulario para revisión? No podrá editarlo después.')) {
        return;
    }
    
    try {
        // TODO: Implementar endpoint real
        // const response = await APIClient.post(`/e14/forms/${formId}/submit`, {});
        
        Utils.showSuccess('Formulario enviado para revisión');
        loadForms();
    } catch (error) {
        Utils.showError('Error al enviar formulario: ' + error.message);
    }
}

function viewForm(formId) {
    // Implementar vista de formulario
    window.open(`/testigo/form/${formId}`, '_blank');
}

function editForm(formId) {
    // Implementar edición de formulario
    Utils.showInfo('Función de edición en desarrollo');
}

function setupImagePreview() {
    const input = document.getElementById('imagen');
    const preview = document.getElementById('imagePreview');
    
    input.addEventListener('change', function(e) {
        const file = e.target.files[0];
        
        if (file) {
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
                };
                reader.readAsDataURL(file);
            } else if (file.type === 'application/pdf') {
                preview.innerHTML = `
                    <div class="text-center">
                        <i class="bi bi-file-pdf" style="font-size: 3rem; color: #dc3545;"></i>
                        <p class="mt-2">${file.name}</p>
                    </div>
                `;
            }
        } else {
            preview.innerHTML = '<p class="text-muted">Seleccione una imagen del formulario E-14</p>';
        }
    });
}

// Función global para logout
async function logout() {
    try {
        await APIClient.logout();
    } catch (error) {
        console.error('Error during logout:', error);
    } finally {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user_data');
        window.location.href = '/login';
    }
}
