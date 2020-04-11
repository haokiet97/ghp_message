$(function () {
    let sk_protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    var userSocket = new ReconnectingWebSocket(
        sk_protocol + '//'
        + window.location.host
        + '/ws/messenger/users/'
    );
    userSocket.onopen = function (e) {
        fetchUsers(userSocket);
    }

    userSocket.onmessage = function (e) {
        var data = JSON.parse(e.data);
        console.log(data);

        if (data['command'] === 'new_user_online') {
            SetUserOnline(data.user);
        } else if (data['command'] === 'new_user_offline') {
            SetUserOffline(data.user);
        } else if (data['command'] === 'fetch_users') {
            for (let i = 0; i < data['users'].length; i++) {
                let user = data['users'][i];
                if (user.online === "True") {
                    SetUserOnline(user);
                } else {
                    SetUserOffline(user);
                }
            }

        }
    }

    function SetUserOffline(user) {
        let user_id = user.id
        let contact_status = $('.chat_user#' + user_id).parent().find("span.contact-status").get(0);
        if ($(contact_status).hasClass('online')) {
            $(contact_status).removeClass('online')
        }
        $(contact_status).addClass('offline')
    }

    function SetUserOnline(user) {
        let user_id = user.id
        let contact_status = $('.chat_user#' + user_id).parent().find("span.contact-status").get(0);
        if ($(contact_status).hasClass('offline')) {
            $(contact_status).removeClass('offline')
        }
        $(contact_status).addClass('online')
    }

    userSocket.onerror = function (e) {
        console.log("errors:", e);
    }

    function fetchUsers(userSocket) {
        userSocket.send(JSON.stringify({'command': 'fetch_users'}));
    }

    function new_user_online(userSocket) {
        userSocket.send(JSON.stringify({'command': 'new_user_online'}));
    }

});
