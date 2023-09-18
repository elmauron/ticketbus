socket = io.connect(socket_url, {
    forceNew: true,
    transports: ['websocket']
});

socket.on('connect', function () {
    console.log('Estado de conexión del socket:' + socket.connected);
});

socket.on('disconnect', function (reason) {
    if (reason === "io server disconnect") {
        socket.connect();
    }
});

socket.on('connect_error', function () {
    console.log('Ha ocurrido un error, se estata tratando de volver a conectar el socket');
    socket.connect();
});

socket.on('messages', function (response) {
    console.log(response);
    if (response.hasOwnProperty('tickets') && !$.isEmptyObject(sale.route)) {
        response.tickets.forEach(function (value, index, array) {
            var position = sale.searchSeat(value);
            var button;
            if (position > -1) {
                button = $('body').find('button.ticket[data-route="' + value.route.id + '"][data-seat="' + value.seat + '"]');
                button.removeClass().addClass('btn btn-app bg-gradient-danger').prop('disabled', true);
                button.append('<span class="badge bg-success">Ocupado</span>');
                sale.details.tickets.splice(position, 1);
                tblTickets.row(position).remove().draw();
            } else {
                if (parseInt(sale.route.id) === value.route.id) {
                    button = $('body').find('button.ticket[data-route="' + value.route.id + '"][data-seat="' + value.seat + '"]');
                    button.removeClass().addClass('btn btn-app bg-gradient-danger').prop('disabled', true);
                    button.append('<span class="badge bg-success">Ocupado</span>');
                }
            }
        });
        sale.calculateInvoice();
        if ($('input[name="cash"]').length) {
            input_cash.trigger('change');
        }
    }
});