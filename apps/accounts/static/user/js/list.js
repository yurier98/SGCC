var user = {
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
                {"data": "full_name"},
                {"data": "username"},
                {"data": "date_joined"},
                {"data": "image"},

                {"data": "groups"},
                {"data": "is_active"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var html = '';
                        html += '<div class="card-header-action"><a href="' + pathname + '/update/' + row.id + '/" class="">' + row.full_name + '</a></div>';

                        return html;
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img alt="" src="' + row.image + '" class="rounded-circle img-fluid " style="width: 50px; height: 50px;">';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var html = '';
                        $.each(row.groups, function (key, value) {
                            html += '<span class=" badge bg-success">' + value.name + '</span> ';
                        });
                        return html
                    }
                },

                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        if (row.is_active == true) {
                            return '<span class=""><i class="bi bi-check-circle-fill" style="color: #15a362;"></i></span>'
                        }
                        return '<span class=""><i class="bi bi-x-circle-fill" style="color: #fb866a;"></i></span>'
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href="' + pathname + '/update/' + row.id + '/" class="btn-sm app-btn-secondary"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="' + pathname + '/delete/' + row.id + '/" type="button" class="btn-sm app-btn-secondary"><i class="fas fa-trash-alt"></i></a>';
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
    user.list();
});