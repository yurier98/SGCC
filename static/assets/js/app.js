'use strict';

/* ===== Enable Bootstrap tooltip (on element  ====== */
// $(function () {
//     $('[data-toggle="tooltip"]').tooltip()
// })

/* ===== Enable Bootstrap Popover (on element  ====== */
const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

/* ==== Enable Bootstrap Alert ====== */
//var alertList = document.querySelectorAll('.alert')
//alertList.forEach(function (alert) {
//  new bootstrap.Alert(alert)
//});

const alertList = document.querySelectorAll('.alert')
const alerts = [...alertList].map(element => new bootstrap.Alert(element))


/* ===== Responsive Sidepanel ====== */
const sidePanelToggler = document.getElementById('sidepanel-toggler');
const sidePanel = document.getElementById('app-sidepanel');
const sidePanelDrop = document.getElementById('sidepanel-drop');
const sidePanelClose = document.getElementById('sidepanel-close');

window.addEventListener('load', function () {
    responsiveSidePanel();
});

window.addEventListener('resize', function () {
    responsiveSidePanel();
});


function responsiveSidePanel() {
    let w = window.innerWidth;
    if (w >= 1200) {
        // if larger
        //console.log('larger');
        sidePanel.classList.remove('sidepanel-hidden');
        sidePanel.classList.add('sidepanel-visible');

    } else {
        // if smaller
        //console.log('smaller');
        sidePanel.classList.remove('sidepanel-visible');
        sidePanel.classList.add('sidepanel-hidden');
    }
};

sidePanelToggler.addEventListener('click', () => {
    if (sidePanel.classList.contains('sidepanel-visible')) {
        console.log('visible');
        sidePanel.classList.remove('sidepanel-visible');
        sidePanel.classList.add('sidepanel-hidden');

    } else {
        console.log('hidden');
        sidePanel.classList.remove('sidepanel-hidden');
        sidePanel.classList.add('sidepanel-visible');
    }
});


sidePanelClose.addEventListener('click', (e) => {
    e.preventDefault();
    sidePanelToggler.click();
});

sidePanelDrop.addEventListener('click', (e) => {
    sidePanelToggler.click();
});















var toastLiveExample = document.getElementById('liveToast');

// Función para obtener los mensajes del servidor
function getMessages() {
    // Enviar una solicitud AJAX para obtener los mensajes
    $.ajax({
        url: '/messages/',
        type: 'GET',
        success: function(data) {
            // Si hay mensajes, mostrar la notificación
            if (data.messages.length > 0) {
                console.log(data.messages)
                var toast = new bootstrap.Toast(toastLiveExample);
                toast.show();
            }
        }
    });
}

// Llamar a la función obtenerMensajes() cuando se cargue la página
$(document).ready(function() {
    getMessages();
});

