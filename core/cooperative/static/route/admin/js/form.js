var fv;

document.addEventListener('DOMContentLoaded', function (e) {
    fv = FormValidation.formValidation(document.getElementById('frmForm'), {
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
                horary: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                chauffeur: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un chofer'
                        },
                    }
                },
                place: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un destino'
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
                price: {
                    validators: {
                        notEmpty: {},
                        numeric: {
                            message: 'El valor no es un número',
                            thousandsSeparator: '',
                            decimalSeparator: '.'
                        }
                    }
                },
                departure_time: {
                    validators: {
                        notEmpty: {
                            message: 'Debe seleccionar una hora'
                        },
                        regexp: {
                            regexp: /^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$/,
                            message: 'El formato de la hora no es el correcto'
                        },
                    }

                }
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
            const iconPlugin = fv.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(fv.form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
             var args = {
                'params': new FormData(fv.form),
                'form': fv.form
            };
            submit_with_formdata(args);
        });
});

$(function () {

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    $('select[name="bus"]').on('change', function () {
        fv.revalidateField('bus');
        var id = $(this).val();
        if (id === '') {
            return false;
        }

        $.ajax({
            url: pathname,
            data: {
                'action': 'search_bus_id',
                'id': id
            },
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            dataType: 'json',
            success: function (request) {
                if (!request.hasOwnProperty('error')) {
                    $('input[name="price"]').val(request.ticket_price);
                    return false;
                }
                message_error(request.error);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                message_error(errorThrown + ' ' + textStatus);
            }
        });

    });

    $('select[name="chauffeur"]').on('change', function () {
        fv.revalidateField('chauffeur');
    });

    $('select[name="place"]').on('change', function () {
        fv.revalidateField('place');
    });

    $('input[name="price"]')
        .TouchSpin({
            min: 0.01,
            max: 1000000,
            step: 0.01,
            decimals: 2,
            boostat: 5,
            verticalbuttons: true,
            maxboostedstep: 10,
            prefix: '$'
        })
        .on('change touchspin.on.min touchspin.on.max', function () {
            fv.revalidateField('price');
        })
        .on('keypress', function (e) {
            return validate_text_box({'event': e, 'type': 'decimals'});
        });

    $('input[name="departure_time"]').clockpicker({
        autoclose: true,
        default: 'now',
    }).change(function () {
        fv.revalidateField('departure_time');
    });
});