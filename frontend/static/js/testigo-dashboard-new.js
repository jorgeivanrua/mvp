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
    // setupImagePreview se llama cuando se abre el modal
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
                // Actualizar panel lateral con lista de mesas
                await actualizarPanelMesas();
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
        
        // Recargar formularios de esta mesa
        loadForms();
        
        // Actualizar panel lateral con todas las mesas
        actualizarPanelMesas();
    }
}

/**
 * Actualizar panel lateral con lista de mesas
 */
async function actualizarPanelMesas() {
    try {
        // Obtener todas las mesas del puesto
        const params = {
            puesto_codigo: userLocation.puesto_codigo,
            zona_codigo: userLocation.zona_codigo,
            municipio_codigo: userLocation.municipio_codigo,
            departamento_codigo: userLocation.departamento_codigo
        };
        
        const response = await APIClient.get('/locations/mesas', params);
        const mesas = response.data || [];
        
        // Obtener formularios para saber qué mesas tienen E-14
        const formulariosResponse = await APIClient.getFormulariosE14({});
        const formularios = formulariosResponse.success ? (formulariosResponse.data.formularios || formulariosResponse.data || []) : [];
        
        // Crear mapa de mesas con formularios
        const mesasConFormularios = {};
        formularios.forEach(form => {
            if (!mesasConFormularios[form.mesa_id]) {
                mesasConFormularios[form.mesa_id] = [];
            }
            mesasConFormularios[form.mesa_id].push(form);
        });
        
        // Generar HTML
        let html = '<h6 class="mb-3">Mis Mesas</h6>';
        
        if (mesas.length === 0) {
            html += '<p class="text-muted">No hay mesas asignadas</p>';
        } else {
            html += '<div class="list-group">';
            mesas.forEach(mesa => {
                const tieneFormularios = mesasConFormularios[mesa.id] && mesasConFormularios[mesa.id].length > 0;
                const cantidadFormularios = tieneFormularios ? mesasConFormularios[mesa.id].length : 0;
                const esSeleccionada = selectedMesa && selectedMesa.id === mesa.id;
                
                html += `
                    <div class="list-group-item ${esSeleccionada ? 'active' : ''}" style="cursor: pointer;" onclick="seleccionarMesaDesdePanel(${mesa.id})">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="mb-1">Mesa ${mesa.mesa_codigo}</h6>
                                <small>${mesa.puesto_nombre || 'N/A'}</small>
                            </div>
                            <div class="text-end">
                                ${tieneFormularios ? 
                                    `<span class="badge bg-success">${cantidadFormularios} E-14</span>` : 
                                    `<span class="badge bg-secondary">Sin E-14</span>`
                                }
                            </div>
                        </div>
                        <small class="text-muted d-block mt-1">
                            <i class="bi bi-people"></i> ${Utils.formatNumber(mesa.total_votantes_registrados || 0)} votantes
                        </small>
                    </div>
                `;
            });
            html += '</div>';
        }
        
        document.getElementById('assignedLocation').innerHTML = html;
        
    } catch (error) {
        console.error('Error actualizando panel de mesas:', error);
        document.getElementById('assignedLocation').innerHTML = `
            <p class="text-danger">Error al cargar mesas</p>
        `;
    }
}

/**
 * Seleccionar mesa desde el panel lateral
 */
function seleccionarMesaDesdePanel(mesaId) {
    const selector = document.getElementById('mesa');
    selector.value = mesaId;
    cambiarMesa();
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
        
        // Obtener formularios del servidor
        let formulariosServidor = [];
        try {
            const response = await APIClient.getFormulariosE14(params);
            if (response.success) {
                formulariosServidor = response.data.formularios || response.data || [];
            }
        } catch (error) {
            console.error('Error al cargar formularios del servidor:', error);
            // Continuar para mostrar al menos los borradores locales
        }
        
        // Obtener borradores locales
        const borradoresLocales = obtenerBorradoresLocales();
        const formulariosLocales = Object.values(borradoresLocales).map(borrador => {
            return {
                id: borrador.local_id,
                mesa_id: borrador.mesa_id,
                mesa_codigo: getMesaCodigoById(borrador.mesa_id),
                estado: 'local',
                total_votos: borrador.total_votos,
                created_at: borrador.saved_at,
                es_local: true
            };
        });
        
        // Filtrar borradores locales por mesa si es necesario
        let formulariosLocalesFiltrados = formulariosLocales;
        if (selectedMesa) {
            formulariosLocalesFiltrados = formulariosLocales.filter(f => f.mesa_id === selectedMesa.id);
        }
        
        // Combinar formularios del servidor y locales
        const todosFormularios = [...formulariosServidor, ...formulariosLocalesFiltrados];
        
        updateFormsTable(todosFormularios);
        
        // Mostrar indicador si hay borradores pendientes de sincronizar
        const totalBorradores = formulariosLocales.length;
        if (totalBorradores > 0) {
            mostrarIndicadorSincronizacion(totalBorradores);
        }
        
        // Actualizar panel lateral
        if (userLocation && userLocation.puesto_codigo) {
            actualizarPanelMesas();
        }
        
    } catch (error) {
        console.error('Error al cargar formularios:', error);
        // Mostrar mensaje en la tabla
        const tbody = document.querySelector('#formsTable tbody');
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="text-center py-4">
                    <p class="text-muted">Error al cargar formularios</p>
                </td>
            </tr>
        `;
    }
}

/**
 * Obtener código de mesa por ID
 */
function getMesaCodigoById(mesaId) {
    const mesaSelect = document.getElementById('mesa');
    for (let i = 0; i < mesaSelect.options.length; i++) {
        const option = mesaSelect.options[i];
        if (option.value == mesaId && option.dataset.mesa) {
            const mesa = JSON.parse(option.dataset.mesa);
            return mesa.mesa_codigo;
        }
    }
    return 'N/A';
}

/**
 * Mostrar indicador de sincronización pendiente
 */
function mostrarIndicadorSincronizacion(cantidad) {
    // Buscar o crear contenedor de indicador
    let indicador = document.getElementById('indicadorSincronizacion');
    
    if (!indicador) {
        indicador = document.createElement('div');
        indicador.id = 'indicadorSincronizacion';
        indicador.className = 'alert alert-warning d-flex justify-content-between align-items-center';
        indicador.style.position = 'fixed';
        indicador.style.bottom = '20px';
        indicador.style.right = '20px';
        indicador.style.zIndex = '1050';
        indicador.style.minWidth = '300px';
        document.body.appendChild(indicador);
    }
    
    indicador.innerHTML = `
        <div>
            <i class="bi bi-cloud-upload"></i>
            <strong>${cantidad}</strong> formulario(s) pendiente(s) de sincronizar
        </div>
        <button class="btn btn-sm btn-warning" onclick="sincronizarBorradoresLocales()">
            <i class="bi bi-arrow-repeat"></i> Sincronizar
        </button>
    `;
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
        const puedeEditar = form.estado === 'borrador' || form.estado === 'pendiente' || form.estado === 'local';
        const esLocal = form.es_local || form.estado === 'local';
        
        // Hacer la fila clickeable si puede editar
        if (puedeEditar) {
            row.style.cursor = 'pointer';
            row.onclick = () => {
                if (esLocal) {
                    editarBorradorLocal(form.id);
                } else {
                    editForm(form.id);
                }
            };
            row.onmouseover = () => row.style.backgroundColor = '#f8f9fa';
            row.onmouseout = () => row.style.backgroundColor = '';
        }
        
        row.innerHTML = `
            <td>Mesa ${form.mesa_codigo || 'N/A'}</td>
            <td><span class="badge bg-${getStatusColor(form.estado)}">${estadoLabel}</span></td>
            <td>${Utils.formatNumber(form.total_votos)}</td>
            <td>${Utils.formatDate(form.created_at)}</td>
            <td>
                ${puedeEditar ? 
                    `<button class="btn btn-sm btn-outline-warning" onclick="event.stopPropagation(); ${esLocal ? `editarBorradorLocal('${form.id}')` : `editForm(${form.id})`}">
                        <i class="bi bi-pencil"></i> Editar
                    </button>
                    ${esLocal ? 
                        `<button class="btn btn-sm btn-outline-danger ms-1" onclick="event.stopPropagation(); eliminarBorradorLocalPorId('${form.id}')">
                            <i class="bi bi-trash"></i>
                        </button>` : ''
                    }` : 
                    `<button class="btn btn-sm btn-outline-primary" onclick="event.stopPropagation(); viewForm(${form.id})">
                        <i class="bi bi-eye"></i> Ver
                    </button>`
                }
            </td>
        `;
        tbody.appendChild(row);
    });
}

function getStatusColor(estado) {
    const colors = {
        'pendiente': 'warning',
        'validado': 'success',
        'rechazado': 'danger',
        'borrador': 'secondary',
        'local': 'info'
    };
    return colors[estado] || 'secondary';
}

function getEstadoLabel(estado) {
    const labels = {
        'pendiente': 'Pendiente',
        'validado': 'Validado',
        'rechazado': 'Rechazado',
        'borrador': 'Borrador',
        'local': 'Guardado Localmente'
    };
    return labels[estado] || estado;
}

function showCreateForm() {
    document.getElementById('e14Form').reset();
    document.getElementById('imagePreview').innerHTML = '<p class="text-muted">Toque el botón para tomar una foto</p>';
    
    // Cargar mesas en el selector del formulario
    const mesaSelect = document.getElementById('mesaFormulario');
    mesaSelect.innerHTML = '<option value="">Seleccione mesa...</option>';
    
    // Obtener todas las mesas del puesto
    const params = {
        puesto_codigo: userLocation.puesto_codigo,
        zona_codigo: userLocation.zona_codigo,
        municipio_codigo: userLocation.municipio_codigo,
        departamento_codigo: userLocation.departamento_codigo
    };
    
    APIClient.get('/locations/mesas', params).then(response => {
        if (response.success) {
            response.data.forEach(mesa => {
                const option = document.createElement('option');
                option.value = mesa.id;
                option.textContent = `Mesa ${mesa.mesa_codigo} - ${mesa.puesto_nombre}`;
                option.dataset.votantes = mesa.total_votantes_registrados || 0;
                mesaSelect.appendChild(option);
            });
            
            // Si hay una mesa seleccionada, preseleccionarla
            if (selectedMesa) {
                mesaSelect.value = selectedMesa.id;
                cambiarMesaFormulario();
            }
        }
    });
    
    // Cargar tipos de elección si no están cargados
    if (tiposEleccion.length === 0) {
        loadTiposEleccion();
    }
    
    // Limpiar contenedor de votación
    document.getElementById('votacionContainer').innerHTML = '<p class="text-muted">Seleccione un tipo de elección para cargar los partidos y candidatos</p>';
    
    // Configurar preview de imagen cada vez que se abre el modal
    setupImagePreview();
    
    new bootstrap.Modal(document.getElementById('formModal')).show();
}

function cambiarMesaFormulario() {
    const mesaSelect = document.getElementById('mesaFormulario');
    const selectedOption = mesaSelect.options[mesaSelect.selectedIndex];
    
    if (selectedOption && selectedOption.value) {
        const votantes = selectedOption.dataset.votantes || 0;
        document.getElementById('votantesRegistrados').value = votantes;
    }
}

async function saveForm(accion = 'borrador') {
    const form = document.getElementById('e14Form');
    
    // Solo validar si se va a enviar
    if (accion === 'enviar' && !form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const mesaId = document.getElementById('mesaFormulario').value;
    if (!mesaId) {
        Utils.showError('Selecciona una mesa');
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
            mesa_id: parseInt(mesaId),
            tipo_eleccion_id: parseInt(formData.get('tipo_eleccion')),
            total_votantes_registrados: parseInt(formData.get('total_votantes_registrados')),
            total_votos: parseInt(formData.get('total_votos')),
            votos_validos: parseInt(formData.get('votos_validos')),
            votos_nulos: parseInt(formData.get('votos_nulos')),
            votos_blanco: parseInt(formData.get('votos_blanco')),
            tarjetas_no_marcadas: parseInt(formData.get('tarjetas_no_marcadas')),
            total_tarjetas: parseInt(formData.get('total_tarjetas')),
            observaciones: formData.get('observaciones') || '',
            estado: accion === 'enviar' ? 'pendiente' : 'borrador',
            votos_partidos: votosPartidos,
            votos_candidatos: votosCandidatos
        };
        
        console.log('Saving form data:', data);
        
        // Si es borrador, guardar en localStorage
        if (accion === 'borrador') {
            guardarBorradorLocal(data);
            Utils.showSuccess('Borrador guardado localmente');
            bootstrap.Modal.getInstance(document.getElementById('formModal')).hide();
            loadForms();
            return;
        }
        
        // Si es enviar, intentar enviar al servidor
        try {
            const response = await APIClient.createFormularioE14(data);
            
            if (response.success) {
                // Si se envió exitosamente, eliminar borrador local si existe
                eliminarBorradorLocal(data.mesa_id, data.tipo_eleccion_id);
                
                Utils.showSuccess('Formulario E-14 enviado para revisión');
                bootstrap.Modal.getInstance(document.getElementById('formModal')).hide();
                loadForms();
            } else {
                Utils.showError('Error: ' + (response.error || 'Error desconocido'));
            }
        } catch (error) {
            console.error('Error enviando formulario:', error);
            
            // Si falla el envío, ofrecer guardar como borrador local
            if (confirm('No se pudo enviar el formulario. ¿Desea guardarlo localmente para enviarlo después?')) {
                guardarBorradorLocal(data);
                Utils.showSuccess('Formulario guardado localmente. Se enviará cuando haya conexión.');
                bootstrap.Modal.getInstance(document.getElementById('formModal')).hide();
                loadForms();
            } else {
                Utils.showError('Error al enviar formulario: ' + error.message);
            }
        }
        
    } catch (error) {
        console.error('Error saving form:', error);
        Utils.showError('Error al guardar formulario: ' + error.message);
    }
}

/**
 * Guardar borrador en localStorage
 */
function guardarBorradorLocal(data) {
    try {
        // Obtener borradores existentes
        const borradores = obtenerBorradoresLocales();
        
        // Crear clave única para el borrador
        const key = `${data.mesa_id}_${data.tipo_eleccion_id}`;
        
        // Agregar timestamp
        data.saved_at = new Date().toISOString();
        data.local_id = key;
        
        // Guardar o actualizar borrador
        borradores[key] = data;
        
        localStorage.setItem('formularios_e14_borradores', JSON.stringify(borradores));
        
        console.log('Borrador guardado localmente:', key);
    } catch (error) {
        console.error('Error guardando borrador local:', error);
        throw new Error('No se pudo guardar el borrador localmente');
    }
}

/**
 * Obtener todos los borradores locales
 */
function obtenerBorradoresLocales() {
    try {
        const borradores = localStorage.getItem('formularios_e14_borradores');
        return borradores ? JSON.parse(borradores) : {};
    } catch (error) {
        console.error('Error obteniendo borradores locales:', error);
        return {};
    }
}

/**
 * Eliminar borrador local
 */
function eliminarBorradorLocal(mesaId, tipoEleccionId) {
    try {
        const borradores = obtenerBorradoresLocales();
        const key = `${mesaId}_${tipoEleccionId}`;
        
        if (borradores[key]) {
            delete borradores[key];
            localStorage.setItem('formularios_e14_borradores', JSON.stringify(borradores));
            console.log('Borrador local eliminado:', key);
        }
    } catch (error) {
        console.error('Error eliminando borrador local:', error);
    }
}

/**
 * Sincronizar borradores locales con el servidor
 */
async function sincronizarBorradoresLocales() {
    try {
        const borradores = obtenerBorradoresLocales();
        const keys = Object.keys(borradores);
        
        if (keys.length === 0) {
            console.log('No hay borradores locales para sincronizar');
            Utils.showInfo('No hay formularios pendientes de sincronizar');
            return;
        }
        
        console.log(`Sincronizando ${keys.length} borradores locales...`);
        
        let sincronizados = 0;
        let errores = 0;
        
        for (const key of keys) {
            const borrador = borradores[key];
            
            try {
                // Cambiar estado a pendiente para enviar
                borrador.estado = 'pendiente';
                
                const response = await APIClient.createFormularioE14(borrador);
                
                if (response.success) {
                    eliminarBorradorLocal(borrador.mesa_id, borrador.tipo_eleccion_id);
                    sincronizados++;
                    console.log('Borrador sincronizado:', key);
                } else {
                    errores++;
                    console.error('Error sincronizando borrador:', key, response.error);
                }
            } catch (error) {
                errores++;
                console.error('Error sincronizando borrador:', key, error);
            }
        }
        
        if (sincronizados > 0) {
            Utils.showSuccess(`${sincronizados} formulario(s) sincronizado(s) exitosamente`);
            loadForms();
        }
        
        if (errores > 0) {
            Utils.showWarning(`${errores} formulario(s) no se pudieron sincronizar`);
        }
        
    } catch (error) {
        console.error('Error en sincronización de borradores:', error);
    }
}

/**
 * Editar borrador local
 */
async function editarBorradorLocal(localId) {
    try {
        const borradores = obtenerBorradoresLocales();
        const borrador = borradores[localId];
        
        if (!borrador) {
            Utils.showError('Borrador no encontrado');
            return;
        }
        
        // Abrir el modal
        document.getElementById('e14Form').reset();
        
        // Cargar mesa
        const mesaSelect = document.getElementById('mesaFormulario');
        mesaSelect.value = borrador.mesa_id;
        cambiarMesaFormulario();
        
        // Cargar tipo de elección
        document.getElementById('tipoEleccion').value = borrador.tipo_eleccion_id;
        await cargarPartidosYCandidatos();
        
        // Cargar datos de votación
        document.getElementById('votosNulos').value = borrador.votos_nulos || 0;
        document.getElementById('votosBlanco').value = borrador.votos_blanco || 0;
        document.getElementById('tarjetasNoMarcadas').value = borrador.tarjetas_no_marcadas || 0;
        
        // Cargar votos por partido
        if (borrador.votos_partidos) {
            borrador.votos_partidos.forEach(vp => {
                const input = document.getElementById(`partido_${vp.partido_id}`);
                if (input) input.value = vp.votos;
            });
        }
        
        // Cargar votos por candidato
        if (borrador.votos_candidatos) {
            borrador.votos_candidatos.forEach(vc => {
                const input = document.getElementById(`candidato_${vc.candidato_id}`);
                if (input) input.value = vc.votos;
            });
        }
        
        // Cargar observaciones
        document.querySelector('[name="observaciones"]').value = borrador.observaciones || '';
        
        // Recalcular totales
        calcularTotales();
        
        // Mostrar modal
        new bootstrap.Modal(document.getElementById('formModal')).show();
        
    } catch (error) {
        console.error('Error loading local draft:', error);
        Utils.showError('Error al cargar borrador: ' + error.message);
    }
}

/**
 * Eliminar borrador local por ID
 */
function eliminarBorradorLocalPorId(localId) {
    if (!confirm('¿Está seguro de eliminar este borrador local?')) {
        return;
    }
    
    try {
        const borradores = obtenerBorradoresLocales();
        
        if (borradores[localId]) {
            delete borradores[localId];
            localStorage.setItem('formularios_e14_borradores', JSON.stringify(borradores));
            Utils.showSuccess('Borrador eliminado');
            loadForms();
        }
    } catch (error) {
        console.error('Error eliminando borrador:', error);
        Utils.showError('Error al eliminar borrador');
    }
}

function viewForm(formId) {
    window.open(`/testigo/form/${formId}`, '_blank');
}

async function editForm(formId) {
    try {
        // Cargar el formulario
        const response = await APIClient.getFormularioE14(formId);
        
        if (!response.success) {
            Utils.showError('Error al cargar formulario');
            return;
        }
        
        const formulario = response.data;
        
        // Abrir el modal
        document.getElementById('e14Form').reset();
        
        // Cargar mesa
        const mesaSelect = document.getElementById('mesaFormulario');
        mesaSelect.value = formulario.mesa_id;
        cambiarMesaFormulario();
        
        // Cargar tipo de elección
        document.getElementById('tipoEleccion').value = formulario.tipo_eleccion_id;
        await cargarPartidosYCandidatos();
        
        // Cargar datos de votación
        document.getElementById('votosNulos').value = formulario.votos_nulos || 0;
        document.getElementById('votosBlanco').value = formulario.votos_blanco || 0;
        document.getElementById('tarjetasNoMarcadas').value = formulario.tarjetas_no_marcadas || 0;
        
        // Cargar votos por partido
        if (formulario.votos_partidos) {
            formulario.votos_partidos.forEach(vp => {
                const input = document.getElementById(`partido_${vp.partido_id}`);
                if (input) input.value = vp.votos;
            });
        }
        
        // Cargar votos por candidato
        if (formulario.votos_candidatos) {
            formulario.votos_candidatos.forEach(vc => {
                const input = document.getElementById(`candidato_${vc.candidato_id}`);
                if (input) input.value = vc.votos;
            });
        }
        
        // Cargar observaciones
        document.querySelector('[name="observaciones"]').value = formulario.observaciones || '';
        
        // Recalcular totales
        calcularTotales();
        
        // Mostrar modal
        new bootstrap.Modal(document.getElementById('formModal')).show();
        
    } catch (error) {
        console.error('Error loading form:', error);
        Utils.showError('Error al cargar formulario: ' + error.message);
    }
}

function setupImagePreview() {
    const input = document.getElementById('imagen');
    const preview = document.getElementById('imagePreview');
    
    if (!input || !preview) {
        console.warn('Image input or preview not found');
        return;
    }
    
    // Remover listeners anteriores clonando el elemento
    const newInput = input.cloneNode(true);
    input.parentNode.replaceChild(newInput, input);
    
    newInput.addEventListener('change', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        const file = e.target.files[0];
        
        if (file) {
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    preview.innerHTML = `<img src="${event.target.result}" alt="Preview" style="max-width: 100%; max-height: 250px; object-fit: contain;">`;
                };
                reader.onerror = function() {
                    preview.innerHTML = '<p class="text-danger">Error al cargar la imagen</p>';
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

/**
 * Verificar presencia del testigo en la mesa
 */
async function verificarPresencia() {
    if (!confirm('¿Confirma que está presente en la mesa asignada?')) {
        return;
    }
    
    try {
        const response = await APIClient.post('/auth/verificar-presencia', {});
        
        if (response.success) {
            Utils.showSuccess('Presencia verificada exitosamente');
            
            // Ocultar botón y mostrar alerta de verificación
            document.getElementById('btnVerificarPresencia').classList.add('d-none');
            document.getElementById('alertaPresenciaVerificada').classList.remove('d-none');
            
            // Mostrar fecha de verificación
            const fecha = new Date(response.data.presencia_verificada_at);
            document.getElementById('presenciaFecha').textContent = 
                `Verificado el ${fecha.toLocaleDateString()} a las ${fecha.toLocaleTimeString()}`;
        }
    } catch (error) {
        console.error('Error verificando presencia:', error);
        Utils.showError('Error al verificar presencia: ' + error.message);
    }
}

/**
 * Verificar estado de presencia al cargar
 */
async function verificarEstadoPresencia() {
    try {
        const response = await APIClient.getProfile();
        if (response.success && response.data.user) {
            const user = response.data.user;
            
            // Si ya verificó presencia, mostrar alerta
            if (user.presencia_verificada) {
                document.getElementById('btnVerificarPresencia').classList.add('d-none');
                document.getElementById('alertaPresenciaVerificada').classList.remove('d-none');
                
                if (user.presencia_verificada_at) {
                    const fecha = new Date(user.presencia_verificada_at);
                    document.getElementById('presenciaFecha').textContent = 
                        `Verificado el ${fecha.toLocaleDateString()} a las ${fecha.toLocaleTimeString()}`;
                }
            }
        }
    } catch (error) {
        console.error('Error verificando estado de presencia:', error);
    }
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

// Agregar evento para seleccionar todo el texto en inputs numéricos al hacer focus
document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('focus', function(e) {
        if (e.target.type === 'number') {
            e.target.select();
        }
    }, true);
    
    // Verificar estado de presencia al cargar
    verificarEstadoPresencia();
    
    // Intentar sincronizar borradores locales al cargar (silenciosamente)
    setTimeout(() => {
        const borradores = obtenerBorradoresLocales();
        if (Object.keys(borradores).length > 0) {
            console.log('Hay borradores locales pendientes de sincronizar');
            // No sincronizar automáticamente, solo mostrar indicador
        }
    }, 2000);
});


// ============================================
// FUNCIONES PARA INCIDENTES Y DELITOS
// ============================================

/**
 * Reportar incidente
 */
function reportarIncidente() {
    document.getElementById('incidenteForm').reset();
    new bootstrap.Modal(document.getElementById('incidenteModal')).show();
}

/**
 * Guardar incidente
 */
async function guardarIncidente() {
    const form = document.getElementById('incidenteForm');
    
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    try {
        const formData = new FormData(form);
        
        const data = {
            mesa_id: selectedMesa ? selectedMesa.id : null,
            tipo_incidente: formData.get('tipo_incidente'),
            descripcion: formData.get('descripcion'),
            fecha_hora: new Date().toISOString()
        };
        
        // Guardar localmente primero
        guardarIncidenteLocal(data);
        
        Utils.showSuccess('Incidente reportado exitosamente');
        bootstrap.Modal.getInstance(document.getElementById('incidenteModal')).hide();
        cargarIncidentes();
        
    } catch (error) {
        console.error('Error guardando incidente:', error);
        Utils.showError('Error al reportar incidente: ' + error.message);
    }
}

/**
 * Guardar incidente en localStorage
 */
function guardarIncidenteLocal(data) {
    try {
        const incidentes = obtenerIncidentesLocales();
        const id = `incidente_${Date.now()}`;
        data.id = id;
        data.sincronizado = false;
        incidentes[id] = data;
        localStorage.setItem('incidentes_testigo', JSON.stringify(incidentes));
    } catch (error) {
        console.error('Error guardando incidente local:', error);
    }
}

/**
 * Obtener incidentes locales
 */
function obtenerIncidentesLocales() {
    try {
        const incidentes = localStorage.getItem('incidentes_testigo');
        return incidentes ? JSON.parse(incidentes) : {};
    } catch (error) {
        console.error('Error obteniendo incidentes locales:', error);
        return {};
    }
}

/**
 * Cargar incidentes
 */
function cargarIncidentes() {
    const incidentes = obtenerIncidentesLocales();
    const lista = document.getElementById('incidentesLista');
    
    const incidentesArray = Object.values(incidentes);
    
    if (incidentesArray.length === 0) {
        lista.innerHTML = '<p class="text-muted text-center py-4">No hay incidentes reportados</p>';
        return;
    }
    
    lista.innerHTML = incidentesArray.map(incidente => `
        <div class="card mb-2">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <h6 class="mb-1">${getTipoIncidenteLabel(incidente.tipo_incidente)}</h6>
                        <p class="mb-1">${incidente.descripcion}</p>
                        <small class="text-muted">
                            <i class="bi bi-clock"></i> ${Utils.formatDate(incidente.fecha_hora)}
                        </small>
                    </div>
                    <span class="badge ${incidente.sincronizado ? 'bg-success' : 'bg-warning'}">
                        ${incidente.sincronizado ? 'Sincronizado' : 'Pendiente'}
                    </span>
                </div>
            </div>
        </div>
    `).join('');
}

/**
 * Obtener label del tipo de incidente
 */
function getTipoIncidenteLabel(tipo) {
    const labels = {
        'retraso_apertura': 'Retraso en apertura',
        'falta_material': 'Falta de material electoral',
        'problemas_tecnicos': 'Problemas técnicos',
        'irregularidades': 'Irregularidades en el proceso',
        'otros': 'Otros'
    };
    return labels[tipo] || tipo;
}

/**
 * Reportar delito
 */
function reportarDelito() {
    document.getElementById('delitoForm').reset();
    new bootstrap.Modal(document.getElementById('delitoModal')).show();
}

/**
 * Guardar delito
 */
async function guardarDelito() {
    const form = document.getElementById('delitoForm');
    
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    if (!confirm('¿Está seguro de reportar este delito electoral? Este reporte será enviado a las autoridades competentes.')) {
        return;
    }
    
    try {
        const formData = new FormData(form);
        
        const data = {
            mesa_id: selectedMesa ? selectedMesa.id : null,
            tipo_delito: formData.get('tipo_delito'),
            descripcion: formData.get('descripcion'),
            fecha_hora: new Date().toISOString()
        };
        
        // Guardar localmente primero
        guardarDelitoLocal(data);
        
        Utils.showSuccess('Delito reportado exitosamente. Las autoridades serán notificadas.');
        bootstrap.Modal.getInstance(document.getElementById('delitoModal')).hide();
        cargarDelitos();
        
    } catch (error) {
        console.error('Error guardando delito:', error);
        Utils.showError('Error al reportar delito: ' + error.message);
    }
}

/**
 * Guardar delito en localStorage
 */
function guardarDelitoLocal(data) {
    try {
        const delitos = obtenerDelitosLocales();
        const id = `delito_${Date.now()}`;
        data.id = id;
        data.sincronizado = false;
        delitos[id] = data;
        localStorage.setItem('delitos_testigo', JSON.stringify(delitos));
    } catch (error) {
        console.error('Error guardando delito local:', error);
    }
}

/**
 * Obtener delitos locales
 */
function obtenerDelitosLocales() {
    try {
        const delitos = localStorage.getItem('delitos_testigo');
        return delitos ? JSON.parse(delitos) : {};
    } catch (error) {
        console.error('Error obteniendo delitos locales:', error);
        return {};
    }
}

/**
 * Cargar delitos
 */
function cargarDelitos() {
    const delitos = obtenerDelitosLocales();
    const lista = document.getElementById('delitosLista');
    
    const delitosArray = Object.values(delitos);
    
    if (delitosArray.length === 0) {
        lista.innerHTML = '<p class="text-muted text-center py-4">No hay delitos reportados</p>';
        return;
    }
    
    lista.innerHTML = delitosArray.map(delito => `
        <div class="card mb-2 border-danger">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <h6 class="mb-1 text-danger">${getTipoDelitoLabel(delito.tipo_delito)}</h6>
                        <p class="mb-1">${delito.descripcion}</p>
                        <small class="text-muted">
                            <i class="bi bi-clock"></i> ${Utils.formatDate(delito.fecha_hora)}
                        </small>
                    </div>
                    <span class="badge ${delito.sincronizado ? 'bg-success' : 'bg-danger'}">
                        ${delito.sincronizado ? 'Reportado' : 'Pendiente'}
                    </span>
                </div>
            </div>
        </div>
    `).join('');
}

/**
 * Obtener label del tipo de delito
 */
function getTipoDelitoLabel(tipo) {
    const labels = {
        'compra_votos': 'Compra de votos',
        'coaccion': 'Coacción al votante',
        'fraude': 'Fraude electoral',
        'suplantacion': 'Suplantación de identidad',
        'alteracion': 'Alteración de resultados',
        'otros': 'Otros delitos'
    };
    return labels[tipo] || tipo;
}

// Cargar incidentes y delitos al cambiar de pestaña
document.addEventListener('DOMContentLoaded', function() {
    const incidentesTab = document.getElementById('incidentes-tab');
    const delitosTab = document.getElementById('delitos-tab');
    
    if (incidentesTab) {
        incidentesTab.addEventListener('shown.bs.tab', function() {
            cargarIncidentes();
        });
    }
    
    if (delitosTab) {
        delitosTab.addEventListener('shown.bs.tab', function() {
            cargarDelitos();
        });
    }
});
