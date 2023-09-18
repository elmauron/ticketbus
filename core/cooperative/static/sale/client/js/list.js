var tblSale;
var input_date_range;
var sale = {
    list: function (all) {
        var parameters = {
            'action': 'search',
            'start_date': input_date_range.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_date_range.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        };
        if (all) {
            parameters['start_date'] = '';
            parameters['end_date'] = '';
        }
        tblSale = $('#data').DataTable({
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: parameters,
                dataSrc: ""
            },
            order: [[0, "desc"]],
            columns: [
                {data: "number"},
                {data: "client.user.names"},
                {data: "payment_method.name"},
                {data: "type_voucher.name"},
                {data: "date_joined"},
                {data: "hour_joined"},
                {data: "cant_tikets"},
                {data: "total"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
                {
                    targets: [2, 3, 4, 5],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data.toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var buttons = '<a class="btn btn-info btn-xs btn-flat" rel="detail" data-toggle="tooltip" title="Detalle"><i class="fas fa-folder-open"></i></a> ';
                        buttons += '<a href="' + pathname + 'print/invoice/' + row.id + '/" target="_blank" data-toggle="tooltip" title="Imprimir" class="btn btn-primary btn-xs btn-flat"><i class="fas fa-print"></i></a>';
                        return buttons;
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $('[data-toggle="tooltip"]').tooltip();
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    }
};

$(function () {

    input_date_range = $('input[name="date_range"]');

    $('#data tbody')
        .off()
        .on('click', 'a[rel="detail"]', function () {
            $('.tooltip').remove();
            var tr = tblSale.cell($(this).closest('td, li')).index();
            var row = tblSale.row(tr.row).data();
            $('#tblDetails').DataTable({
                autoWidth: false,
                destroy: true,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_detail_tickets',
                        'id': row.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "route.bus.name"},
                    {data: "route.bus.plaque"},
                    {data: "route.bus.car_disk"},
                    {data: "route.place.name"},
                    {data: "route.departure_time"},
                    {data: "seat"},
                    {data: "route.price"},
                ],
                columnDefs: [
                    {
                        targets: [-1],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + data.toFixed(2);
                        }
                    },
                    {
                        targets: [-2, -3, -5],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    }
                ]
            });
            var invoice = [];
            invoice.push({'id': 'Cliente', 'name': row.client.user.names});
            invoice.push({'id': 'Método de Pago', 'name': row.payment_method.name});
            invoice.push({'id': 'Subtotal', 'name': '$' + row.subtotal.toFixed(2)});
            invoice.push({'id': 'Iva', 'name': row.iva.toFixed(2) + ' %'});
            invoice.push({'id': 'Total Iva', 'name': '$' + row.total_iva.toFixed(2)});
            invoice.push({'id': 'Total a pagar', 'name': '$' + row.total.toFixed(2)});
            if (row.payment_method.id === 'efectivo') {
                invoice.push({'id': 'Efectivo', 'name': '$' + row.cash.toFixed(2)});
                invoice.push({'id': 'Vuelto', 'name': '$' + row.change.toFixed(2)});
            } else if (row.payment_method.id === 'tarjeta_debito_credito') {
                invoice.push({'id': 'Número de tarjeta', 'name': row.card_number});
                invoice.push({'id': 'Titular de tarjeta', 'name': row.card_titular});
                invoice.push({'id': 'Año/Mes', 'name': row.card_year});
                invoice.push({'id': 'Tipo de Tarjeta', 'name': row.card_type.name});
                invoice.push({'id': 'CCV', 'name': 'XXX'});
                invoice.push({'id': 'Monto a debitar', 'name': '$' + row.card_amount_debited.toFixed(2)});
            } else if (row.payment_method.id === 'efectivo_tarjeta') {
                invoice.push({'id': 'Efectivo', 'name': '$' + row.cash.toFixed(2)});
                invoice.push({'id': 'Número de tarjeta', 'name': row.card_number});
                invoice.push({'id': 'Titular de tarjeta', 'name': row.card_titular});
                invoice.push({'id': 'Año/Mes', 'name': row.card_year});
                invoice.push({'id': 'Tipo de Tarjeta', 'name': row.card_type.name});
                invoice.push({'id': 'CCV', 'name': 'XXX'});
                invoice.push({'id': 'Monto a debitar', 'name': '$' + row.card_amount_debited.toFixed(2)});
            }
            $('#tblInvoice').DataTable({
                autoWidth: false,
                destroy: true,
                data: invoice,
                paging: false,
                ordering: false,
                info: false,
                columns: [
                    {data: "id"},
                    {data: "name"},
                ],
                columnDefs: [
                    {
                        targets: [0, 1],
                        class: 'text-left',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('.nav-tabs a[href="#home"]').tab('show');
            $('#myModalDetails').modal('show');
        });

    input_date_range
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            }
        });

    $('.drp-buttons').hide();

    sale.list(false);

    $('.btnSearch').on('click', function () {
        sale.list(false);
    });

    $('.btnSearchAll').on('click', function () {
        sale.list(true);
    });
});
