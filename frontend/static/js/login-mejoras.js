/**
 * Mejoras UI/UX para Login Page
 * Mobile-first responsive design
 */

(function() {
    'use strict';

    // ============================================
    // HAPTIC FEEDBACK
    // ============================================
    
    function addHapticFeedback() {
        const touchElements = document.querySelectorAll('.form-select, .form-control, .btn-login, .btn-outline-secondary');
        
        touchElements.forEach(element => {
            element.addEventListener('focus', function() {
                // Vibración deshabilitada para evitar advertencias de Chrome
                // if (navigator.vibrate) {
                //     navigator.vibrate(5);
                // }
            });
            
            if (element.classList.contains('btn-login') || element.classList.contains('btn-outline-secondary')) {
                element.addEventListener('click', function() {
                    // Vibración deshabilitada para evitar advertencias de Chrome
                    // if (navigator.vibrate) {
                    //     navigator.vibrate(10);
                    // }
                });
            }
        });
    }

    // ============================================
    // ANIMACIONES DE ENTRADA
    // ============================================
    
    function initAnimations() {
        const card = document.querySelector('.login-card');
        if (card) {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.6s ease-out';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 100);
        }
    }

    // ============================================
    // VALIDACIÓN VISUAL
    // ============================================
    
    function initValidation() {
        const form = document.getElementById('loginForm');
        if (!form) return;
        
        const inputs = form.querySelectorAll('.form-select, .form-control');
        
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.value && this.checkValidity()) {
                    this.classList.add('is-valid');
                    this.classList.remove('is-invalid');
                } else if (this.value) {
                    this.classList.add('is-invalid');
                    this.classList.remove('is-valid');
                }
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid') && this.checkValidity()) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                }
            });
        });
    }

    // ============================================
    // MEJORAR TOGGLE PASSWORD
    // ============================================
    
    function enhancePasswordToggle() {
        const toggleBtn = document.getElementById('togglePassword');
        const passwordInput = document.getElementById('password');
        const eyeIcon = document.getElementById('eyeIcon');
        
        console.log('🔍 Inicializando toggle de contraseña...');
        console.log('Toggle button:', toggleBtn);
        console.log('Password input:', passwordInput);
        console.log('Eye icon:', eyeIcon);
        
        if (toggleBtn && passwordInput && eyeIcon) {
            // Remover cualquier listener previo
            toggleBtn.replaceWith(toggleBtn.cloneNode(true));
            const newToggleBtn = document.getElementById('togglePassword');
            
            newToggleBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                console.log('👁️ Toggle password clicked');
                
                const currentType = passwordInput.getAttribute('type');
                const newType = currentType === 'password' ? 'text' : 'password';
                
                console.log('Cambiando tipo de:', currentType, 'a:', newType);
                
                passwordInput.setAttribute('type', newType);
                
                // Cambiar icono
                const eyeIcon = document.getElementById('eyeIcon');
                if (newType === 'text') {
                    eyeIcon.classList.remove('bi-eye');
                    eyeIcon.classList.add('bi-eye-slash');
                    newToggleBtn.setAttribute('aria-label', 'Ocultar contraseña');
                    console.log('👁️ Contraseña visible - icono cambiado a eye-slash');
                } else {
                    eyeIcon.classList.remove('bi-eye-slash');
                    eyeIcon.classList.add('bi-eye');
                    newToggleBtn.setAttribute('aria-label', 'Mostrar contraseña');
                    console.log('👁️ Contraseña oculta - icono cambiado a eye');
                }
                
                // Mantener el foco en el input de contraseña
                passwordInput.focus();
            });
            
            console.log('✅ Toggle de contraseña configurado correctamente');
        } else {
            console.error('❌ No se pudieron encontrar los elementos del toggle de contraseña');
        }
    }

    // ============================================
    // LOADING STATE
    // ============================================
    
    function enhanceLoadingState() {
        const form = document.getElementById('loginForm');
        const loginBtn = document.getElementById('loginBtn');
        const loginText = document.getElementById('loginText');
        const loginSpinner = document.getElementById('loginSpinner');
        
        if (form && loginBtn) {
            form.addEventListener('submit', function(e) {
                // Deshabilitar botón
                loginBtn.disabled = true;
                loginBtn.style.opacity = '0.7';
                
                // Mostrar spinner
                if (loginText) loginText.textContent = 'Iniciando...';
                if (loginSpinner) loginSpinner.classList.remove('d-none');
                
                // Vibración deshabilitada para evitar advertencias de Chrome
                // if (navigator.vibrate) {
                //     navigator.vibrate([10, 50, 10]);
                // }
            });
        }
    }

    // ============================================
    // AUTO-FOCUS
    // ============================================
    
    function initAutoFocus() {
        const rolSelect = document.getElementById('rol');
        if (rolSelect && window.innerWidth > 768) {
            // Solo en desktop
            setTimeout(() => {
                rolSelect.focus();
            }, 700);
        }
    }

    // ============================================
    // MEJORAR SELECTS EN MÓVIL
    // ============================================
    
    function enhanceMobileSelects() {
        if (window.innerWidth <= 768) {
            const selects = document.querySelectorAll('.form-select');
            selects.forEach(select => {
                // Agregar atributo para mejor UX en móvil
                select.setAttribute('autocomplete', 'off');
            });
        }
    }

    // ============================================
    // TOAST NOTIFICATIONS
    // ============================================
    
    function showToast(message, type = 'info') {
        const alertContainer = document.getElementById('alert-container');
        if (!alertContainer) return;
        
        const iconMap = {
            'success': 'check-circle-fill',
            'error': 'x-circle-fill',
            'warning': 'exclamation-triangle-fill',
            'info': 'info-circle-fill'
        };
        
        const colorMap = {
            'success': 'success',
            'error': 'danger',
            'warning': 'warning',
            'info': 'info'
        };
        
        const alert = document.createElement('div');
        alert.className = `alert alert-${colorMap[type]} alert-dismissible fade show`;
        alert.innerHTML = `
            <i class="bi bi-${iconMap[type]}"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        alertContainer.appendChild(alert);
        
        // Auto-dismiss después de 5 segundos
        setTimeout(() => {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 150);
        }, 5000);
    }

    // ============================================
    // KEYBOARD SHORTCUTS
    // ============================================
    
    function initKeyboardShortcuts() {
        document.addEventListener('keydown', function(e) {
            // Enter en cualquier campo del formulario
            if (e.key === 'Enter' && e.target.tagName !== 'BUTTON') {
                const form = document.getElementById('loginForm');
                if (form && form.checkValidity()) {
                    form.requestSubmit();
                }
            }
        });
    }

    // ============================================
    // PREVENIR ZOOM EN iOS
    // ============================================
    
    function preventIOSZoom() {
        if (/iPhone|iPad|iPod/.test(navigator.userAgent)) {
            const inputs = document.querySelectorAll('input, select, textarea');
            inputs.forEach(input => {
                if (input.style.fontSize < '16px') {
                    input.style.fontSize = '16px';
                }
            });
        }
    }

    // ============================================
    // MEJORAR ACCESIBILIDAD
    // ============================================
    
    function enhanceAccessibility() {
        // Agregar labels descriptivos
        const rolSelect = document.getElementById('rol');
        if (rolSelect) {
            rolSelect.setAttribute('aria-label', 'Seleccione su rol en el sistema');
        }
        
        const passwordInput = document.getElementById('password');
        if (passwordInput) {
            passwordInput.setAttribute('aria-label', 'Ingrese su contraseña');
        }
        
        // Mejorar mensajes de error
        const form = document.getElementById('loginForm');
        if (form) {
            form.setAttribute('novalidate', '');
        }
    }

    // ============================================
    // INICIALIZACIÓN
    // ============================================
    
    function init() {
        console.log('🎨 Inicializando mejoras UI/UX para Login Page');
        
        // Esperar a que el DOM esté listo
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }
        
        // Inicializar componentes con un pequeño delay para asegurar que todo esté cargado
        setTimeout(() => {
            initAnimations();
            addHapticFeedback();
            initValidation();
            enhancePasswordToggle(); // Esta es la función crítica
            enhanceLoadingState();
            initAutoFocus();
            enhanceMobileSelects();
            initKeyboardShortcuts();
            preventIOSZoom();
            enhanceAccessibility();
            
            console.log('✅ Mejoras UI/UX inicializadas correctamente');
        }, 100);
        
        // Exponer funciones globales
        window.loginMejoras = {
            showToast
        };
    }

    // Iniciar
    init();
    
    // Función de respaldo para el toggle de contraseña
    // Se ejecuta después de 1 segundo si la primera no funcionó
    setTimeout(() => {
        const toggleBtn = document.getElementById('togglePassword');
        const passwordInput = document.getElementById('password');
        const eyeIcon = document.getElementById('eyeIcon');
        
        if (toggleBtn && passwordInput && eyeIcon) {
            // Verificar si ya tiene el event listener
            if (!toggleBtn.hasAttribute('data-toggle-initialized')) {
                console.log('🔄 Configurando toggle de contraseña (respaldo)...');
                
                toggleBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    
                    const currentType = passwordInput.type;
                    const newType = currentType === 'password' ? 'text' : 'password';
                    
                    passwordInput.type = newType;
                    
                    if (newType === 'text') {
                        eyeIcon.className = 'bi bi-eye-slash';
                    } else {
                        eyeIcon.className = 'bi bi-eye';
                    }
                    
                    console.log('👁️ Toggle ejecutado (respaldo):', newType);
                });
                
                toggleBtn.setAttribute('data-toggle-initialized', 'true');
                console.log('✅ Toggle de contraseña configurado (respaldo)');
            }
        }
    }, 1000);
})();
