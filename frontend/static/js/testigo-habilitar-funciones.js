/**
 * Habilitar todas las funciones del testigo después de verificar mesa
 */

window.habilitarFuncionesTestigo = function() {
    console.log('🔓 Habilitando funciones del testigo...');
    
    // 1. Habilitar pestañas desktop
    const tabs = ['participacion-tab', 'formularios-tab', 'incidentes-tab', 'delitos-tab'];
    tabs.forEach(tabId => {
        const tab = document.getElementById(tabId);
        if (tab) {
            tab.classList.remove('disabled');
            tab.removeAttribute('disabled');
            console.log(`  ✅ Pestaña ${tabId} habilitada`);
        }
    });
    
    // 2. Habilitar navegación móvil
    const bottomNavItems = document.querySelectorAll('.bottom-nav-item');
    bottomNavItems.forEach(item => {
        item.classList.remove('disabled');
        item.style.pointerEvents = 'auto';
        item.style.opacity = '1';
    });
    console.log(`  ✅ Navegación móvil habilitada (${bottomNavItems.length} items)`);
    
    // 3. Habilitar botones de acción
    const botonesAccion = [
        'btnNuevoFormulario',
        'btnNuevoFormularioMobile'
    ];
    
    botonesAccion.forEach(btnId => {
        const btn = document.getElementById(btnId);
        if (btn) {
            btn.removeAttribute('disabled');
            btn.classList.remove('disabled');
            btn.title = '';
            console.log(`  ✅ Botón ${btnId} habilitado`);
        }
    });
    
    // 4. Actualizar alertas de verificación
    const alertNoVerificada = document.getElementById('alertMesaNoVerificada');
    const alertVerificada = document.getElementById('alertMesaVerificada');
    
    if (alertNoVerificada) {
        alertNoVerificada.classList.add('d-none');
    }
    if (alertVerificada) {
        alertVerificada.classList.remove('d-none');
    }
    
    // 5. Cambiar estilo de la card de verificación
    const verificacionCard = document.getElementById('verificacionMesaCard');
    if (verificacionCard) {
        verificacionCard.classList.remove('border-primary');
        verificacionCard.classList.add('border-success');
        const cardHeader = verificacionCard.querySelector('.card-header');
        if (cardHeader) {
            cardHeader.classList.remove('bg-primary');
            cardHeader.classList.add('bg-success');
        }
    }
    
    console.log('✅ Todas las funciones del testigo habilitadas');
};

window.deshabilitarFuncionesTestigo = function() {
    console.log('🔒 Deshabilitando funciones del testigo...');
    
    // 1. Deshabilitar pestañas desktop
    const tabs = ['participacion-tab', 'formularios-tab', 'incidentes-tab', 'delitos-tab'];
    tabs.forEach(tabId => {
        const tab = document.getElementById(tabId);
        if (tab) {
            tab.classList.add('disabled');
            tab.setAttribute('disabled', 'disabled');
        }
    });
    
    // 2. Deshabilitar navegación móvil
    const bottomNavItems = document.querySelectorAll('.bottom-nav-item');
    bottomNavItems.forEach(item => {
        item.classList.add('disabled');
        item.style.pointerEvents = 'none';
        item.style.opacity = '0.5';
    });
    
    // 3. Deshabilitar botones de acción
    const botonesAccion = [
        'btnNuevoFormulario',
        'btnNuevoFormularioMobile'
    ];
    
    botonesAccion.forEach(btnId => {
        const btn = document.getElementById(btnId);
        if (btn) {
            btn.setAttribute('disabled', 'disabled');
            btn.classList.add('disabled');
            btn.title = 'Debe verificar su mesa primero';
        }
    });
    
    // 4. Actualizar alertas
    const alertNoVerificada = document.getElementById('alertMesaNoVerificada');
    const alertVerificada = document.getElementById('alertMesaVerificada');
    
    if (alertNoVerificada) {
        alertNoVerificada.classList.remove('d-none');
    }
    if (alertVerificada) {
        alertVerificada.classList.add('d-none');
    }
    
    // 5. Restaurar estilo de la card
    const verificacionCard = document.getElementById('verificacionMesaCard');
    if (verificacionCard) {
        verificacionCard.classList.remove('border-success');
        verificacionCard.classList.add('border-primary');
        const cardHeader = verificacionCard.querySelector('.card-header');
        if (cardHeader) {
            cardHeader.classList.remove('bg-success');
            cardHeader.classList.add('bg-primary');
        }
    }
    
    console.log('✅ Funciones del testigo deshabilitadas');
};

// Verificar al cargar la página si ya hay una mesa verificada
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔍 Verificando estado de verificación al cargar...');
    
    const presenciaVerificada = localStorage.getItem('presenciaVerificada') === 'true';
    const mesaId = localStorage.getItem('mesaVerificadaId');
    
    if (presenciaVerificada && mesaId) {
        console.log('✅ Mesa ya verificada, habilitando funciones...');
        setTimeout(() => {
            habilitarFuncionesTestigo();
        }, 500);
    } else {
        console.log('⚠️ Mesa no verificada, funciones deshabilitadas');
        deshabilitarFuncionesTestigo();
    }
});

console.log('✅ Script de habilitación de funciones cargado');
