const roomName = JSON.parse(document.getElementById('room-name').textContent);
const username = JSON.parse(document.getElementById('username').textContent);

const chatSocket = new ReconnectingWebSocket(
    'ws://'
    + window.location.host
    + '/ws/messenger/'
    + roomName
    + '/'
);

function fetchMessages() {
    chatSocket.send(JSON.stringify({'command': 'fetch_messages'}));
}

chatSocket.onopen = function (e) {
    fetchMessages();
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
};

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};
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
    chatSocket.send(JSON.stringify({
        'command': 'new_message',
        'message': message,
        'from': username
    }));
    messageInputDom.value = '';
    $('.contact.active .preview').html('<span>You: </span>' + message);
    $(".messages").animate({scrollTop: $(document).height()}, "fast");
};

function fetchMessages() {
    chatSocket.send(JSON.stringify({'command': 'fetch_messages'}));
}

function createMessage(data) {
    var author = data['author'];
    var msgListTag = document.createElement('li');
    var imgTag = document.createElement('img');
    var pTag = document.createElement('p');
    pTag.textContent = data.content;
    imgTag.src = 'http://emilcarlsson.se/assets/mikeross.png';

    if (author === username) {
        msgListTag.className = 'replies';
    } else {
        msgListTag.className = 'sent';
    }
    msgListTag.appendChild(imgTag);
    msgListTag.appendChild(pTag);
    document.querySelector('#chat-log').appendChild(msgListTag);


}
