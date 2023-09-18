var fv;
var input_year;

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
                name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                plaque: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    parameter: fv.form.querySelector('[name="plaque"]').value,
                                    pattern: 'plaque',
                                    action: 'validate_data'
                                };
                            },
                            message: 'El numero de placa ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                car_disk: {
                    validators: {
                        notEmpty: {},
                        digits: {},
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    parameter: fv.form.querySelector('[name="car_disk"]').value,
                                    pattern: 'car_disk',
                                    action: 'validate_data'
                                };
                            },
                            message: 'El numero de disco ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                category: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una categoría'
                        },
                    }
                },
                exemplar: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una modelo/marca'
                        },
                    }
                },
                member: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un socio'
                        },
                    }
                },
                year: {
                    validators: {
                        notEmpty: {},
                        digits: {}
                    }
                },
                car_seats: {
                    validators: {
                        notEmpty: {},
                        digits: {}
                    }
                },
                ticket_price: {
                    validators: {
                        notEmpty: {},
                        numeric: {
                            message: 'El valor no es un número',
                            thousandsSeparator: '',
                            decimalSeparator: '.'
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

    input_year = $('input[name="year"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    $('select[name="category"]').on('change.select2', function () {
        fv.revalidateField('category');
    });

    $('select[name="exemplar"]').on('change.select2', function () {
        fv.revalidateField('exemplar');
    });

    $('select[name="member"]').on('change.select2', function () {
        fv.revalidateField('member');
    });

    $('input[name="car_seats"]')
        .TouchSpin({
            min: 0,
            max: 100,
            stepinterval: 1,
            maxboostedstep: 100,
            verticalbuttons: true,
        })
        .on('change touchspin.on.min touchspin.on.max', function () {
            fv.revalidateField('car_seats');
        })
        .on('keypress', function (e) {
            return validate_text_box({'event': e, 'type': 'numbers'});
        });

    $('input[name="car_disk"]')
        .TouchSpin({
            min: 0,
            max: 100,
            stepinterval: 1,
            maxboostedstep: 100,
            verticalbuttons: true,
        })
        .on('change touchspin.on.min touchspin.on.max', function () {
            fv.revalidateField('car_disk');
        })
        .on('keypress', function (e) {
            return validate_text_box({'event': e, 'type': 'numbers'});
        });

    input_year.datetimepicker({
        locale: 'es',
        keepOpen: true,
        viewMode: 'years',
        format: 'YYYY',
    });

    input_year.on('keypress', function (e) {
        return validate_text_box({'event': e, 'type': 'numbers'});
    });

    input_year.on('change.datetimepicker', function (e) {
        fv.revalidateField('year');
    });

    $('input[name="plaque"]')
        .on('keyup', function (e) {
            var obj = $(this).val();
            return $(this).val(obj.toUpperCase());
        });

    $('input[name="ticket_price"]')
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
            fv.revalidateField('ticket_price');
        })
        .on('keypress', function (e) {
            return validate_text_box({'event': e, 'type': 'decimals'});
        });
});