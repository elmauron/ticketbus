var fvSale, fvClient;
var select_client, select_payment_method, select_route, select_place, select_bus;
var input_birthdate, input_cash, input_card_number, input_card_amount_debited, input_card_titular, input_year_card, input_change, inputs_vents;
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
        input_card_amount_debited.val(sale.details.total.toFixed(2));
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
    },
    setOptionsFields: function (inputs) {
        inputs.forEach(function (value, index, array) {
            if (value.enable) {
                $(inputs_vents[value.index]).show();
            } else {
                $(inputs_vents[value.index]).hide();
            }
        });
    },
};

document.addEventListener('DOMContentLoaded', function (e) {
    fvClient = FormValidation.formValidation(document.getElementById('frmClient'), {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                names: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                dni: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 10
                        },
                        digits: {},
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    parameter: fvClient.form.querySelector('[name="dni"]').value,
                                    pattern: 'dni',
                                    action: 'validate_client'
                                };
                            },
                            message: 'El número de documento ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                mobile: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 7
                        },
                        digits: {},
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    parameter: fvClient.form.querySelector('[name="mobile"]').value,
                                    pattern: 'mobile',
                                    action: 'validate_client'
                                };
                            },
                            message: 'El número de teléfono ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                email: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 5
                        },
                        regexp: {
                            regexp: /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/i,
                            message: 'El formato email no es correcto'
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    parameter: fvClient.form.querySelector('[name="email"]').value,
                                    pattern: 'email',
                                    action: 'validate_client'
                                };
                            },
                            message: 'El email ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                address: {
                    validators: {
                        stringLength: {
                            min: 2,
                        }
                    }
                },
                image: {
                    validators: {
                        file: {
                            extension: 'jpeg,jpg,png',
                            type: 'image/jpeg,image/png',
                            maxFiles: 1,
                            message: 'Introduce una imagen válida'
                        }
                    }
                },
                birthdate: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        }
                    },
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
            const iconPlugin = fvClient.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(fvClient.form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var params = new FormData(fvClient.form);
            params.append('action', 'create_client');
            var args = {
                'params': params,
                'success': function (request) {
                    var newOption = new Option(request.user.names + ' / ' + request.dni, request.id, false, true);
                    select_client.append(newOption).trigger('change');
                    fvSale.revalidateField('client');
                    $('#myModalClient').modal('hide');
                }
            };
            submit_with_formdata(args);
        });
});

document.addEventListener('DOMContentLoaded', function (e) {
    function validateChange() {
        var cash = parseFloat(input_cash.val());
        var method_payment = select_payment_method.val();
        var total = sale.details.total;
        if (method_payment === 'efectivo') {
            if (cash < total) {
                return {valid: false, message: 'El efectivo debe ser mayor o igual al total a pagar'};
            }
        } else if (method_payment === 'efectivo_tarjeta') {
            var amount_debited = total - cash;
            input_card_amount_debited.val(amount_debited.toFixed(2));
        }
        return {valid: true};
    }

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
                client: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un cliente'
                        },
                    }
                },
                payment_method: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un método de pago'
                        },
                    }
                },
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
                card_amount_debited: {
                    validators: {
                        notEmpty: {
                            enabled: false,
                        },
                        numeric: {
                            message: 'El valor no es un número',
                            thousandsSeparator: '',
                            decimalSeparator: '.'
                        },
                        callback: {
                            message: 'El monto a debitar no puede ser menor al total a pagar',
                            callback: function (input) {
                                return validateAmountDebited();
                            }
                        }
                    }
                },
                cash: {
                    validators: {
                        notEmpty: {},
                        numeric: {
                            message: 'El valor no es un número',
                            thousandsSeparator: '',
                            decimalSeparator: '.'
                        }
                    }
                },
                change: {
                    validators: {
                        notEmpty: {},
                        callback: {
                            //message: 'El cambio no puede ser negativo',
                            callback: function (input) {
                                return validateChange();
                            }
                        }
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
            params.append('payment_method', select_payment_method.val());
            params.append('type_voucher', $('select[name="type_voucher"]').val());
            params.append('cash', input_cash.val());
            params.append('change', input_change.val());
            params.append('card_number', input_card_number.val());
            params.append('card_titular', input_card_titular.val());
            params.append('card_amount_debited', input_card_amount_debited.val());
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

    select_bus = $('select[name="bus"]');
    select_place = $('select[name="place"]');
    select_route = $('select[name="route"]');
    select_client = $('select[name="client"]');
    input_birthdate = $('input[name="birthdate"]');
    select_payment_method = $('select[name="payment_method"]');
    input_card_number = $('input[name="card_number"]');
    input_card_amount_debited = $('input[name="card_amount_debited"]');
    input_cash = $('input[name="cash"]');
    input_change = $('input[name="change"]');
    input_card_titular = $('input[name="card_titular"]');
    input_year_card = $('input[name="card_year"]');
    inputs_vents = $('.rowVents');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    /* Tickets */

    $('body').on('click', 'button.ticket', function () {
        var item = {
            'seat': parseInt($(this).data('seat')),
            'route': sale.route
        };
        if (sale.addTicket(item)) {
            $(this).removeClass('bg-secondary').addClass('bg-gradient-danger');
        } else {
            $(this).removeClass('bg-gradient-danger').addClass('bg-secondary');
        }
        sale.calculateInvoice();
        input_cash.trigger('change');
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
            input_cash.trigger('change');
            //sale.listBusSeats();
            //sale.listTickets();
        });

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

    /* Client */

    select_client.select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_client'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
    })
        .on('select2:select', function (e) {
            fvSale.revalidateField('client');
        })
        .on('select2:clear', function (e) {
            fvSale.revalidateField('client');
        });

    $('.btnAddClient').on('click', function () {
        $('#myModalClient').modal('show');
    });

    $('input[name="names"]').on('keypress', function (e) {
        return validate_text_box({'event': e, 'type': 'letters'});
    });

    $('#myModalClient').on('hidden.bs.modal', function () {
        fvClient.resetForm(true);
    });

    $('input[name="dni"]').on('keypress', function (e) {
        return validate_text_box({'event': e, 'type': 'numbers'});
    });

    $('input[name="mobile"]').on('keypress', function (e) {
        return validate_text_box({'event': e, 'type': 'numbers'});
    });

    input_birthdate.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
    });

    input_birthdate.on('change.datetimepicker', function (e) {
        fvClient.revalidateField('birthdate');
    });

    select_payment_method.on('change', function () {
        var id = $(this).val();
        sale.setOptionsFields([{'index': 0, 'enable': false}, {'index': 1, 'enable': false}, {'index': 2, 'enable': false}]);
        input_cash.val(input_cash.val());
        input_card_amount_debited.val('0.00');
        switch (id) {
            case "efectivo":
                fvSale.enableValidator('change');
                fvSale.disableValidator('card_number');
                fvSale.disableValidator('card_titular');
                fvSale.disableValidator('card_amount_debited');
                fvSale.disableValidator('card_type');
                fvSale.disableValidator('card_year');
                fvSale.disableValidator('card_code_verification');
                input_cash.trigger("touchspin.updatesettings", {max: 100000000});
                sale.setOptionsFields([{'index': 0, 'enable': true}]);
                break;
            case "tarjeta_debito_credito":
                fvSale.disableValidator('change');
                fvSale.enableValidator('card_number');
                fvSale.enableValidator('card_titular');
                fvSale.enableValidator('card_amount_debited');
                fvSale.enableValidator('card_type');
                fvSale.enableValidator('card_year');
                fvSale.enableValidator('card_code_verification');
                input_card_amount_debited.val(sale.details.total);
                sale.setOptionsFields([{'index': 1, 'enable': true}, {'index': 2, 'enable': true}]);
                break;
            case "efectivo_tarjeta":
                input_change.val('0.00');
                fvSale.enableValidator('change');
                fvSale.enableValidator('card_number');
                fvSale.enableValidator('card_titular');
                fvSale.enableValidator('card_amount_debited');
                fvSale.enableValidator('card_type');
                fvSale.enableValidator('card_year');
                fvSale.enableValidator('card_code_verification');
                input_cash.trigger("touchspin.updatesettings", {max: sale.details.total});
                sale.setOptionsFields([{'index': 0, 'enable': true}, {'index': 1, 'enable': true}, {'index': 2, 'enable': true}]);
                break;
        }
    });

    input_cash
        .TouchSpin({
            min: 0.00,
            max: 100000000,
            step: 0.01,
            decimals: 2,
            boostat: 5,
            verticalbuttons: true,
            maxboostedstep: 10,
        })
        .on('change touchspin.on.min touchspin.on.max', function () {
            var paymentmethod = select_payment_method.val();
            fvSale.revalidateField('cash');
            var total = sale.details.total;
            switch (paymentmethod) {
                case "efectivo_tarjeta":
                    fvSale.revalidateField('card_amount_debited');
                    fvSale.revalidateField('change');
                    //input_change.val('0.00');
                    break;
                case "efectivo":
                    var cash = parseFloat($(this).val());
                    var change = cash - total;
                    input_change.val(change.toFixed(2));
                    fvSale.revalidateField('change');
                    break;
            }
        })
        .on('keypress', function (e) {
            return validate_text_box({'event': e, 'type': 'decimals'});
        });

    input_card_number.on('keypress', function (e) {
        fvSale.revalidateField('card_number');
        return validate_text_box({'event': e, 'type': 'numbers_spaceless'});
    }).on('keyup', function (e) {
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

    sale.setOptionsFields([{'index': 1, 'enable': false}, {'index': 2, 'enable': false}]);

    $('.btnRemoveTicketsAll').on('click', function () {
        if (sale.details.tickets.length === 0) return false;
        dialog_action({
            'success': function () {
                sale.details.tickets = [];
                sale.listTickets();
                sale.listBusSeats();
                sale.calculateInvoice();
                input_cash.trigger('change');
            },
            'cancel': function () {

            }
        });
    });

    $('i[data-field="client"]').hide();
    $('i[data-field="card_code_verification"]').hide();
});