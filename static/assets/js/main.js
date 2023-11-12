var pathname = window.location.pathname;



// var progressBar = new ProgressBar.Line('#container', {
//     color: '#04966b', // El color de la barra de progreso
//     strokeWidth: 4, // El ancho de la barra de progreso
//     easing: 'easeInOut', // La función de interpolación utilizada para animar la barra de progreso
//     duration: 1000, // La duración de la animación de la barra de progreso (en milisegundos)
//     trailColor: '#f4f4f4', // El color de la pista de la barra de progreso
//     trailWidth: 1, // El ancho de la pista de la barra de progreso
// });
//
// function updateProgressBar() {
//     var total = 0;
//     var loaded = 0;
//     var tags = document.getElementsByTagName('*');
//     for (var i = 0; i < tags.length; i++) {
//         total++;
//         if (tags[i].complete) {
//             loaded++;
//         }
//     }
//     var progress = loaded / total;
//     progressBar.animate(progress, {
//         duration: 1000
//     });
// }
//
// window.onload = function () {
//     updateProgressBar();
// };
//
// // Muestra la barra de progreso cuando se empieza a cargar la página
// NProgress.start();
//
// // Muestra la barra de progreso cuando se empieza a cargar la página
// NProgress.set(0.9); // Puedes establecer manualmente la cantidad de progreso que se ha completado
//
// // Oculta la barra de progreso cuando se completa la carga de la página
// $(window).on('load', function () {
//     NProgress.done();
// });
