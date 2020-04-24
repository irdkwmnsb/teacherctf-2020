let express = require('express');
let app = express();
let WebSocketServer = new require('ws');
let seedrandom = require('seedrandom');
let events = require('./events.json');


app.use(express.static('public'));

app.get('/', function (req, res) {
    res.sendFile(__dirname + '/public/index.html');
});

app.listen(3000, function () {
    console.log('Listening on port 3000');
});

class User {
    constructor(name) {
        this.rnd = seedrandom(name);
        this.wins = 0;
        this.loses = 0;
        this.round = 0;
    }

    auto_choice() {
        return Math.floor(this.rnd() * 3);
    }
}

let clients = {};
let users = {};

let webSocketServer = new WebSocketServer.Server({
    port: 3001
});

webSocketServer.on('connection', function (ws) {
    let id = Math.random();
    clients[id] = ws;
    users[id] = 0;

    console.log('[+] Connected: ' + id);
    clients[id].send(JSON.stringify({ 'action': 'announcement', 'error': false, 'data': events['connected'] }));


    ws.on('message', function (message) {
        console.log('[?] Recieved: ' + message);
        data = JSON.parse(message)

        switch (data['action']) {
            case 'new_name':
                users[id] = new User(data['name']);
                break;

            case 'btn_click':
                bot = users[id].auto_choice();
                users[id].round++;
                switch (data['btn']) {
                    case 'rock':

                        if (bot == 0) {
                            clients[id].send(JSON.stringify({ 'action': 'new_round', 'round': users[id].round, 'user': 'камень', 'bot': 'камень', 'res': 'ничья' }));
                        }
                        if (bot == 1) {
                            clients[id].send(JSON.stringify({ 'action': 'new_round', 'round': users[id].round, 'user': 'камень', 'bot': 'ножницы', 'res': 'победа' }));
                            users[id].wins++;
                        }
                        if (bot == 2) {
                            clients[id].send(JSON.stringify({ 'action': 'new_round', 'round': users[id].round, 'user': 'камень', 'bot': 'бумага', 'res': 'поражение' }));
                            users[id].loses++;
                        }
                        break;

                    case 'scissors':

                        if (bot == 0) {
                            clients[id].send(JSON.stringify({ 'action': 'new_round', 'round': users[id].round, 'user': 'ножницы', 'bot': 'камень', 'res': 'поражение' }));
                            users[id].loses++;
                        }
                        if (bot == 1) {
                            clients[id].send(JSON.stringify({ 'action': 'new_round', 'round': users[id].round, 'user': 'ножницы', 'bot': 'ножницы', 'res': 'ничья' }));
                        }
                        if (bot == 2) {
                            clients[id].send(JSON.stringify({ 'action': 'new_round', 'round': users[id].round, 'user': 'ножницы', 'bot': 'бумага', 'res': 'победа' }));
                            users[id].wins++;
                        }
                        break;

                    case 'paper':

                        if (bot == 0) {
                            clients[id].send(JSON.stringify({ 'action': 'new_round', 'round': users[id].round, 'user': 'бумага', 'bot': 'камень', 'res': 'победа' }));
                            users[id].wins++;
                        }
                        if (bot == 1) {
                            clients[id].send(JSON.stringify({ 'action': 'new_round', 'round': users[id].round, 'user': 'бумага', 'bot': 'ножницы', 'res': 'поражение' }));
                            users[id].loses++;
                        }
                        if (bot == 2) {
                            clients[id].send(JSON.stringify({ 'action': 'new_round', 'round': users[id].round, 'user': 'бумага', 'bot': 'бумага', 'res': 'ничья' }));
                        }

                        break;
                }
                clients[id].send(JSON.stringify({ 'action': 'user_stats', 'user': users[id] }))
                break;

            case 'get_flag':
                if (users[id].round == 0 | users[id].wins * users[id].wins / users[id].round < 10)
                    clients[id].send(JSON.stringify({ 'action': 'announcement', 'error': true, 'data': events['points_error'] }));
                else if (users[id].wins < users[id].round)
                    clients[id].send(JSON.stringify({ 'action': 'announcement', 'error': true, 'data': events['percent_error'] }));
                else
                    clients[id].send(JSON.stringify({ 'action': 'announcement', 'error': false, 'data': events['flag'] }));
                break;
        }
    });

    ws.on('close', function () {
        console.log('[-] Closed: ' + id);
        delete clients[id];
    });
});