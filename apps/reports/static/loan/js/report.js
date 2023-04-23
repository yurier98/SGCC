var input_daterange;
var tblloan;
var report = {
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
                    autoWidth: false,
                    destroy: true,
                    deferRender: true,
                    ajax: {
                        url: pathname,
                        type: 'POST',
                        data: parameters,
                        dataSrc: "",
                        headers: {
                            'X-CSRFToken': csrftoken
                        },
                    },
                    order: false,
                    paging: false,
                    ordering: false,
                    info: false,
                    searching: false,
                    dom: 'Bfrtip',
                    buttons: [
                        {
                            extend: 'excelHtml5',
                            text: '<i class="fas fa-file-excel"></i> Descargar Excel ',
                            titleAttr: 'Excel',
                            className: 'btn app-btn-primary btn-flat',
                        },
                        {
                            extend: 'pdfHtml5',
                            text: '<i class="fas fa-file-pdf"></i> Descargar Pdf ',
                            titleAttr: 'PDF',
                            className: 'btn app-btn-secondary',
                            download: 'open',
                            orientation: 'landscape',
                            pageSize: 'LEGAL',
                            customize: function (doc) {
                                doc.styles = {
                                    header: {
                                        fontSize: 18,
                                        bold: true,
                                        alignment: 'center'
                                    },
                                    subheader: {
                                        fontSize: 13,
                                        bold: true
                                    },
                                    quote: {
                                        italics: true
                                    },
                                    small: {
                                        fontSize: 8
                                    },
                                    tableHeader: {
                                        bold: true,
                                        fontSize: 11,
                                        color: 'white',
                                        fillColor: '#2d4154',
                                        alignment: 'center'
                                    }
                                };
                                doc.content[1].table.widths = ['20%', '20%', '15%', '15%', '15%', '15%'];
                                doc.content[1].margin = [0, 35, 0, 0];
                                doc.content[1].layout = {};
                                doc['footer'] = (function (page, pages) {
                                    return {
                                        columns: [
                                            {
                                                alignment: 'left',
                                                text: ['Fecha de creación: ', {text: new moment().format('DD-MM-YYYY')}]
                                            },
                                            {
                                                alignment: 'right',
                                                text: ['página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                            }
                                        ],
                                        margin: 20
                                    }
                                });

                            }
                        }
                    ],
                    columns: [

                        {"data": "id"},
                        {"data": "user.full_name"},
                        {"data": "user.area"},
                        {"data": "user.phone"},
                        {"data": "loanproduct"},
                        {"data": "loanproduct"},
                        {"data": "created"},


                    ],
                    columnDefs: [
                        {
                            targets: [1],
                            class: 'text-left',
                            render: function (data, type, row) {
                                return '<div class="card-header-action"><b><a class="" rel="number">' + data + '</a></b></div>'
                            }
                        },
                        {
                            targets: [-3],
                            class: 'text-left',
                            render: function (data, type, row) {
                                var html = '';
                                $.each(row.loanproduct, function (key, value) {
                                    html += '<span class="">' + value.product.full_name + ',</span> ';
                                });
                                return html
                            }
                        },
                        {
                            targets: [-2],
                            class: 'text-left',
                            render: function (data, type, row) {
                                var html = '';
                                $.each(row.loanproduct, function (key, value) {
                                    html += '<span class="">' + value.cant + '</span> ';
                                });
                                return html
                            }
                        },
                    ],
                    initComplete: function (settings, json) {

                    }
                }
            );
        },
        formatRowHtml: function (d) {
            var html = '<table class="table app-table-hover mb-0 text-left">';
            html += '<thead class="thead-dark">';
            html += '<tr><th class="cell" scope="col">Producto</th>';
            html += '<th class="cell" scope="col">Categoría</th>';
            html += '<th class="cell" scope="col">Cantidad</th>';
            html += '</thead>';
            html += '<tbody>';
            $.each(d.loanproduct, function (key, value) {
                html += '<tr>'
                html += '<td>' + value.product.name + '</td>'
                html += '<td>' + value.product.category.name + '</td>'
                html += '<td>' + value.cant + '</td>'
                html += '</tr>';
            });
            html += '</tbody>';
            return html;
        }
    }
;

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

    // input_daterange
    //     .daterangepicker({
    //         language: 'auto',
    //         startDate: new Date(),
    //         locale: {
    //             format: 'YYYY-MM-DD',
    //             applyLabel: '<i class="fas fa-chart-pie"></i> Aplicar',
    //             cancelLabel: '<i class="fas fa-times"></i> Cancelar',
    //         },
    //     })
    //     .on('hide.daterangepicker', function (ev, picker) {
    //         report.list();
    //     });

    $('.drp-buttons').hide();

    $('.btnSearch').on('click', function () {
        report.list(false);
    });

    $('.btnSearchAll').on('click', function () {
        report.list(true);
    });


    $('#data tbody')
        .off()
        .on('click', 'a[rel="number"]', function () {
            var tr = $(this).closest('tr');
            var row = tblloan.row(tr);
            if (row.child.isShown()) {
                row.child.hide();
                tr.removeClass('shown');
            } else {
                row.child(report.formatRowHtml(row.data())).show();
                tr.addClass('shown');
            }
        });
    report.list(false);
});