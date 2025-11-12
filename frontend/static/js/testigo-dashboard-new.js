/**
 * Dashboard del Testigo Electoral - Versión Completa
 */
let currentUser = null;
let userLocation = null;
let selectedMesa = null;
let tiposEleccion = [];
let partidosData = [];
let candidatosData = [];
let votosData = {};

document.addEventListener('DOMContentLoaded', function() {
    loadUserProfile();
    loadForms();
    loadTiposEleccion();
    setupImagePreview();
});

async function loadUserProfile() {
    try {
        const response = await APIClient.getProfile();
        if (response.success) {
            currentUser = response.data.user;
            userLocation = response.data.ubicacion;
            
            console.log('User profile loaded:', currentUser);
            console.log('User location:', userLocation);
            
            // Cargar mesas disponibles del puesto
            if (userLocation && userLocation.puesto_codigo) {
                await loadMesas();
            }
            
            // Mostrar información de la ubicación asignada
            if (userLocation) {
                document.getElementById('assignedLocation').innerHTML = `
                    <h6>${userLocation.puesto_nombre || userLocation.nombre_completo}</h6>
                    <p class="text-muted mb-1">Código: ${userLocation.puesto_codigo || 'N/A'}</p>
                    <p class="mb-0">Dirección: ${userLocation.direccion || 'N/A'}</p>
                `;
            } else {
                document.getElementById('assignedLocation').innerHTML = `
                    <p class="text-muted">No hay ubicación asignada</p>
                `;
            }
        }
    } catch (error) {
        console.error('Error al cargar perfil:', error);
        Utils.showError('Error al cargar perfil: ' + error.message);
    }
}

async function loadMesas() {
    try {
        const params = {
            puesto_codigo: userLocation.puesto_codigo,
            zona_codigo: userLocation.zona_codigo,
            municipio_codigo: userLocation.municipio_codigo,
            departamento_codigo: userLocation.departamento_codigo
        };
        
        console.log('Loading mesas with params:', params);
        
        const response = await APIClient.get('/locations/mesas', params);
        const mesas = response.data;
        
        console.log('Mesas loaded:', mesas);
        
        const selector = document.getElementById('mesa');
        selector.innerHTML = '<option value="">Seleccione mesa...</option>';
        
        mesas.forEach(mesa => {
            const option = document.createElement('option');
            option.value = mesa.id;
            option.textContent = `Mesa ${mesa.mesa_codigo} - ${mesa.puesto_nombre}`;
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

async function loadTiposEleccion() {
    try {
        const response = await APIClient.getTiposEleccion();
        if (response.success) {
            tiposEleccion = response.data;
            const select = document.getElementById('tipoEleccion');
            select.innerHTML = '<option value="">Seleccione...</option>';
            
            tiposEleccion.forEach(tipo => {
                const option = document.createElement('option');
                option.value = tipo.id;
                option.textContent = tipo.nombre;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading tipos eleccion:', error);
    }
}

async function cargarPartidosYCandidatos() {
    const tipoEleccionId = document.getElementById('tipoEleccion').value;
    
    if (!tipoEleccionId) {
        document.getElementById('votacionContainer').innerHTML = '<p class="text-muted">Seleccione un tipo de elección</p>';
        return;
    }
    
    try {
        console.log('Cargando datos para tipo de elección:', tipoEleccionId);
        
        // Cargar partidos
        const partidosResponse = await APIClient.getPartidos();
        partidosData = partidosResponse.success ? partidosResponse.data : [];
        console.log('Partidos cargados:', partidosData);
        
        // Cargar candidatos del tipo de elección
        const candidatosResponse = await APIClient.getCandidatos({ tipo_eleccion_id: tipoEleccionId });
        console.log('Respuesta de candidatos:', candidatosResponse);
        candidatosData = candidatosResponse.success ? candidatosResponse.data : [];
        console.log('Candidatos cargados:', candidatosData);
        
        if (candidatosData.length === 0) {
            console.warn('No se encontraron candidatos para el tipo de elección:', tipoEleccionId);
        }
        
        // Agrupar candidatos por partido
        const candidatosPorPartido = {};
        candidatosData.forEach(candidato => {
            if (!candidatosPorPartido[candidato.partido_id]) {
                candidatosPorPartido[candidato.partido_id] = [];
            }
            candidatosPorPartido[candidato.partido_id].push(candidato);
        });
        console.log('Candidatos agrupados por partido:', candidatosPorPartido);
        
        // Renderizar formulario de votación
        renderVotacionForm(partidosData, candidatosPorPartido);
        
    } catch (error) {
        console.error('Error loading partidos y candidatos:', error);
        Utils.showError('Error cargando datos de votación: ' + error.message);
    }
}

function renderVotacionForm(partidos, candidatosPorPartido) {
    const container = document.getElementById('votacionContainer');
    container.innerHTML = '';
    
    votosData = {};
    
    // Verificar si es elección uninominal
    const tipoEleccionSelect = document.getElementById('tipoEleccion');
    const selectedOption = tipoEleccionSelect.options[tipoEleccionSelect.selectedIndex];
    const tipoEleccion = tiposEleccion.find(t => t.id == tipoEleccionSelect.value);
    const esUninominal = tipoEleccion?.es_uninominal || false;
    
    partidos.forEach(partido => {
        const partidoDiv = document.createElement('div');
        partidoDiv.className = 'card mb-3';
        partidoDiv.style.borderLeft = `4px solid ${partido.color || '#6c757d'}`;
        
        const candidatos = candidatosPorPartido[partido.id] || [];
        
        if (esUninominal) {
            // Elección uninominal: un candidato por partido, sin votos de partido
            const candidato = candidatos[0];
            
            partidoDiv.innerHTML = `
                <div class="card-header" style="background-color: ${partido.color}20;">
                    <div class="row align-items-center">
                        <div class="col-md-8">
                            <h6 class="mb-0">${partido.nombre}</h6>
                            ${candidato ? `<p class="mb-0 small"><strong>Candidato:</strong> ${candidato.nombre_completo}</p>` : '<p class="mb-0 small text-muted">Sin candidato</p>'}
                        </div>
                        <div class="col-md-4">
                            <label class="form-label mb-1 small">Votos</label>
                            <input type="number" 
                                   class="form-control form-control-sm" 
                                   id="${candidato ? `candidato_${candidato.id}` : `partido_${partido.id}`}" 
                                   min="0" 
                                   value="0"
                                   onchange="calcularTotales()"
                                   placeholder="0">
                        </div>
                    </div>
                </div>
            `;
        } else {
            // Elección por listas: múltiples candidatos + votos de partido
            partidoDiv.innerHTML = `
                <div class="card-header" style="background-color: ${partido.color}20;">
                    <div class="row align-items-center">
                        <div class="col-8">
                            <h6 class="mb-0">${partido.nombre}</h6>
                            <small class="text-muted">${partido.nombre_corto}</small>
                        </div>
                        <div class="col-4 text-end">
                            <label class="form-label mb-1 small d-block">Votos solo partido</label>
                            <input type="number" 
                                   class="form-control form-control-sm text-center" 
                                   id="partido_${partido.id}" 
                                   min="0" 
                                   value="0"
                                   onchange="calcularTotales()"
                                   placeholder="0"
                                   style="max-width: 80px; margin-left: auto;">
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <div class="row g-2">
                        ${candidatos.map((candidato, idx) => `
                            <div class="col-12 mb-1">
                                <div class="row align-items-center">
                                    <div class="col-1 text-center">
                                        <span class="badge bg-secondary">${candidato.numero_lista || idx + 1}</span>
                                    </div>
                                    <div class="col-8">
                                        <small class="fw-medium">${candidato.nombre_completo}</small>
                                    </div>
                                    <div class="col-3 text-end">
                                        <input type="number" 
                                               class="form-control form-control-sm text-center" 
                                               id="candidato_${candidato.id}" 
                                               min="0" 
                                               value="0"
                                               onchange="calcularTotales()"
                                               placeholder="0"
                                               style="max-width: 80px; margin-left: auto;">
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                    ${candidatos.length === 0 ? '<p class="text-muted mb-0 small">No hay candidatos registrados para este partido</p>' : ''}
                    <div class="mt-2 pt-2 border-top">
                        <div class="row align-items-center">
                            <div class="col-8">
                                <strong>Total ${partido.nombre_corto}:</strong>
                            </div>
                            <div class="col-4 text-end">
                                <span id="total_partido_${partido.id}" class="badge bg-primary fs-6">0</span>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }
        
        container.appendChild(partidoDiv);
        
        // Inicializar datos de votos
        votosData[partido.id] = {
            partido: partido,
            votosPartido: 0,
            candidatos: candidatos.map(c => ({ ...c, votos: 0 })),
            total: 0,
            esUninominal: esUninominal
        };
    });
    
    // Agregar opción de voto en blanco
    const votoBlancoDiv = document.createElement('div');
    votoBlancoDiv.className = 'card mb-3';
    votoBlancoDiv.style.borderLeft = '4px solid #6c757d';
    votoBlancoDiv.innerHTML = `
        <div class="card-header" style="background-color: #f8f9fa;">
            <div class="row align-items-center">
                <div class="col-md-8">
                    <h6 class="mb-0">Voto en Blanco</h6>
                    <small class="text-muted">Votos sin candidato específico</small>
                </div>
                <div class="col-md-4">
                    <label class="form-label mb-1 small">Votos</label>
                    <input type="number" 
                           class="form-control form-control-sm" 
                           id="voto_blanco" 
                           min="0" 
                           value="0"
                           onchange="calcularTotales()"
                           placeholder="0">
                </div>
            </div>
        </div>
    `;
    container.appendChild(votoBlancoDiv);
    
    calcularTotales();
}

function calcularTotales() {
    let votosValidos = 0;
    let maxVotosPartido = 0;
    let partidoGanador = null;
    
    // Calcular por cada partido
    Object.keys(votosData).forEach(partidoId => {
        const data = votosData[partidoId];
        
        // Votos del partido
        const inputPartido = document.getElementById(`partido_${partidoId}`);
        const votosPartido = parseInt(inputPartido?.value || 0);
        data.votosPartido = votosPartido;
        
        // Votos de candidatos
        let votosCandidatos = 0;
        data.candidatos.forEach(candidato => {
            const inputCandidato = document.getElementById(`candidato_${candidato.id}`);
            const votos = parseInt(inputCandidato?.value || 0);
            candidato.votos = votos;
            votosCandidatos += votos;
        });
        
        // Total del partido (votos partido + votos candidatos)
        data.total = votosPartido + votosCandidatos;
        votosValidos += data.total;
        
        // Actualizar display del total del partido
        const totalSpan = document.getElementById(`total_partido_${partidoId}`);
        if (totalSpan) {
            totalSpan.textContent = Utils.formatNumber(data.total);
        }
        
        // Verificar partido con más votos en esta mesa
        if (data.total > maxVotosPartido) {
            maxVotosPartido = data.total;
            partidoGanador = data.partido;
        }
    });
    
    // Obtener otros valores
    const votosNulos = parseInt(document.getElementById('votosNulos')?.value || 0);
    const votosBlanco = parseInt(document.getElementById('votosBlanco')?.value || 0);
    const tarjetasNoMarcadas = parseInt(document.getElementById('tarjetasNoMarcadas')?.value || 0);
    
    // Calcular totales
    const totalVotos = votosValidos + votosNulos + votosBlanco;
    const totalTarjetas = totalVotos + tarjetasNoMarcadas;
    
    // Actualizar campos automáticos
    document.getElementById('votosValidos').value = votosValidos;
    document.getElementById('totalVotos').value = totalVotos;
    document.getElementById('totalTarjetas').value = totalTarjetas;
    
    // Actualizar resumen
    document.getElementById('resumenTotal').textContent = Utils.formatNumber(votosValidos);
    document.getElementById('partidoGanador').textContent = partidoGanador ? 
        `${partidoGanador.nombre_corto} (${Utils.formatNumber(maxVotosPartido)} votos)` : '-';
}

async function loadForms() {
    try {
        const params = selectedMesa ? { mesa_id: selectedMesa.id } : {};
        const response = await APIClient.getFormulariosE14(params);
        
        if (response.success) {
            updateFormsTable(response.data);
        } else {
            Utils.showError('Error al cargar formularios');
        }
    } catch (error) {
        console.error('Error al cargar formularios:', error);
        // No mostrar error si es porque no hay endpoint aún
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
            <td>Mesa ${form.mesa_codigo || 'N/A'}</td>
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
    document.getElementById('imagePreview').innerHTML = '<p class="text-muted">Toque el botón para tomar una foto</p>';
    
    // Establecer mesa asignada
    document.getElementById('mesaAsignada').value = `Mesa ${selectedMesa.mesa_codigo} - ${selectedMesa.puesto_nombre}`;
    document.getElementById('mesaId').value = selectedMesa.id;
    
    // Cargar votantes registrados de la mesa
    const votantesRegistrados = selectedMesa.total_votantes_registrados || 0;
    document.getElementById('votantesRegistrados').value = votantesRegistrados;
    
    // Cargar tipos de elección si no están cargados
    if (tiposEleccion.length === 0) {
        loadTiposEleccion();
    }
    
    // Limpiar contenedor de votación
    document.getElementById('votacionContainer').innerHTML = '<p class="text-muted">Seleccione un tipo de elección para cargar los partidos y candidatos</p>';
    
    new bootstrap.Modal(document.getElementById('formModal')).show();
}

async function saveForm() {
    const form = document.getElementById('e14Form');
    
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    if (!selectedMesa) {
        Utils.showError('No hay mesa seleccionada');
        return;
    }
    
    try {
        const formData = new FormData(form);
        
        // Construir datos de votos por partido y candidato
        const votosPartidos = [];
        const votosCandidatos = [];
        
        Object.keys(votosData).forEach(partidoId => {
            const data = votosData[partidoId];
            
            // Votos del partido
            if (data.votosPartido > 0) {
                votosPartidos.push({
                    partido_id: parseInt(partidoId),
                    votos: data.votosPartido
                });
            }
            
            // Votos de candidatos
            data.candidatos.forEach(candidato => {
                if (candidato.votos > 0) {
                    votosCandidatos.push({
                        candidato_id: candidato.id,
                        votos: candidato.votos
                    });
                }
            });
        });
        
        // Construir objeto de datos
        const data = {
            mesa_id: selectedMesa.id,
            tipo_eleccion_id: parseInt(formData.get('tipo_eleccion')),
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
        
        console.log('Saving form data:', data);
        
        // TODO: Implementar upload de imagen
        // Por ahora solo guardamos los datos
        
        const response = await APIClient.createFormularioE14(data);
        
        if (response.success) {
            Utils.showSuccess('Formulario E-14 guardado exitosamente');
            bootstrap.Modal.getInstance(document.getElementById('formModal')).hide();
            loadForms();
        } else {
            Utils.showError('Error: ' + (response.error || 'Error desconocido'));
        }
        
    } catch (error) {
        console.error('Error saving form:', error);
        Utils.showError('Error al guardar formulario: ' + error.message);
    }
}

function viewForm(formId) {
    window.open(`/testigo/form/${formId}`, '_blank');
}

function editForm(formId) {
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
                    preview.innerHTML = `<img src="${e.target.result}" alt="Preview" style="max-width: 100%; max-height: 400px;">`;
                };
                reader.readAsDataURL(file);
            } else {
                preview.innerHTML = '<p class="text-danger">Por favor seleccione una imagen válida</p>';
            }
        } else {
            preview.innerHTML = '<p class="text-muted">Toque el botón para tomar una foto</p>';
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
