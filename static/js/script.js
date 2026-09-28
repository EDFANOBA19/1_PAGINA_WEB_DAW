/**
 * SCRIPT.JS - Validaciones Dinámicas y Manejo de Formularios
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ DOM cargado');

    // ============================================================
    // REFERENCIAS DOM - SOLICITUDES
    // ============================================================
    var solicitudesForm = document.getElementById('solicitudForm');
    var nombreInput = document.getElementById('solicitudNombre');
    var emailInput = document.getElementById('solicitudEmail');
    var categoriaSelect = document.getElementById('solicitudCategoria');
    var descripcionInput = document.getElementById('solicitudDescripcion');
    var caracteresActuales = document.getElementById('caracteresActuales');

    var nombreFeedback = document.getElementById('nombreFeedback');
    var nombreFeedbackSuccess = document.getElementById('nombreFeedbackSuccess');
    var emailFeedback = document.getElementById('emailFeedback');
    var emailFeedbackSuccess = document.getElementById('emailFeedbackSuccess');
    var categoriaFeedback = document.getElementById('categoriaFeedback');
    var categoriaFeedbackSuccess = document.getElementById('categoriaFeedbackSuccess');
    var descripcionFeedback = document.getElementById('descripcionFeedback');
    var descripcionFeedbackSuccess = document.getElementById('descripcionFeedbackSuccess');

    // ============================================================
    // REFERENCIAS DOM - CONTACTO
    // ============================================================
    var formularioContacto = document.getElementById('formularioContacto');
    var contactoNombre = document.getElementById('contactoNombre');
    var contactoEmail = document.getElementById('contactoEmail');
    var contactoAsunto = document.getElementById('contactoAsunto');
    var contactoMensaje = document.getElementById('contactoMensaje');
    var contactoCaracteresActuales = document.getElementById('contactoCaracteresActuales');

    var contactoNombreFeedback = document.getElementById('contactoNombreFeedback');
    var contactoNombreFeedbackSuccess = document.getElementById('contactoNombreFeedbackSuccess');
    var contactoEmailFeedback = document.getElementById('contactoEmailFeedback');
    var contactoEmailFeedbackSuccess = document.getElementById('contactoEmailFeedbackSuccess');
    var contactoAsuntoFeedback = document.getElementById('contactoAsuntoFeedback');
    var contactoAsuntoFeedbackSuccess = document.getElementById('contactoAsuntoFeedbackSuccess');
    var contactoMensajeFeedback = document.getElementById('contactoMensajeFeedback');
    var contactoMensajeFeedbackSuccess = document.getElementById('contactoMensajeFeedbackSuccess');

    // ============================================================
    // FUNCIONES AUXILIARES
    // ============================================================
    function validarSoloLetras(texto) {
        return /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/.test(texto);
    }

    function validarEmail(email) {
        // Validación estricta: solo dominios reales
        var regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|net|org|edu|gov|mil|ec|co|es|mx|ar|cl|pe|br|us|uk)$/;
        return regex.test(email);
    }

    // ============================================================
    // VALIDACIONES SOLICITUDES
    // ============================================================
    if (nombreInput) {
        nombreInput.addEventListener('input', function() {
            var valor = this.value.trim();
            var soloLetras = validarSoloLetras(valor);
            var longitudValida = valor.length >= 3;
            
            if (valor.length > 0 && soloLetras && longitudValida) {
                this.className = 'form-control is-valid';
                if (nombreFeedback) nombreFeedback.style.display = 'none';
                if (nombreFeedbackSuccess) nombreFeedbackSuccess.style.display = 'block';
            } else if (valor.length > 0 && !soloLetras) {
                this.className = 'form-control is-invalid';
                if (nombreFeedback) {
                    nombreFeedback.textContent = 'Solo letras y espacios';
                    nombreFeedback.style.display = 'block';
                }
                if (nombreFeedbackSuccess) nombreFeedbackSuccess.style.display = 'none';
            } else if (valor.length > 0 && !longitudValida) {
                this.className = 'form-control is-invalid';
                if (nombreFeedback) {
                    nombreFeedback.textContent = 'Mínimo 3 caracteres';
                    nombreFeedback.style.display = 'block';
                }
                if (nombreFeedbackSuccess) nombreFeedbackSuccess.style.display = 'none';
            } else {
                this.className = 'form-control';
                if (nombreFeedback) nombreFeedback.style.display = 'none';
                if (nombreFeedbackSuccess) nombreFeedbackSuccess.style.display = 'none';
            }
        });
    }

    if (emailInput) {
        emailInput.addEventListener('input', function() {
            var valor = this.value.trim();
            var esValido = validarEmail(valor);
            
            if (valor.length > 0 && esValido) {
                this.className = 'form-control is-valid';
                if (emailFeedback) emailFeedback.style.display = 'none';
                if (emailFeedbackSuccess) emailFeedbackSuccess.style.display = 'block';
            } else if (valor.length > 0 && !esValido) {
                this.className = 'form-control is-invalid';
                if (emailFeedback) emailFeedback.style.display = 'block';
                if (emailFeedbackSuccess) emailFeedbackSuccess.style.display = 'none';
            } else {
                this.className = 'form-control';
                if (emailFeedback) emailFeedback.style.display = 'none';
                if (emailFeedbackSuccess) emailFeedbackSuccess.style.display = 'none';
            }
        });
    }

    if (categoriaSelect) {
        categoriaSelect.addEventListener('change', function() {
            if (this.value !== '') {
                this.className = 'form-select is-valid';
                if (categoriaFeedback) categoriaFeedback.style.display = 'none';
                if (categoriaFeedbackSuccess) categoriaFeedbackSuccess.style.display = 'block';
            } else {
                this.className = 'form-select is-invalid';
                if (categoriaFeedback) categoriaFeedback.style.display = 'block';
                if (categoriaFeedbackSuccess) categoriaFeedbackSuccess.style.display = 'none';
            }
        });
    }

    if (descripcionInput) {
        descripcionInput.addEventListener('input', function() {
            var valor = this.value.trim();
            var esValido = valor.length >= 10;
            if (caracteresActuales) caracteresActuales.textContent = valor.length;
            
            if (valor.length > 0 && esValido) {
                this.className = 'form-control is-valid';
                if (descripcionFeedback) descripcionFeedback.style.display = 'none';
                if (descripcionFeedbackSuccess) descripcionFeedbackSuccess.style.display = 'block';
            } else if (valor.length > 0 && !esValido) {
                this.className = 'form-control is-invalid';
                if (descripcionFeedback) {
                    descripcionFeedback.textContent = 'Mínimo 10 caracteres (actual: ' + valor.length + ')';
                    descripcionFeedback.style.display = 'block';
                }
                if (descripcionFeedbackSuccess) descripcionFeedbackSuccess.style.display = 'none';
            } else {
                this.className = 'form-control';
                if (descripcionFeedback) descripcionFeedback.style.display = 'none';
                if (descripcionFeedbackSuccess) descripcionFeedbackSuccess.style.display = 'none';
            }
        });
    }

    // ============================================================
    // VALIDACIONES CONTACTO
    // ============================================================
    if (contactoNombre) {
        contactoNombre.addEventListener('input', function() {
            var valor = this.value.trim();
            var soloLetras = validarSoloLetras(valor);
            var longitudValida = valor.length >= 3 && valor.length <= 50;
            
            if (valor.length > 0 && soloLetras && longitudValida) {
                this.className = 'form-control is-valid';
                if (contactoNombreFeedback) contactoNombreFeedback.style.display = 'none';
                if (contactoNombreFeedbackSuccess) contactoNombreFeedbackSuccess.style.display = 'block';
            } else if (valor.length > 0 && !soloLetras) {
                this.className = 'form-control is-invalid';
                if (contactoNombreFeedback) {
                    contactoNombreFeedback.textContent = 'Solo letras y espacios';
                    contactoNombreFeedback.style.display = 'block';
                }
                if (contactoNombreFeedbackSuccess) contactoNombreFeedbackSuccess.style.display = 'none';
            } else if (valor.length > 0 && !longitudValida) {
                this.className = 'form-control is-invalid';
                if (contactoNombreFeedback) {
                    contactoNombreFeedback.textContent = 'Entre 3 y 50 caracteres';
                    contactoNombreFeedback.style.display = 'block';
                }
                if (contactoNombreFeedbackSuccess) contactoNombreFeedbackSuccess.style.display = 'none';
            } else {
                this.className = 'form-control';
                if (contactoNombreFeedback) contactoNombreFeedback.style.display = 'none';
                if (contactoNombreFeedbackSuccess) contactoNombreFeedbackSuccess.style.display = 'none';
            }
        });
    }

    if (contactoEmail) {
        contactoEmail.addEventListener('input', function() {
            var valor = this.value.trim();
            var esValido = validarEmail(valor);
            
            if (valor.length > 0 && esValido) {
                this.className = 'form-control is-valid';
                if (contactoEmailFeedback) contactoEmailFeedback.style.display = 'none';
                if (contactoEmailFeedbackSuccess) contactoEmailFeedbackSuccess.style.display = 'block';
            } else if (valor.length > 0 && !esValido) {
                this.className = 'form-control is-invalid';
                if (contactoEmailFeedback) {
                    contactoEmailFeedback.textContent = 'Ingrese un correo válido (ejemplo@correo.com)';
                    contactoEmailFeedback.style.display = 'block';
                }
                if (contactoEmailFeedbackSuccess) contactoEmailFeedbackSuccess.style.display = 'none';
            } else {
                this.className = 'form-control';
                if (contactoEmailFeedback) contactoEmailFeedback.style.display = 'none';
                if (contactoEmailFeedbackSuccess) contactoEmailFeedbackSuccess.style.display = 'none';
            }
        });
    }

    if (contactoAsunto) {
        contactoAsunto.addEventListener('input', function() {
            var valor = this.value.trim();
            var esValido = valor.length >= 5 && valor.length <= 100;
            
            if (valor.length > 0 && esValido) {
                this.className = 'form-control is-valid';
                if (contactoAsuntoFeedback) contactoAsuntoFeedback.style.display = 'none';
                if (contactoAsuntoFeedbackSuccess) contactoAsuntoFeedbackSuccess.style.display = 'block';
            } else if (valor.length > 0 && !esValido) {
                this.className = 'form-control is-invalid';
                if (contactoAsuntoFeedback) {
                    contactoAsuntoFeedback.textContent = 'Entre 5 y 100 caracteres';
                    contactoAsuntoFeedback.style.display = 'block';
                }
                if (contactoAsuntoFeedbackSuccess) contactoAsuntoFeedbackSuccess.style.display = 'none';
            } else {
                this.className = 'form-control';
                if (contactoAsuntoFeedback) contactoAsuntoFeedback.style.display = 'none';
                if (contactoAsuntoFeedbackSuccess) contactoAsuntoFeedbackSuccess.style.display = 'none';
            }
        });
    }

    if (contactoMensaje) {
        contactoMensaje.addEventListener('input', function() {
            var valor = this.value.trim();
            var esValido = valor.length >= 10 && valor.length <= 500;
            if (contactoCaracteresActuales) contactoCaracteresActuales.textContent = valor.length;
            
            if (valor.length > 0 && esValido) {
                this.className = 'form-control is-valid';
                if (contactoMensajeFeedback) contactoMensajeFeedback.style.display = 'none';
                if (contactoMensajeFeedbackSuccess) contactoMensajeFeedbackSuccess.style.display = 'block';
            } else if (valor.length > 0 && !esValido) {
                this.className = 'form-control is-invalid';
                if (contactoMensajeFeedback) {
                    contactoMensajeFeedback.textContent = 'Entre 10 y 500 caracteres (actual: ' + valor.length + ')';
                    contactoMensajeFeedback.style.display = 'block';
                }
                if (contactoMensajeFeedbackSuccess) contactoMensajeFeedbackSuccess.style.display = 'none';
            } else {
                this.className = 'form-control';
                if (contactoMensajeFeedback) contactoMensajeFeedback.style.display = 'none';
                if (contactoMensajeFeedbackSuccess) contactoMensajeFeedbackSuccess.style.display = 'none';
            }
        });
    }

    console.log('🚀 Aplicación lista');
});