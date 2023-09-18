module.exports = (io) => {
    const app = io.of('/');
    app.on('connection', (socket) => {
        console.log('user:' + socket.id + ' status:conectado ');

        socket.on('message', (msg) => {
            console.log(msg);
            app.emit('messages', msg);
        });

        socket.on('disconnect', () => {
            console.log('user:' + socket.id + ' status:disconnect ');
        });
    });

}
