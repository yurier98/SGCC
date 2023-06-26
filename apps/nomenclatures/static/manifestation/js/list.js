var manifestation = {
    list: function () {
        tbl = $('#data').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search'
                },
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                },
            },
            columns: [
                {"data": "id"},
                {"data": "name"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [1],
                    class: 'text-left',
                    orderable: false,
                    render: function (data, type, row) {
                        var html = '';
                        html += '<div class="card-header-action"><a href="' + pathname + '/update/' + row.id + '/" class="">' + row.name + '</a></div>';

                        return html;
                    }
                },

                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href="' + pathname + '/update/' + row.id + '/" class="update btn-sm app-btn-secondary"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="' + pathname + '/delete/' + row.id + '/" type="button" class="delete btn-sm app-btn-secondary"><i class="fas fa-trash-alt"></i></a>';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });

        tbl.on('order.dt search.dt', function () {
            tbl.column(0, {search: 'applied', order: 'applied'}).nodes().each(function (cell, i) {
                cell.innerHTML = i + 1;
            });
        }).draw();
    }
};

$(function () {

    $('.btnCreate').on('click', function () {
        $('#myModalManifestation').modal('show');
    });
    $('.btnClose').on('click', function () {
        $('#myModalManifestation').modal('hide');
    });

    $('#myModalManifestation').on('hidden.bs.modal', function (e) {
        $('#frmManifestation').trigger('reset');
    });

    $('#frmManifestation').on('submit', function (e) {
        e.preventDefault();
        var success_url = this.getAttribute('data-url');
        var parameters = new FormData(this);
        parameters.append('action', 'create_manifestation');

        // console.log(response);
        // location.reload();

        // $.ajax({
        //     url: pathname,
        //     type: 'POST',
        //     data: {
        //         'action': 'create_manifestation'
        //     },
        //     dataSrc: "",
        //     headers: {
        //         'X-CSRFToken': csrftoken
        //     },
        //     // parameters,
        //     success: function (data) {
        //         // modalDiv.html(data);
        //         $('#myModalManifestation').modal('hide');
        //     }
        // });

        submit_with_ajax(pathname, 'Notificación',
            '¿Estas seguro de crear la siguiente manifestación?', parameters, function (response) {
                console.log(response);
                location.reload();
                $('#myModalManifestation').modal('hide');
            });
    });


    manifestation.list();
});

