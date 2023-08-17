var tblloan;
var input_daterange;

var loan = {
    list: function (all) {
        var parameters = {
            'action': 'search',
            'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        };
        if (all) {
            parameters['start_date'] = '';
            parameters['end_date'] = '';
        }
        tblloan = $('#data').DataTable({
            responsive: true,
            scrollX: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            rowId: 'staffId',
            ajax: {
                url: pathname,
                type: 'POST',
                data: parameters,
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: function (data) {
                    console.log(data);
                }
            },
            columns: [
                {"data": "id"},
                {"data": "order"},

                {"data": "order"},
                {"data": "order"},

                {"data": "state"},
                {"data": "id"},
            ],
            order: [[0, "desc"], [2, "desc"]],
            columnDefs: [
                {
                    targets: [1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<div class="card-header-action"><b><a class="" rel="number">' + data + '</a></b></div>'
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.state == 'PR') {
                            return '<div class="badge  bg-danger">Prestado</div>'
                        }
                        if (row.state == 'PE') {
                            return '<div class="badge  bg-warning">Pendiente</div>'
                        }
                        return '<div class="badge bg-success ">Entregado</div>'
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var html = ' <div class="dropdown-icon">\n' +
                            '    <button type="button"\n' +
                            '            class="btn p-0 hide-arrow"\n' +
                            '            data-bs-toggle="dropdown" aria-expanded="false"><i class="bi bi-three-dots-vertical"></i></button>\n' +
                            '      <ul class="dropdown-menu" style="font-size: 14px;">\n' +
                            '        <li><a class="dropdown-item" href="' + pathname + 'detail/' + row.id + '/"> <span><i class="bi bi-eye"></i>  Ver</span></a></li>\n' +
                            '        <li><a class="dropdown-item" href="' + pathname + 'update/' + row.id + '/"> <span><i class="bi bi-pencil"></i>  Modificar</span></a></li>\n' +
                            '        <li><hr class="dropdown-divider"></li>\n' +
                            '        <li><a class="dropdown-item" href="' + pathname + 'invoice/pdf/' + row.id + '/" target="_blank"> <span><i class="bi bi-file-pdf"></i>  Descargar pdf</span></a></li>\n' +
                            // '        <li><a class="dropdown-item" href="' + pathname + 'delete/' + row.id + '/"> <span><i class="bi bi-trash"></i>  Eliminar</span></a></li>\n' +
                            '      </ul>\n' +
                            '</div>';
                        return html;
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });

        tblloan.on('order.dt search.dt', function () {
            tblloan.column(0, {search: 'applied', order: 'applied'}).nodes().each(function (cell, i) {
                cell.innerHTML = i + 1;
            });
        }).draw();
    },


};

$(function () {

    input_daterange = $('input[name="date_range"]');

    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            }
        });


    var start = moment().subtract(5, 'days');
    var end = moment().add(1, 'days');

    function cb(start, end) {
        $('#reportrange span').html(start.format('YYYY-MM-DD') + ' - ' + end.format('YYYY-MM-DD'));
    }

    input_daterange.daterangepicker({
        startDate: start,
        endDate: end,
        ranges: {
            'Hoy': [moment(), moment().add(1, 'days')],
            'Ayer': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            'Últimos 7 días': [moment().subtract(6, 'days'), moment()],
            'Últimos 30 días': [moment().subtract(29, 'days'), moment()],
            'Este mes': [moment().startOf('month'), moment().endOf('month')],
            'El mes pasado': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        }
    }, cb);
    cb(start, end);


    $('.drp-buttons').hide();

    $('.btnSearch').on('click', function () {
        loan.list(false);
    });

    $('.btnSearchAll').on('click', function () {
        loan.list(true);
    });

    $('#data tbody')
        .off()

    loan.list(false);
});
