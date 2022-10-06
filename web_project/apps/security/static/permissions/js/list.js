var permission = {
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
                // {"data": "name"},
                {"data": "content_type_id"},
                {"data": "codename"},
                {"data": "id"},
            ],
            columnDefs: [

                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {

                        console.log(row.content_type_id);

                        var html = '<span class="">' + row.content_type_id + '</span> ';

                        return html
                    }
                },
                {
                    targets: [-2],
                    class: 'text-left',
                    orderable: false,
                    render: function (data, type, row) {
                        var html = '<span class=" badge bg-success">' + row.codename + '</span> ';
                        return html
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
    permission.list();
});