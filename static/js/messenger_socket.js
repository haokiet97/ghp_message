// const roomid = JSON.parse(document.getElementById('room-id').textContent);
var sket_protocol;
if(window.location.protocol === 'http:' ){
    sket_protocol = 'ws:';
}else {
    sket_protocol = 'wss:';
}

const username = JSON.parse(document.getElementById('username').textContent);

//get list of contacts or chatrooms
var contacts = $('#contacts');
var list_contacts = contacts.find('li.contact');
var first_contact = list_contacts.get(0);
$(first_contact).addClass('active');
let room_id = first_contact.getAttribute('id');
var dict_chatsocket = new Map();

$(list_contacts).each(function (index, item) {
    let room_id = $(item).attr('id');
    let chatSocket = new ReconnectingWebSocket(
        sket_protocol
        +'//'
        + window.location.host
        + '/ws/messenger/rooms/'
        + room_id
        + '/'
    );
    chatSocket.onopen = function (e) {
        checkConnect(current_connect)
    };
    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        if (data['command'] === 'messages') {
            for (let i = 0; i < data['messages'].length; i++) {
                createMessage(data['messages'][i]);
            }
        } else if (data['command'] === 'new_message') {
            createMessage(data['message']);
        }
        current_connect.onclose = function (e) {
            console.error('Chat socket closed unexpectedly');
        };
    };

    dict_chatsocket.set(room_id, chatSocket);
});

var current_connect = dict_chatsocket.get(room_id);
current_connect.onopen = function (e) {
    fetchMessages(current_connect)
};

current_connect.onmessage = function (e) {
    const data = JSON.parse(e.data);
    if (data['command'] === 'messages') {
        for (let i = 0; i < data['messages'].length; i++) {
            createMessage(data['messages'][i]);
        }
    } else if (data['command'] === 'new_message') {
        createMessage(data['message']);
    }
    current_connect.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };
};

$('li.contact').on('click', function () {
    if ($(this).hasClass('active')) {
        return
    }
    $(list_contacts).removeClass('active');
    $(this).addClass('active');
    let room_id = $(this).attr('id');
    //clear messages
    $('.content .messages #chat-log').html('');
    if (dict_chatsocket.get(room_id) == null) {
        let chatSocket = new ReconnectingWebSocket(
            sket_protocol
            + '//'
            + window.location.host
            + '/ws/messenger/rooms/'
            + room_id
            + '/'
        );
        dict_chatsocket.set(room_id, chatSocket);
        current_connect = chatSocket;
    } else {
        let old_connect = dict_chatsocket.get(room_id);
        old_connect.close();
        let chatSocket = new ReconnectingWebSocket(
            'ws://'
            + window.location.host
            + '/ws/messenger/rooms/'
            + room_id
            + '/'
        );
        dict_chatsocket.set(room_id, chatSocket);
        current_connect = chatSocket;
    }

    current_connect = dict_chatsocket.get(room_id);

    current_connect.onopen = function (e) {
        fetchMessages(current_connect);
    };

    current_connect.onmessage = function (e) {
        const data = JSON.parse(e.data);
        if (data['command'] === 'messages') {
            for (let i = 0; i < data['messages'].length; i++) {
                createMessage(data['messages'][i]);
            }
        } else if (data['command'] === 'new_message') {
            createMessage(data['message']);
        }
    };

    current_connect.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };
});

document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        message = document.getElementById('chat-message-input').value;
        if ($.trim(message) == '') {
            return false;
        }
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    var messageInputDom = document.getElementById('chat-message-input');
    var message = messageInputDom.value;
    if ($.trim(message) == '') {
        return false;
    }
    current_connect.send(JSON.stringify({
        'command': 'new_message',
        'message': message,
    }));
    messageInputDom.value = '';
    $('.contact.active .preview').html('<span>You: </span>' + message);
    $(".messages").animate({ScrollTop: $(document).height()}, "fast");
};

function fetchMessages(chatSocket) {
    chatSocket.send(JSON.stringify({'command': 'fetch_messages'}));
}

function checkConnect(chatSocket) {
    chatSocket.send(JSON.stringify({'command': 'check_connect'}));
}

function createMessage(data) {
    var author = data['author'];
    var room_id = data['room_id'];
    var msgListTag = document.createElement('li');
    var imgTag = document.createElement('img');
    var new_ms_tag = document.createElement('span');
    new_ms_tag.className = 'new-message';
    var pTag = document.createElement('p');
    pTag.textContent = data.content;
    imgTag.src = 'http://emilcarlsson.se/assets/mikeross.png';
    imgTag.title = author;

    if (author === username) {
        msgListTag.className = 'replies';
        $('.contact#' + room_id + ' .preview').html('<span>You: </span>' + data.content);
    } else {
        msgListTag.className = 'sent';
        $('.contact#' + room_id + ' .preview').html('<span>' + author + ': </span>' + data.content);
    }
    msgListTag.appendChild(imgTag);
    msgListTag.appendChild(pTag);

    var contact_tag = $('#contacts li.contact#' + room_id).get(0);
    var list_contacts_tag = $('#contacts ul').get(0);

    if ($('#contacts li.contact#' + room_id).hasClass('active')) {
        document.querySelector('#chat-log').appendChild(msgListTag);
    }else{
        if (author === username) {
            msgListTag.className = 'replies';
            $('.contact#' + room_id + ' .preview').html('<span>You: </span>' + '<b>' + data.content + '</b>');
        } else {
            msgListTag.className = 'sent';
            $('.contact#' + room_id + ' .preview').html('<span>' + author + ': </span>' + '<b>' + data.content + '</b>');
        }
        contact_tag.remove();
        list_contacts_tag.prepend(contact_tag);
    }
}
