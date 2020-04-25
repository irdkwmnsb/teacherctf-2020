let socket = new WebSocket('ws://' + location.host.split(':')[0] + ":3001");
let type = 0

socket.onmessage = function (event) {
    data = JSON.parse(event.data);
    console.log(data);
    switch (data['action']) {
        case 'new_round':
            type = 'green-card'
            if (data['res'] == 'ничья')
                type = 'yellow-card'
            if (data['res'] == 'поражение')
                type = 'red-card'
            $('#history').append('<div class="card round-card ' + type + '">\
                    <h5 class="card-title">Раунд ' + data['round'] + '</h5>\
                    <div class="card-body">\
                        <p class="card-text">Ваш выбор: ' + data['user'] + '</p>\
                        <p class="card-text">Bыбор бота: ' + data['bot'] + '</p>\
                        <p class="card-text result-text">' + data['res'] + '</p>\
                    </div>\
                </div>');
            $("#history").scrollTop($("#history")[0].scrollHeight);
            break;

        case 'user_stats':
            console.log(data['user']);
            $('#user-wins').html(data['user']['wins']);
            $('#user-perc').html((data['user']['wins'] / data['user']['round'] * 100).toFixed(0));
            $('#user-score').html((data['user']['wins'] * data['user']['wins'] / data['user']['round']).toFixed(3));


            $('#bot-wins').html(data['user']['loses']);
            $('#bot-perc').html((data['user']['loses'] / data['user']['round'] * 100).toFixed(0));
            $('#bot-score').html((data['user']['loses'] * data['user']['loses'] / data['user']['round']).toFixed(3));

            break;

        case 'announcement':
            type = 'success';
            if (data['error'])
                type = 'danger'
            $('#info-col').append('<div class="alert alert-' + type + ' fade announcement" id="announcement"   role="alert">\
                    ' + data['data'] + '\
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">\
                        <span aria-hidden="true">&times;</span>\
                    </button>\
                </div>');
            $('#announcement').addClass('show');
            $(".announcement").fadeTo(2000, 500).slideUp(500, function () {
                $(this).slideUp(500);
                $(this).alert('close');
            });
            break;
    }
};

$('#btn-start').click(function () {
    if ($('#username')[0].value == '') {
        $('#name-input').css('border', 'solid 3px #f55');
    }
    else {
        $('#player-name').html($('#username')[0].value)
        $('.wrapper').css('display', 'none');
        $('.blurred').css('display', 'none');
        socket.send(JSON.stringify({ 'action': 'new_name', 'name': $('#username')[0].value }));

    }
});

$('#btn-flag').click(function () {
    socket.send(JSON.stringify({ 'action': 'get_flag' }));
});

$('.btn-game').click(function (el) {
    socket.send(JSON.stringify({ 'action': 'btn_click', 'btn': el.target.id }));
});