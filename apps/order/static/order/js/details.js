var tblProducts;

var order = {
    details: {
        products: []
    }, listProducts: function () {
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            paging: false,// hide showing paging
            "bInfo": false, // hide showing entries
            searching: false,
            data: this.details.products,
            columns: [
                {"data": "img"},
                {"data": "name"},
                {"data": "category.name"},
                {"data": "stock"},
                {"data": "cant"},
                {"data": "state"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img src="' + data + '" class="img-fluid" style="width: 80px; height: 80px;">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false, render: function (data, type, row) {
                        if (row.state == 'D') {
                            return '<div class="badge  bg-success">Disponible</div>'
                        }
                        return '<div class="badge  bg-danger">Prestado</div>'
                    }
                },

            ],
            initComplete: function (settings, json) {
            }
        });
    },
};


$(function () {
    order.listProducts();
});
