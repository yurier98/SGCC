var tblProducts;
var select_user, select_search_product;
var input_daterange;
var tblSearchProducts;


var loan = {
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
                    ids: JSON.stringify(loan.getProductsIds())
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
            loan.addProduct(data);
            select_search_product.val('').trigger('change.select2');
        });

    $('#tblProducts tbody')
        .off()
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar el producto del listado?', function () {
                loan.details.products.splice(tr.row, 1);
                tblProducts.row(tr.row).remove().draw();

            }, function () {

            });
        })
        .on('change', 'input[name="cant"]', function () {
            console.clear();
            var cant = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            loan.details.products[tr.row].cant = cant;

            // $('td:last', tblProducts.row(tr.row).node()).html('$' + loan.details.products[tr.row].cant.toFixed(2));
        });

    $('.btnRemoveAll').on('click', function () {
        if (loan.details.products.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los details de tu detalle?', function () {
            loan.details.products = [];
            loan.listProducts();
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
                    'ids': JSON.stringify(loan.getProductsIds()),
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
            loan.addProduct(product);
            tblSearchProducts.row($(this).parents('tr')).remove().draw();
        });

    // Form Loan

    input_daterange = $('input[name="date_range"]');

    // input_daterange
    //     .daterangepicker({
    //         language: 'auto',
    //         startDate: new Date(),
    //         minDate: new Date(),
    //         locale: {
    //             format: 'YYYY-MM-DD',
    //         }
    //     });

    input_daterange
        .daterangepicker({
                language: 'auto',
                // startDate: "start_date",
                // endDate: "end_date",
                // minDate: new Date(),
                locale: {
                    language: 'es',
                    format: 'YYYY-MM-DD',
                    "applyLabel": "Aplicar",
                    "cancelLabel": "Cancelar",
                    "fromLabel": "Desde",
                    "toLabel": "hasta",
                    "customRangeLabel": "Custom",
                },
                // "startDate": "2022/08/02",
                // "endDate": "2022/08/25",
                // "buttonClasses": "btn-sm ",
                "applyButtonClasses": "app-btn-primary",
                "cancelClass": "app-btn-secondary",


                // getValue: function () {
                //     $('#startDate').val() + 'to' + $('#endDate').val();
                // },
                // setValue: function () {
                //     $('#startDate').val('2000-09-09');
                //     $('#endDate').val("startDate");
                // }
            }, function (start, end, label) {
                console.log("A new date selection was made: " + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD'));

            }
        );
    var startDate = $("start_date").val();
    var endDate = $("end_date").val();

    // input_daterange.data('daterangepicker').setDateRanger(startDate, endDate).format('YYYY-MM-DD')
    // input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD').setValue(startDate)

    console.log("Fechas : " + $("start_date").val());


    $('#frmLoan').on('submit', function (e) {
        e.preventDefault();

        if (loan.details.products.length === 0) {
            message_error('Debe al menos tener un item en su detalle de préstamos');
            return false;
        }

        var success_url = this.getAttribute('data-url');
        var parameters = new FormData(this);
        parameters.append('products', JSON.stringify(loan.details.products));
        parameters.append('start_date', input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'));
        parameters.append('end_date', input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'));

        submit_with_ajax(pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
            alert_action('Notificación', '¿Desea imprimir la boleta de préstamos?', function () {
                window.open('/loan/invoice/pdf/' + response.id + '/', '_blank');
                location.href = success_url;
            }, function () {
                location.href = success_url;
            });
        });
    });

    loan.listProducts();
});

