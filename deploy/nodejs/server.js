const express = require('express');
const app = express();
var cors = require('cors');
app.options('*', cors());
const http = require('http').createServer(app);
const io = require('socket.io')(http);

const nameSpace = require('./name_space/listen');
nameSpace(io);

app.get('/', function (req, res) {
    res.status(200).send({status: true});
});

http.listen(9072, function () {
    console.log('Servidor ON puerto: ', 9072);
});