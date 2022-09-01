var tblProducts;
var select_user, select_search_product;
var input_daterange;
var tblSearchProducts;


var order = {
    details: {
        products: []
    }, getProductsIds: function () {
        return this.details.products.map(value => value.id);
    }, addProduct: function (item) {
        this.details.products.push(item);
        this.listProducts();
    }, listProducts: function () {

        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.details.products,
            columns: [
                {"data": "id"},
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
                        return '<a rel="remove" class="btn-sm app-btn-secondary" ><i class="fa-regular fa-trash-alt "></i></a>';
                    }
                },
                {
                    targets: [1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img src="' + data + '" class="img-fluid" style="width: 80px; height: 80px;">';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cant + '">';
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
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {

                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1, max: data.stock, step: 1
                });

            },
            initComplete: function (settings, json) {

            }
        });
    },
};

$(function () {

    select_user = $('select[name="username"]');
    select_search_product = $('select[name="search_product"]');
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    // Usuario
    select_user.select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: pathname,
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: function (params) {
                return {
                    term: params.term,
                    action: 'search_user'
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese el usuario o el solapin',
        minimumInputLength: 1,
    });

    // Products
    select_search_product.select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: pathname,
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: function (params) {
                return {
                    term: params.term,
                    action: 'search_products_select2',
                    ids: JSON.stringify(order.getProductsIds())
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1, templateResult: function (repo) {
            if (repo.loading) {
                return repo.text;
            }

            if (!Number.isInteger(repo.id)) {
                return repo.text;
            }

            return $('<div class="wrapper container">' +
                '<div class="row">' +
                '<div class="col-lg-1">' +
                '<img alt="" src="' + repo.img + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
                '</div>' +
                '<div class="col-lg-11 text-left shadow-sm">' +
                //'<br>' +
                '<p style="margin-bottom: 0;">' +
                '<b>Nombre:</b> ' + repo.name + '<br>' +
                '<b>Categoría:</b> <span class="">' + repo.category.name + '</span>' + '<br>' +
                '<b>Stock:  </b>' + '<span class="badge  bg-success">' + repo.stock + '</span>' + ' <br>' +
                '</p>' +
                '</div>' +
                '</div>' +
                '</div>');
        },
    })
        .on('select2:select', function (e) {
            var data = e.params.data;
            if (!Number.isInteger(data.id)) {
                return false;
            }
            data.cant = 1;
            order.addProduct(data);
            select_search_product.val('').trigger('change.select2');
        });

    $('#tblProducts tbody')
        .off()
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar el producto del listado?', function () {
                order.details.products.splice(tr.row, 1);
                tblProducts.row(tr.row).remove().draw();

            }, function () {

            });
        })
        .on('change', 'input[name="cant"]', function () {
            console.clear();
            var cant = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            order.details.products[tr.row].cant = cant;

        });

    $('.btnRemoveAll').on('click', function () {
        if (order.details.products.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los details de tu detalle?', function () {
            order.details.products = [];
            order.listProducts();
        }, function () {

        });
    });

    $('.btnClearSearch').on('click', function () {
        select_search_product.val('').focus();
    });

    $('.btnSearchProducts').on('click', function () {
        tblSearchProducts = $('#tblSearchProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'ids': JSON.stringify(order.getProductsIds()),
                    'term': select_search_product.val()
                },
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                },
            },
            columns: [
                {"data": "full_name"},
                {"data": "img"},
                {"data": "stock"},
                {"data": "category.name"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img src="' + data + '" class="img-fluid d-block mx-auto" style="width: 30px; height: 30px;">';
                    }
                },

                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a rel="add" class="btn-sm app-btn-primary "><i class="fas fa-plus"></i></a> ';
                        return buttons;
                    }
                },],
            initComplete: function (settings, json) {

            }
        });
        $('#myModalSearchProducts').modal('show');

    });

    $('#tblSearchProducts tbody')
        .off()
        .on('click', 'a[rel="add"]', function () {
            var tr = tblSearchProducts.cell($(this).closest('td, li')).index();
            var product = tblSearchProducts.row(tr.row).data();
            product.cant = 1;
            order.addProduct(product);
            tblSearchProducts.row($(this).parents('tr')).remove().draw();
        });

    // Form order

    input_daterange = $('input[name="date_range"]');

    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            minDate: new Date(),
            "applyButtonClasses": "app-btn-primary",
            "cancelClass": "app-btn-secondary",
            locale: {
                format: 'YYYY-MM-DD',
                "applyLabel": "Aplicar",
                "cancelLabel": "Cancelar",
                "fromLabel": "Desde",
                "toLabel": "hasta",
                "customRangeLabel": "Custom",
            }

        });

    $('#frmOrder').on('submit', function (e) {
        e.preventDefault();

        if (order.details.products.length === 0) {
            message_error('Debe al menos tener un item en su detalle de préstamos');
            return false;
        }

        var success_url = this.getAttribute('data-url');
        var parameters = new FormData(this);
        parameters.append('products', JSON.stringify(order.details.products));
        parameters.append('start_date', input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'));
        parameters.append('end_date', input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'));

        submit_with_ajax(pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {

            location.href = success_url;

        });
    });

    order.listProducts();
});

