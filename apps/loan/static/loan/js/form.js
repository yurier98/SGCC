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
                        return '<img src="' + data + '" class="" style="width: 60px; height: 60px; border-radius: 8px;">';
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

            return $('       <div class="row justify-content-between align-items-center">\n' +
                '                        <div class="col-auto">\n' +
                '                            <div class="d-flex align-items-center row">\n' +
                '                                <div class="col-auto">\n' +
                '                                    <!-- Avatar place holder -->\n' +
                '                                    <span class="avatar avatar-md">\n' +
                '                                        <img class="avatar-img" style="border-radius: 8px"\n' +
                '                                             src="' + repo.img + '" alt="">\n' +
                '                                    </span>\n' +
                '                                </div>\n' +
                '                                <div class="col-auto">\n' +
                '                                    <div class="item-label"><strong>' + repo.name + '</strong></div>\n' +
                '                                    <div class="item-data">Categoría: ' + repo.category.name + '</div>\n' +
                '                                    <div class="item-data">En almacen: ' + '<span class="badge  bg-success">' + repo.stock + '</span>' + '</div>\n' +
                '                                </div>\n' +
                '                            </div>\n' +
                '                        </div>\n' +
                '                    </div>');
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
        alert_action('Notificación', '¿Estas seguro de eliminar todos el listado de productos?', function () {
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
                {"data": "img"},
                {"data": "name"},
                {"data": "stock"},
                {"data": "category.name"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img src="' + data + '" class="" style="width: 60px; height: 60px; border-radius: 8px;" >';
                    }
                },

                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a rel="add" class="btn app-btn-primary "><i class="bi-cart-plus"></i></a> ';
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

    input_daterange
        .daterangepicker({
                language: 'auto',
                startDate: new Date(),
                minDate: new Date(),
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
                console.log("Los productos son: " + JSON.stringify(loan.details.products));
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

