function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function message_error(obj) {
    var html = '';
    if (typeof (obj) === 'object') {
        html = '<ul style="text-align: left;">';
        $.each(obj, function (key, value) {
            html += '<li>' + key + ': ' + value + '</li>';
        });
        html += '</ul>';
    } else {
        html = '<p>' + obj + '</p>';
    }
    Swal.fire({
        title: 'Error!',
        html: html,
        icon: 'error'
    });
}


function submit_with_ajaxx(url, title, content, parameters, callback) {
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn app-btn-secondary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Aceptar",
                btnClass: 'btn app-btn-primary',
                action: function () {
                    $.ajax({
                        url: url,
                        data: parameters,
                        type: 'POST',
                        dataType: 'json',
                        headers: {
                            'X-CSRFToken': csrftoken
                        },
                        processData: false,
                        contentType: false,
                        success: function (request) {
                            if (!request.hasOwnProperty('error')) {
                                callback(request);
                                return false;
                            }
                            message_error(request.error);
                        },
                        error: function (jqXHR, textStatus, errorThrown) {
                            message_error(errorThrown + ' ' + textStatus);
                        }
                    });
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn app-btn-secondary app-btn-outline-danger',
                action: function () {

                }
            },
        }
    })
}


function alert_action(title, content, callback, cancel) {
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    callback();
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {
                    cancel();
                }
            },
        }
    })
}

function validate_form_text(type, event, regex) {
    var key = event.keyCode || event.which;
    var numbers = (key > 47 && key < 58) || key === 8;
    var numbers_spaceless = (key > 47 && key < 58);
    var letters = !((key !== 32) && (key < 65) || (key > 90) && (key < 97) || (key > 122 && key !== 241 && key !== 209 && key !== 225 && key !== 233 && key !== 237 && key !== 243 && key !== 250 && key !== 193 && key !== 201 && key !== 205 && key !== 211 && key !== 218)) || key === 8;
    var letters_spaceless = !((key < 65) || (key > 90) && (key < 97) || (key > 122 && key !== 241 && key !== 209 && key !== 225 && key !== 233 && key !== 237 && key !== 243 && key !== 250 && key !== 193 && key !== 201 && key !== 205 && key !== 211 && key !== 218)) || key === 8;
    var decimals = ((key > 47 && key < 58) || key === 8 || key === 46);

    if (type === 'numbers') {
        return numbers;
    } else if (type === 'numbers_spaceless') {
        return numbers_spaceless;
    } else if (type === 'letters') {
        return letters;
    } else if (type === 'numbers_letters') {
        return numbers || letters;
    } else if (type === 'letters_spaceless') {
        return letters_spaceless;
    } else if (type === 'letters_numbers_spaceless') {
        return letters_spaceless || numbers_spaceless;
    } else if (type === 'decimals') {
        return decimals;
    } else if (type === 'regex') {
        return regex;
    }
    return true;
}

function validate_decimals(el, evt) {
    var charCode = (evt.which) ? evt.which : event.keyCode;
    var number = el.val().split('.');

    if (charCode !== 46 && charCode > 31 && (charCode < 48 || charCode > 57)) {
        return false;
    } else if (number.length > 1 && charCode === 46) {
        return false;
    } else if (el.val().length === 0 && charCode === 46) {
        return false;
    }

    return true;
}

//MIS FUNCIONES

function submit_with_ajax(url, title, content, parameters, callback) {
    // Crear el modal personalizado
    var modalHTML = `
         <div id="confirm-modal" class="modal fade" tabindex="-1" data-bs-backdrop="static" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content rounded-8">
                
                    <div class="modal-header border-bottom-0">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="position-absolute top-0 end-0 m-3 btn-close bg-soft-secondary rounded-pill" data-bs-dismiss="modal"  aria-label="Close"></button>
                    </div>
                    
                    <div class="modal-body py-0">
                      <p class="">${content}</p>
                    </div>
                          
                    <div class="modal-footer flex-nowrap border-top-0 gap-2 ">              
                        <button id="cancel-button" type="button" class="btn btn-lg btn-light w-100 mx-0" data-bs-dismiss="modal">Cerrar</button>
                        <button id="confirm-button" type="button" class="btn btn-lg btn-primary w-100 mx-0 mb-2">Guardar</button>                  
                    </div>
                </div>
            </div>
         </div>
  `;

    // Agregar el modal al DOM
    var modalContainer = document.createElement('div');
    modalContainer.innerHTML = modalHTML;
    document.body.appendChild(modalContainer);

    // Obtener los botones del modal
    var modal = document.getElementById('confirm-modal');
    var confirmButton = document.getElementById('confirm-button');
    var cancelButton = document.getElementById('cancel-button');

    // Mostrar el modal
    var modalInstance = new bootstrap.Modal(modal);
    modalInstance.show();


    // Agregar eventos a los botones
    confirmButton.addEventListener('click', function () {
        // Realizar la solicitud AJAX para eliminar el objeto
        $.ajax({
            url: url,
            data: parameters,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            processData: false,
            contentType: false,
            success: function (request) {
                if (!request.hasOwnProperty('error')) {
                    callback(request);
                    return false;
                }
                message_error(request.error);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                message_error(errorThrown + ' ' + textStatus);
            }
        });

        // Ocultar el modal y eliminarlo del DOM
        modalInstance.hide();
        modalContainer.parentNode.removeChild(modalContainer);
    });

    cancelButton.addEventListener('click', function () {
        // Ocultar el modal y eliminarlo del DOM sin hacer nada
        modalInstance.hide();
        modalContainer.parentNode.removeChild(modalContainer);
    });
}


function submit_without_alert(url, parameters, callback) {
    $.ajax({
        url: url,
        data: parameters,
        type: 'POST',
        dataType: 'json',
        headers: {
            'X-CSRFToken': csrftoken
        },
        processData: false,
        contentType: false,
        success: function (request) {
            if (!request.hasOwnProperty('error')) {
                callback(request);
                return false;
            }
            message_error(request.error);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            message_error(errorThrown + ' ' + textStatus);
        }
    });
}


function delete_with_ajax(url, title, content, parameters, callback) {
    // Crear el modal personalizado
    var modalHTML = `
         <div id="confirm-delete-modal" class="modal fade" tabindex="-1" data-bs-backdrop="static" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-sm">
        <div class="modal-content rounded-8">
          <div class="modal-body p-4 text-center">
            <h5 class="mb-0">${title}</h5>
            <p class="mb-0">${content}</p>
          </div>
          <div class="modal-footer flex-nowrap p-0">
            <button type="button" id="confirm-delete-button" class="btn btn-lg btn-link fs-6 text-decoration-none col-6 m-0 rounded-0 border-right">
              <strong class="text-danger">Sí, eliminar</strong>
            </button>
            <button type="button" id="cancel-delete-button" class="btn btn-lg btn-dark fs-6 text-decoration-none col-6 m-0 rounded-0" data-bs-dismiss="modal">
              No gracias
            </button>
          </div>
        </div>
      </div>
    </div>
  `;

    // Agregar el modal al DOM
    var modalContainer = document.createElement('div');
    modalContainer.innerHTML = modalHTML;
    document.body.appendChild(modalContainer);

    // Obtener los botones del modal
    var modal = document.getElementById('confirm-delete-modal');
    var confirmButton = document.getElementById('confirm-delete-button');
    var cancelButton = document.getElementById('cancel-delete-button');

    // Mostrar el modal
    var modalInstance = new bootstrap.Modal(modal);
    modalInstance.show();


    // Agregar eventos a los botones
    confirmButton.addEventListener('click', function () {
        // Realizar la solicitud AJAX para eliminar el objeto
        $.ajax({
            url: url,
            data: parameters,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            processData: false,
            contentType: false,
            success: function (request) {
                if (!request.hasOwnProperty('error')) {
                    callback(request);
                    return false;
                }
                message_error(request.error);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                message_error(errorThrown + ' ' + textStatus);
            }
        });

        // Ocultar el modal y eliminarlo del DOM
        modalInstance.hide();
        modalContainer.parentNode.removeChild(modalContainer);
    });

    cancelButton.addEventListener('click', function () {
        // Ocultar el modal y eliminarlo del DOM sin hacer nada
        modalInstance.hide();
        modalContainer.parentNode.removeChild(modalContainer);
    });
}


function updateFilterCount(filterParams) {
    //funcion para mostrar el valor del  filterCount
    //solo muestra el span si se aplico algun filtro

    // Obtén la URL actual
    const urlParams = new URLSearchParams(window.location.search);
    // Contador para realizar el seguimiento de los filtros utilizados
    let filtersUsed = 0;
    // Recorre los nombres de los parámetros de filtro
    filterParams.forEach(param => {
        if (urlParams.has(param) && urlParams.get(param) !== '') {
            filtersUsed++;
        }
    });
    // Actualiza el valor del contador de filtros
    const filterCount = document.getElementById('filterCount');
    filterCount.textContent = filtersUsed;
    if (filtersUsed > 0) {
        filterCount.style.display = 'inline'; // Muestra el elemento <span> si se están utilizando filtros
    } else {
        filterCount.style.display = 'none'; // Oculta el elemento <span> si no se están utilizando filtros
    }
}

function clearFilters(filterParams) {
    //funcion para limpiar los filtros aplicados
    // Obtén la URL actual
    let url = new URL(window.location.href);
    // Elimina los parámetros de filtro de la URL
    filterParams.forEach(param => {
        url.searchParams.delete(param);
    });
    // Recarga la página con la URL actualizada
    window.location.href = url.toString();
}
