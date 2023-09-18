var fvSale;
var select_route, select_place, select_bus;
var input_card_number, input_card_titular, input_year_card;
var tblTickets;

var sale = {
    details: {
        tickets: [],
    },
    route: null,
    calculateInvoice: function () {
        sale.details.subtotal = this.details.tickets.reduce(function (accumulator, currentValue) {
            return accumulator + currentValue.route.price;
        }, 0);
        sale.details.total_iva = sale.details.subtotal * (sale.details.iva / 100);
        sale.details.total = sale.details.subtotal + sale.details.total_iva;
        $('input[name="subtotal"]').val(sale.details.subtotal.toFixed(2));
        $('input[name="iva"]').val(sale.details.iva.toFixed(2));
        $('input[name="total_iva"]').val(sale.details.total_iva.toFixed(2));
        $('input[name="total"]').val(sale.details.total.toFixed(2));
        $('input[name="amount"]').val(sale.details.total.toFixed(2));
    },
    listTickets: function () {
        this.calculateInvoice();
        tblTickets = $('#tblTickets').DataTable({
            autoWidth: false,
            destroy: true,
            data: this.details.tickets,
            lengthChange: false,
            searching: false,
            paginate: false,
            columns: [
                {data: "route.bus.name"},
                {data: "route.place.name"},
                {data: "route.departure_time"},
                {data: "route.bus.car_disk"},
                {data: "seat"},
                {data: "route.price"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs"><i class="fas fa-times"></i></a>';
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
                    targets: [-3, -4, -5],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    },
    searchSeat: function (item) {
        return this.details.tickets.findIndex(value => value.seat === item.seat && parseInt(value.route.id) === parseInt(item.route.id));
    },
    addTicket: function (item) {
        var position = this.searchSeat(item);
        if (position === -1) {
            this.details.tickets.push(item);
        } else {
            this.details.tickets.splice(position, 1);
        }
        this.listTickets();
        return position === -1;
    },
    listBusSeats: function () {
        var content = '';
        if (!$.isEmptyObject(this.route)) {
            var cant = this.route.bus.car_seats;
            var occupied = this.route.occupied;
            for (let i = 1; i <= cant; i++) {
                var verify_seat = occupied.includes(i);
                var search = this.details.tickets.filter(function (item, key) {
                    return item.seat === i && item.route.id === sale.route.id;
                });
                if (search.length > 0 || verify_seat) {
                    content += '<button type="button" class="btn btn-app bg-gradient-danger ticket" disabled data-route="' + sale.route.id + '" data-seat="' + i + '">';
                } else {
                    content += '<button type="button" class="btn btn-app bg-secondary ticket" data-route="' + sale.route.id + '" data-seat="' + i + '">';
                }
                if (verify_seat) {
                    content += '<span class="badge bg-success">Ocupado</span>';
                }
                content += ' <i class="fas fa-bus-alt mb-1"></i> Asiento ' + i;
                content += '</button>';
            }
        }
        $('.tickets').html(content);
    },
    clearSelect: function (names) {
        var items = [{'id': '', 'text': '--------------'}];
        names.forEach(function (name) {
            $('select[name="' + name + '"]').html('').select2({
                data: items,
                theme: 'bootstrap4',
                language: "es"
            });
        });
    }
};

document.addEventListener('DOMContentLoaded', function (e) {
    fvSale = FormValidation.formValidation(document.getElementById('frmForm'), {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                excluded: new FormValidation.plugins.Excluded(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                place: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una destino'
                        },
                    }
                },
                bus: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un bus'
                        },
                    }
                },
                route: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una ruta'
                        },
                    }
                },
                type_voucher: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un tipo de comprobante'
                        },
                    }
                },
                card_type: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un tipo de tarjeta'
                        },
                    }
                },
                card_year: {
                    validators: {
                        regexp: {
                            regexp: /^([0-9]{1,2}([/][0-9]{2}))+$/i,
                            message: 'Debe ingresar el mes y el año en el siguiente formato 01/20'
                        },
                        notEmpty: {},
                    }
                },
                card_number: {
                    validators: {
                        notEmpty: {},
                        // creditCard: {
                        //     message: 'El número de tarjeta de crédito no es válido.',
                        // },
                        regexp: {
                            regexp: /^\d{4}\s\d{4}\s\d{4}\s\d{4}$/,
                            message: 'Debe ingresar un numéro de tarjeta en el siguiente formato 1234 5678 9103 2247'
                        },
                        stringLength: {
                            min: 2,
                            max: 19,
                        },
                    }
                },
                card_code_verification: {
                    validators: {
                        notEmpty: {}
                    }
                },
                card_titular: {
                    validators: {
                        notEmpty: {
                            enabled: false,
                        },
                        stringLength: {
                            min: 3,
                        },
                    }
                },
            },
        }
    )
        .on('core.element.validated', function (e) {
            if (e.valid) {
                const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                if (groupEle) {
                    FormValidation.utils.classSet(groupEle, {
                        'has-success': false,
                    });
                }
                FormValidation.utils.classSet(e.element, {
                    'is-valid': false,
                });
            }
            const iconPlugin = fvSale.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(fvSale.form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            if (sale.details.tickets.length === 0) {
                message_error('Debe tener al menos un asiento en el detalle de la venta');
                return false;
            }
            var params = new FormData(fvSale.form);
            params.append('tickets', JSON.stringify(sale.details.tickets));
            params.append('type_voucher', $('select[name="type_voucher"]').val());
            params.append('card_number', input_card_number.val());
            params.append('card_titular', input_card_titular.val());
            params.append('card_type', $('select[name="card_type"]').val());
            params.append('card_year', input_year_card.val());
            params.append('card_code_verification', $('input[name="card_code_verification"]').val());
            var list_url = $(fvSale.form).attr('data-url');
            var args = {
                'params': params,
                'success': function (request) {
                    dialog_action({
                        'content': '¿Desea Imprimir el Comprobante?',
                        'success': function () {
                            window.open(request.print_url, '_blank');
                            location.href = list_url;
                        },
                        'cancel': function () {
                            location.href = list_url;
                        }
                    });
                }
            };
            submit_with_formdata(args);
        });
});

$(function () {

    select_route = $('select[name="route"]');
    select_bus = $('select[name="bus"]');
    select_place = $('select[name="place"]');
    input_card_number = $('input[name="card_number"]');
    input_card_titular = $('input[name="card_titular"]');
    input_year_card = $('input[name="card_year"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    /* Tickets */

    select_place.on('change', function () {
        fvSale.validateField('place').then(function (status) {
            sale.clearSelect(['bus', 'route']);
            sale.route = []
            sale.listBusSeats();
            if (status === 'Valid') {
                $.ajax({
                    url: pathname,
                    data: {
                        'action': 'search_bus_by_place',
                        'place': select_place.val(),
                    },
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    dataType: 'json',
                    beforeSend: function () {

                    },
                    success: function (request) {
                        if (!request.hasOwnProperty('error')) {
                            select_bus.html('').select2({
                                data: request,
                                theme: 'bootstrap4',
                                language: "es"
                            });
                            select_bus.trigger('change');
                            return false;
                        }
                        message_error(request.error);
                    },
                    error: function (jqXHR, textStatus, errorThrown) {
                        message_error(errorThrown + ' ' + textStatus);
                    }
                });
            }
        });
    });

    select_bus.on('change', function () {
        fvSale.validateField('bus').then(function (status) {
            sale.clearSelect(['route']);
            sale.route = []
            sale.listBusSeats();
            if (status === 'Valid') {
                $.ajax({
                    url: pathname,
                    data: {
                        'action': 'search_route_by_bus',
                        'place': select_place.val(),
                        'bus': select_bus.val(),
                    },
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    dataType: 'json',
                    beforeSend: function () {

                    },
                    success: function (request) {
                        if (!request.hasOwnProperty('error')) {
                            select_route.html('').select2({
                                data: request,
                                theme: 'bootstrap4',
                                language: "es"
                            });
                            select_route.trigger('change');
                            return false;
                        }
                        message_error(request.error);
                    },
                    error: function (jqXHR, textStatus, errorThrown) {
                        message_error(errorThrown + ' ' + textStatus);
                    }
                });
            }
        });
    });

    select_route
        .on('change', function () {
            fvSale.validateField('route').then(function (status) {
                sale.route = []
                if (status === 'Valid') {
                    sale.route = select_route.select2('data')[0];
                }
                sale.listBusSeats();
            });
        });

    $('body').on('click', 'button.ticket', function () {
        var item = {
            'seat': parseInt($(this).data('seat')),
            'route': sale.route
        };
        //$(this).attr('disabled', true);
        if (sale.addTicket(item)) {
            $(this).removeClass('bg-secondary').addClass('bg-gradient-danger');
        } else {
            $(this).removeClass('bg-gradient-danger').addClass('bg-secondary');
        }
        sale.calculateInvoice();
    });

    $('#tblTickets tbody')
        .off()
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblTickets.cell($(this).closest('td, li')).index();
            var ticket = sale.details.tickets[tr.row];
            sale.details.tickets.splice(tr.row, 1);
            tblTickets.row(tr.row).remove().draw();
            var button = $('body').find('button.ticket[data-route="' + ticket.route.id + '"][data-seat="' + ticket.seat + '"]');
            button.prop('disabled', false);
            button.removeClass('bg-gradient-danger').addClass('bg-secondary');
            sale.calculateInvoice();
            //sale.listBusSeats();
            //sale.listTickets();
        });

    /* Card */

    input_card_number
        .on('keypress', function (e) {
            fvSale.revalidateField('card_number');
            return validate_text_box({'event': e, 'type': 'numbers_spaceless'});
        })
        .on('keyup', function (e) {
            var number = $(this).val();
            var number_nospaces = number.replace(/ /g, "");
            if (number_nospaces.length % 4 === 0 && number_nospaces.length > 0 && number_nospaces.length < 16) {
                number += ' ';
            }
            $(this).val(number);
        });

    input_card_titular.on('keypress', function (e) {
        return validate_text_box({'event': e, 'type': 'letters'});
    });

    input_year_card.on('change.datetimepicker', function (e) {
        fvSale.revalidateField('card_year');
    });

    input_year_card.datetimepicker({
        viewMode: 'years',
        format: 'MM/YY',
        useCurrent: false,
    });

    $('.btnShowCodeVerif').on('click', function () {
        var i = $(this).find('i');
        var input = $(this).parent().parent().find('input');
        if (i.hasClass('fas fa-eye-slash')) {
            i.removeClass();
            i.addClass('far fa-eye');
            input.attr('type', 'password');
        } else {
            i.removeClass();
            i.addClass('fas fa-eye-slash');
            input.attr('type', 'text');
        }
    });

    $('.btnRemoveTicketsAll').on('click', function () {
        if (sale.details.tickets.length === 0) return false;
        dialog_action({
            'success': function () {
                sale.details.tickets = [];
                sale.listTickets();
                sale.listBusSeats();
                sale.calculateInvoice();
            },
            'cancel': function () {

            }
        });
    });

    $('i[data-field="card_code_verification"]').hide();
});