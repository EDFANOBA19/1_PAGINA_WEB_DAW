/**
 * SCRIPT.JS - Validaciones Dinámicas y Manejo de Formularios
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ DOM cargado - Semana 9');

    // ============================================================
    // DATOS DE EJEMPLO (4 solicitudes precargadas)
    // ============================================================
    var solicitudesData = [
        {
            id: 1,
            nombre: 'Carlos Mendoza',
            email: 'carlos.mendoza@empresa.com',
            categoria: 'Generadores Eléctricos',
            descripcion: 'Necesito un generador de 100kW para un proyecto de construcción en Quito.',
            fecha: '2026-07-10 14:30'
        },
        {
            id: 2,
            nombre: 'María Fernández',
            email: 'maria.fernandez@eventos.com',
            categoria: 'Torres de Iluminación',
            descripcion: 'Requerimos 4 torres de iluminación para un evento nocturno.',
            fecha: '2026-07-11 09:15'
        },
        {
            id: 3,
            nombre: 'José Ramírez',
            email: 'jose.ramirez@petrolera.com',
            categoria: 'Compresores de Aire',
            descripcion: 'Necesito un compresor de 150 psi para operaciones en el campo petrolero.',
            fecha: '2026-07-12 11:45'
        },
        {
            id: 4,
            nombre: 'Ana Torres',
            email: 'ana.torres@construccion.com',
            categoria: 'Asesoría Técnica',
            descripcion: 'Solicito asesoría para seleccionar el equipo adecuado para una planta de energía.',
            fecha: '2026-07-12 16:20'
        }
    ];

    // ============================================================
    // REFERENCIAS DOM
    // ============================================================
    var solicitudesForm = document.getElementById('solicitudForm');
    var nombreInput = document.getElementById('solicitudNombre');
    var emailInput = document.getElementById('solicitudEmail');
    var categoriaSelect = document.getElementById('solicitudCategoria');
    var descripcionInput = document.getElementById('solicitudDescripcion');
    var listaSolicitudes = document.getElementById('listaSolicitudes');
    var contadorSolicitudes = document.getElementById('contadorSolicitudes');
    var mensajeVacio = document.getElementById('mensajeVacio');
    var caracteresActuales = document.getElementById('caracteresActuales');
    var contenedorTarjetas = document.getElementById('contenedorTarjetas');
    var estadoSolicitudes = document.getElementById('estadoSolicitudes');

    var alertaMensaje = document.getElementById('alertaMensaje');
    var alertaTexto = document.getElementById('alertaTexto');
    var alertaContacto = document.getElementById('alertaContacto');
    var alertaContactoTexto = document.getElementById('alertaContactoTexto');

    var spinnerCarga = document.getElementById('spinnerCarga');
    var spinnerContacto = document.getElementById('spinnerContacto');

    var confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));
    var confirmarAccionBtn = document.getElementById('confirmarAccion');
    var modalMensaje = document.getElementById('modalMensaje');

    // Feedback
    var nombreFeedback = document.getElementById('nombreFeedback');
    var nombreFeedbackSuccess = document.getElementById('nombreFeedbackSuccess');
    var emailFeedback = document.getElementById('emailFeedback');
    var emailFeedbackSuccess = document.getElementById('emailFeedbackSuccess');
    var categoriaFeedback = document.getElementById('categoriaFeedback');
    var categoriaFeedbackSuccess = document.getElementById('categoriaFeedbackSuccess');
    var descripcionFeedback = document.getElementById('descripcionFeedback');
    var descripcionFeedbackSuccess = document.getElementById('descripcionFeedbackSuccess');

    // Contacto
    var formularioContacto = document.getElementById('formularioContacto');
    var contactoNombre = document.getElementById('contactoNombre');
    var contactoEmail = document.getElementById('contactoEmail');
    var contactoAsunto = document.getElementById('contactoAsunto');
    var contactoMensaje = document.getElementById('contactoMensaje');
    var contactoCaracteresActuales = document.getElementById('contactoCaracteresActuales');

    // ============================================================
    // FUNCIONES AUXILIARES
    // ============================================================
    function validarSoloLetras(texto) {
        return /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/.test(texto);
    }

    function validarEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    function escapeHTML(texto) {
        var div = document.createElement('div');
        div.textContent = texto;
        return div.innerHTML;
    }

    function mostrarAlerta(tipo, mensaje, esContacto) {
        var alerta = esContacto ? alertaContacto : alertaMensaje;
        var texto = esContacto ? alertaContactoTexto : alertaTexto;
        
        alerta.className = 'alert alert-dismissible fade show alert-' + tipo;
        texto.textContent = mensaje;
        alerta.style.display = 'block';
        
        setTimeout(function() {
            alerta.style.display = 'none';
        }, 4000);
    }

    function mostrarSpinner(esContacto) {
        var spinner = esContacto ? spinnerContacto : spinnerCarga;
        spinner.style.display = 'flex';
        setTimeout(function() {
            spinner.style.display = 'none';
        }, 2000);
    }

    function limpiarFormulario() {
        nombreInput.value = '';
        emailInput.value = '';
        categoriaSelect.value = '';
        descripcionInput.value = '';
        
        [nombreInput, emailInput, categoriaSelect, descripcionInput].forEach(function(el) {
            el.classList.remove('is-valid', 'is-invalid');
        });
        
        if (caracteresActuales) caracteresActuales.textContent = '0';
    }

    function actualizarContador() {
        var total = listaSolicitudes.children.length;
        contadorSolicitudes.textContent = total;
    }

    // ============================================================
    // RENDERIZAR TARJETAS
    // ============================================================
    function renderizarTarjetas(data) {
        contenedorTarjetas.innerHTML = '';
        
        if (data.length === 0) {
            estadoSolicitudes.textContent = 'Sin solicitudes';
            estadoSolicitudes.className = 'badge bg-warning';
            contenedorTarjetas.innerHTML = `
                <div class="col-12">
                    <div class="alert alert-info text-center py-5">
                        <span class="fs-1">📭</span>
                        <h5 class="mt-3">No hay solicitudes recientes</h5>
                    </div>
                </div>
            `;
            return;
        }
        
        estadoSolicitudes.textContent = data.length + ' solicitudes activas';
        estadoSolicitudes.className = 'badge bg-success';
        
        var colores = {
            'Generadores Eléctricos': 'border-primary',
            'Torres de Iluminación': 'border-warning',
            'Compresores de Aire': 'border-success',
            'Asesoría Técnica': 'border-info',
            'Entrega y Retiro': 'border-secondary',
            'Mantenimiento Preventivo': 'border-danger'
        };
        
        data.forEach(function(solicitud) {
            var columna = document.createElement('div');
            columna.className = 'col-md-6 col-lg-4';
            var colorBorde = colores[solicitud.categoria] || 'border-secondary';
            
            columna.innerHTML = `
                <div class="card h-100 ${colorBorde} border-4 shadow-sm solicitud-tarjeta" data-id="${solicitud.id}">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <h5 class="card-title text-primary mb-0">${escapeHTML(solicitud.nombre)}</h5>
                            <span class="badge bg-primary rounded-pill">#${solicitud.id}</span>
                        </div>
                        <p class="card-text small text-muted mb-1"><strong>📧</strong> ${escapeHTML(solicitud.email)}</p>
                        <p class="card-text"><span class="badge bg-secondary">${escapeHTML(solicitud.categoria)}</span></p>
                        <p class="card-text text-justificado small">${escapeHTML(solicitud.descripcion)}</p>
                        <p class="card-text"><small class="text-muted">📅 ${escapeHTML(solicitud.fecha)}</small></p>
                        <button class="btn btn-outline-danger btn-sm w-100 eliminar-tarjeta" data-id="${solicitud.id}">🗑️ Eliminar</button>
                    </div>
                </div>
            `;
            
            contenedorTarjetas.appendChild(columna);
        });
        
        document.querySelectorAll('.eliminar-tarjeta').forEach(function(btn) {
            btn.addEventListener('click', function() {
                eliminarSolicitud(parseInt(this.dataset.id));
            });
        });
    }

    // ============================================================
    // ELIMINAR SOLICITUD
    // ============================================================
    function eliminarSolicitud(id) {
        var index = solicitudesData.findIndex(function(item) { return item.id === id; });
        if (index === -1) return;
        
        solicitudesData.splice(index, 1);
        renderizarTarjetas(solicitudesData);
        
        var elementoLista = document.querySelector('.solicitud-item[data-id="' + id + '"]');
        if (elementoLista) {
            elementoLista.remove();
            actualizarContador();
            if (listaSolicitudes.children.length === 0) {
                mensajeVacio.style.display = 'block';
            }
        }
        
        mostrarAlerta('success', '🗑️ Solicitud eliminada correctamente', false);
    }

    // ============================================================
    // VALIDACIONES EN TIEMPO REAL
    // ============================================================
    
    nombreInput.addEventListener('input', function() {
        var valor = this.value.trim();
        var soloLetras = validarSoloLetras(valor);
        var longitudValida = valor.length >= 3;
        
        if (valor.length > 0 && soloLetras && longitudValida) {
            this.className = 'form-control is-valid';
            nombreFeedback.style.display = 'none';
            nombreFeedbackSuccess.style.display = 'block';
        } else if (valor.length > 0 && !soloLetras) {
            this.className = 'form-control is-invalid';
            nombreFeedback.textContent = 'Solo letras y espacios';
            nombreFeedback.style.display = 'block';
            nombreFeedbackSuccess.style.display = 'none';
        } else if (valor.length > 0 && !longitudValida) {
            this.className = 'form-control is-invalid';
            nombreFeedback.textContent = 'Mínimo 3 caracteres';
            nombreFeedback.style.display = 'block';
            nombreFeedbackSuccess.style.display = 'none';
        } else {
            this.className = 'form-control';
            nombreFeedback.style.display = 'none';
            nombreFeedbackSuccess.style.display = 'none';
        }
    });

    emailInput.addEventListener('input', function() {
        var valor = this.value.trim();
        var esValido = validarEmail(valor);
        
        if (valor.length > 0 && esValido) {
            this.className = 'form-control is-valid';
            emailFeedback.style.display = 'none';
            emailFeedbackSuccess.style.display = 'block';
        } else if (valor.length > 0 && !esValido) {
            this.className = 'form-control is-invalid';
            emailFeedback.style.display = 'block';
            emailFeedbackSuccess.style.display = 'none';
        } else {
            this.className = 'form-control';
            emailFeedback.style.display = 'none';
            emailFeedbackSuccess.style.display = 'none';
        }
    });

    categoriaSelect.addEventListener('change', function() {
        if (this.value !== '') {
            this.className = 'form-select is-valid';
            categoriaFeedback.style.display = 'none';
            categoriaFeedbackSuccess.style.display = 'block';
        } else {
            this.className = 'form-select is-invalid';
            categoriaFeedback.style.display = 'block';
            categoriaFeedbackSuccess.style.display = 'none';
        }
    });

    descripcionInput.addEventListener('input', function() {
        var valor = this.value.trim();
        var esValido = valor.length >= 10;
        if (caracteresActuales) caracteresActuales.textContent = valor.length;
        
        if (valor.length > 0 && esValido) {
            this.className = 'form-control is-valid';
            descripcionFeedback.style.display = 'none';
            descripcionFeedbackSuccess.style.display = 'block';
        } else if (valor.length > 0 && !esValido) {
            this.className = 'form-control is-invalid';
            descripcionFeedback.textContent = 'Mínimo 10 caracteres (actual: ' + valor.length + ')';
            descripcionFeedback.style.display = 'block';
            descripcionFeedbackSuccess.style.display = 'none';
        } else {
            this.className = 'form-control';
            descripcionFeedback.style.display = 'none';
            descripcionFeedbackSuccess.style.display = 'none';
        }
    });

    // ============================================================
    // ENVÍO DE SOLICITUD
    // ============================================================
    solicitudesForm.addEventListener('submit', function(event) {
        event.preventDefault();

        var nombre = nombreInput.value.trim();
        var email = emailInput.value.trim();
        var categoria = categoriaSelect.value;
        var descripcion = descripcionInput.value.trim();
        var errores = [];

        if (!nombre) {
            errores.push('Nombre obligatorio');
            nombreInput.className = 'form-control is-invalid';
            nombreFeedback.textContent = 'Nombre obligatorio';
            nombreFeedback.style.display = 'block';
            nombreFeedbackSuccess.style.display = 'none';
        } else if (!validarSoloLetras(nombre)) {
            errores.push('Solo letras');
            nombreInput.className = 'form-control is-invalid';
            nombreFeedback.textContent = 'Solo letras y espacios';
            nombreFeedback.style.display = 'block';
            nombreFeedbackSuccess.style.display = 'none';
        } else if (nombre.length < 3) {
            errores.push('Mínimo 3 caracteres');
            nombreInput.className = 'form-control is-invalid';
            nombreFeedback.textContent = 'Mínimo 3 caracteres';
            nombreFeedback.style.display = 'block';
            nombreFeedbackSuccess.style.display = 'none';
        } else {
            nombreInput.className = 'form-control is-valid';
            nombreFeedback.style.display = 'none';
            nombreFeedbackSuccess.style.display = 'block';
        }

        if (!email) {
            errores.push('Email obligatorio');
            emailInput.className = 'form-control is-invalid';
            emailFeedback.textContent = 'Email obligatorio';
            emailFeedback.style.display = 'block';
            emailFeedbackSuccess.style.display = 'none';
        } else if (!validarEmail(email)) {
            errores.push('Email inválido');
            emailInput.className = 'form-control is-invalid';
            emailFeedback.textContent = 'Email inválido (ejemplo@dominio.com)';
            emailFeedback.style.display = 'block';
            emailFeedbackSuccess.style.display = 'none';
        } else {
            emailInput.className = 'form-control is-valid';
            emailFeedback.style.display = 'none';
            emailFeedbackSuccess.style.display = 'block';
        }

        if (!categoria) {
            errores.push('Categoría obligatoria');
            categoriaSelect.className = 'form-select is-invalid';
            categoriaFeedback.style.display = 'block';
            categoriaFeedbackSuccess.style.display = 'none';
        } else {
            categoriaSelect.className = 'form-select is-valid';
            categoriaFeedback.style.display = 'none';
            categoriaFeedbackSuccess.style.display = 'block';
        }

        if (!descripcion) {
            errores.push('Descripción obligatoria');
            descripcionInput.className = 'form-control is-invalid';
            descripcionFeedback.textContent = 'Descripción obligatoria';
            descripcionFeedback.style.display = 'block';
            descripcionFeedbackSuccess.style.display = 'none';
        } else if (descripcion.length < 10) {
            errores.push('Mínimo 10 caracteres');
            descripcionInput.className = 'form-control is-invalid';
            descripcionFeedback.textContent = 'Mínimo 10 caracteres (actual: ' + descripcion.length + ')';
            descripcionFeedback.style.display = 'block';
            descripcionFeedbackSuccess.style.display = 'none';
        } else {
            descripcionInput.className = 'form-control is-valid';
            descripcionFeedback.style.display = 'none';
            descripcionFeedbackSuccess.style.display = 'block';
        }

        if (errores.length > 0) {
            mostrarAlerta('danger', '⚠️ Corrija los errores', false);
            var primerError = document.querySelector('.is-invalid');
            if (primerError) {
                primerError.focus();
                primerError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
            return;
        }

        modalMensaje.textContent = '¿Registrar solicitud de ' + nombre + '?';
        confirmModal.show();

        confirmarAccionBtn.onclick = function() {
            confirmModal.hide();
            mostrarSpinner(false);

            var nuevaSolicitud = {
                id: Date.now(),
                nombre: nombre,
                email: email,
                categoria: categoria,
                descripcion: descripcion,
                fecha: new Date().toLocaleString('es-EC')
            };
            
            solicitudesData.push(nuevaSolicitud);
            renderizarTarjetas(solicitudesData);
            
            var li = document.createElement('li');
            li.className = 'list-group-item solicitud-item';
            li.dataset.id = nuevaSolicitud.id;
            li.innerHTML = `
                <div class="d-flex flex-wrap justify-content-between align-items-start">
                    <div class="flex-grow-1 me-3">
                        <h5 class="mb-1">${escapeHTML(nombre)}</h5>
                        <div class="d-flex flex-wrap gap-2 mb-1">
                            <span class="badge bg-primary">${escapeHTML(categoria)}</span>
                            <span class="badge bg-secondary">${escapeHTML(email)}</span>
                        </div>
                        <p class="mb-1 text-muted small">${escapeHTML(descripcion)}</p>
                        <small class="text-muted">📅 ${nuevaSolicitud.fecha}</small>
                    </div>
                    <button class="btn btn-danger btn-sm eliminar-solicitud" data-id="${nuevaSolicitud.id}">🗑️ Eliminar</button>
                </div>
            `;

            listaSolicitudes.appendChild(li);
            mensajeVacio.style.display = 'none';

            li.querySelector('.eliminar-solicitud').addEventListener('click', function() {
                eliminarSolicitud(parseInt(this.dataset.id));
            });

            actualizarContador();
            limpiarFormulario();
            mostrarAlerta('success', '✅ ¡Solicitud registrada!', false);
        };
    });

    // ============================================================
    // FORMULARIO DE CONTACTO
    // ============================================================
    contactoNombre.addEventListener('input', function() {
        var valor = this.value.trim();
        var soloLetras = validarSoloLetras(valor);
        var longitudValida = valor.length >= 3;
        
        if (valor.length > 0 && soloLetras && longitudValida) {
            this.className = 'form-control is-valid';
            document.getElementById('contactoNombreFeedback').style.display = 'none';
            document.getElementById('contactoNombreFeedbackSuccess').style.display = 'block';
        } else if (valor.length > 0 && !soloLetras) {
            this.className = 'form-control is-invalid';
            document.getElementById('contactoNombreFeedback').textContent = 'Solo letras y espacios';
            document.getElementById('contactoNombreFeedback').style.display = 'block';
            document.getElementById('contactoNombreFeedbackSuccess').style.display = 'none';
        } else if (valor.length > 0 && !longitudValida) {
            this.className = 'form-control is-invalid';
            document.getElementById('contactoNombreFeedback').textContent = 'Mínimo 3 caracteres';
            document.getElementById('contactoNombreFeedback').style.display = 'block';
            document.getElementById('contactoNombreFeedbackSuccess').style.display = 'none';
        } else {
            this.className = 'form-control';
            document.getElementById('contactoNombreFeedback').style.display = 'none';
            document.getElementById('contactoNombreFeedbackSuccess').style.display = 'none';
        }
    });

    contactoEmail.addEventListener('input', function() {
        var valor = this.value.trim();
        var esValido = validarEmail(valor);
        
        if (valor.length > 0 && esValido) {
            this.className = 'form-control is-valid';
            document.getElementById('contactoEmailFeedback').style.display = 'none';
            document.getElementById('contactoEmailFeedbackSuccess').style.display = 'block';
        } else if (valor.length > 0 && !esValido) {
            this.className = 'form-control is-invalid';
            document.getElementById('contactoEmailFeedback').style.display = 'block';
            document.getElementById('contactoEmailFeedbackSuccess').style.display = 'none';
        } else {
            this.className = 'form-control';
            document.getElementById('contactoEmailFeedback').style.display = 'none';
            document.getElementById('contactoEmailFeedbackSuccess').style.display = 'none';
        }
    });

    contactoAsunto.addEventListener('input', function() {
        var valor = this.value.trim();
        var esValido = valor.length >= 5;
        
        if (valor.length > 0 && esValido) {
            this.className = 'form-control is-valid';
            document.getElementById('contactoAsuntoFeedback').style.display = 'none';
            document.getElementById('contactoAsuntoFeedbackSuccess').style.display = 'block';
        } else if (valor.length > 0 && !esValido) {
            this.className = 'form-control is-invalid';
            document.getElementById('contactoAsuntoFeedback').textContent = 'Mínimo 5 caracteres';
            document.getElementById('contactoAsuntoFeedback').style.display = 'block';
            document.getElementById('contactoAsuntoFeedbackSuccess').style.display = 'none';
        } else {
            this.className = 'form-control';
            document.getElementById('contactoAsuntoFeedback').style.display = 'none';
            document.getElementById('contactoAsuntoFeedbackSuccess').style.display = 'none';
        }
    });

    contactoMensaje.addEventListener('input', function() {
        var valor = this.value.trim();
        var esValido = valor.length >= 10;
        if (contactoCaracteresActuales) contactoCaracteresActuales.textContent = valor.length;
        
        if (valor.length > 0 && esValido) {
            this.className = 'form-control is-valid';
            document.getElementById('contactoMensajeFeedback').style.display = 'none';
            document.getElementById('contactoMensajeFeedbackSuccess').style.display = 'block';
        } else if (valor.length > 0 && !esValido) {
            this.className = 'form-control is-invalid';
            document.getElementById('contactoMensajeFeedback').textContent = 'Mínimo 10 caracteres (actual: ' + valor.length + ')';
            document.getElementById('contactoMensajeFeedback').style.display = 'block';
            document.getElementById('contactoMensajeFeedbackSuccess').style.display = 'none';
        } else {
            this.className = 'form-control';
            document.getElementById('contactoMensajeFeedback').style.display = 'none';
            document.getElementById('contactoMensajeFeedbackSuccess').style.display = 'none';
        }
    });

    formularioContacto.addEventListener('submit', function(event) {
        event.preventDefault();

        var nombre = contactoNombre.value.trim();
        var email = contactoEmail.value.trim();
        var asunto = contactoAsunto.value.trim();
        var mensaje = contactoMensaje.value.trim();
        var errores = [];

        if (!nombre) {
            errores.push('Nombre obligatorio');
            contactoNombre.className = 'form-control is-invalid';
            document.getElementById('contactoNombreFeedback').textContent = 'Nombre obligatorio';
            document.getElementById('contactoNombreFeedback').style.display = 'block';
            document.getElementById('contactoNombreFeedbackSuccess').style.display = 'none';
        } else if (!validarSoloLetras(nombre)) {
            errores.push('Solo letras');
            contactoNombre.className = 'form-control is-invalid';
            document.getElementById('contactoNombreFeedback').textContent = 'Solo letras y espacios';
            document.getElementById('contactoNombreFeedback').style.display = 'block';
            document.getElementById('contactoNombreFeedbackSuccess').style.display = 'none';
        } else if (nombre.length < 3) {
            errores.push('Mínimo 3 caracteres');
            contactoNombre.className = 'form-control is-invalid';
            document.getElementById('contactoNombreFeedback').textContent = 'Mínimo 3 caracteres';
            document.getElementById('contactoNombreFeedback').style.display = 'block';
            document.getElementById('contactoNombreFeedbackSuccess').style.display = 'none';
        } else {
            contactoNombre.className = 'form-control is-valid';
            document.getElementById('contactoNombreFeedback').style.display = 'none';
            document.getElementById('contactoNombreFeedbackSuccess').style.display = 'block';
        }

        if (!email) {
            errores.push('Email obligatorio');
            contactoEmail.className = 'form-control is-invalid';
            document.getElementById('contactoEmailFeedback').textContent = 'Email obligatorio';
            document.getElementById('contactoEmailFeedback').style.display = 'block';
            document.getElementById('contactoEmailFeedbackSuccess').style.display = 'none';
        } else if (!validarEmail(email)) {
            errores.push('Email inválido');
            contactoEmail.className = 'form-control is-invalid';
            document.getElementById('contactoEmailFeedback').textContent = 'Email inválido';
            document.getElementById('contactoEmailFeedback').style.display = 'block';
            document.getElementById('contactoEmailFeedbackSuccess').style.display = 'none';
        } else {
            contactoEmail.className = 'form-control is-valid';
            document.getElementById('contactoEmailFeedback').style.display = 'none';
            document.getElementById('contactoEmailFeedbackSuccess').style.display = 'block';
        }

        if (!asunto) {
            errores.push('Asunto obligatorio');
            contactoAsunto.className = 'form-control is-invalid';
            document.getElementById('contactoAsuntoFeedback').textContent = 'Asunto obligatorio';
            document.getElementById('contactoAsuntoFeedback').style.display = 'block';
            document.getElementById('contactoAsuntoFeedbackSuccess').style.display = 'none';
        } else if (asunto.length < 5) {
            errores.push('Mínimo 5 caracteres');
            contactoAsunto.className = 'form-control is-invalid';
            document.getElementById('contactoAsuntoFeedback').textContent = 'Mínimo 5 caracteres';
            document.getElementById('contactoAsuntoFeedback').style.display = 'block';
            document.getElementById('contactoAsuntoFeedbackSuccess').style.display = 'none';
        } else {
            contactoAsunto.className = 'form-control is-valid';
            document.getElementById('contactoAsuntoFeedback').style.display = 'none';
            document.getElementById('contactoAsuntoFeedbackSuccess').style.display = 'block';
        }

        if (!mensaje) {
            errores.push('Mensaje obligatorio');
            contactoMensaje.className = 'form-control is-invalid';
            document.getElementById('contactoMensajeFeedback').textContent = 'Mensaje obligatorio';
            document.getElementById('contactoMensajeFeedback').style.display = 'block';
            document.getElementById('contactoMensajeFeedbackSuccess').style.display = 'none';
        } else if (mensaje.length < 10) {
            errores.push('Mínimo 10 caracteres');
            contactoMensaje.className = 'form-control is-invalid';
            document.getElementById('contactoMensajeFeedback').textContent = 'Mínimo 10 caracteres (actual: ' + mensaje.length + ')';
            document.getElementById('contactoMensajeFeedback').style.display = 'block';
            document.getElementById('contactoMensajeFeedbackSuccess').style.display = 'none';
        } else {
            contactoMensaje.className = 'form-control is-valid';
            document.getElementById('contactoMensajeFeedback').style.display = 'none';
            document.getElementById('contactoMensajeFeedbackSuccess').style.display = 'block';
        }

        if (errores.length > 0) {
            mostrarAlerta('danger', '⚠️ Corrija los errores', true);
            return;
        }

        mostrarSpinner(true);
        mostrarAlerta('success', '✅ ¡Mensaje enviado!', true);

        contactoNombre.value = '';
        contactoEmail.value = '';
        contactoAsunto.value = '';
        contactoMensaje.value = '';
        if (contactoCaracteresActuales) contactoCaracteresActuales.textContent = '0';
        
        [contactoNombre, contactoEmail, contactoAsunto, contactoMensaje].forEach(function(el) {
            el.className = 'form-control';
        });
        
        ['contactoNombreFeedback', 'contactoNombreFeedbackSuccess', 'contactoEmailFeedback',
         'contactoEmailFeedbackSuccess', 'contactoAsuntoFeedback', 'contactoAsuntoFeedbackSuccess',
         'contactoMensajeFeedback', 'contactoMensajeFeedbackSuccess'].forEach(function(id) {
            var el = document.getElementById(id);
            if (el) el.style.display = 'none';
        });
    });

    // ============================================================
    // INICIALIZAR
    // ============================================================
    renderizarTarjetas(solicitudesData);
    console.log('🚀 Aplicación lista - Semana 9');
});