
const roomName = JSON.parse(document.getElementById('room-name').textContent);
var username = JSON.parse(document.getElementById('username').textContent);
var socketurl = 'ws://'+ window.location.host+ '/ws/chat/'+ roomName+ '/'
console.log(socketurl)
if (window.location.protocol == 'https:') {
    socketurl =  'wss://'+ window.location.host+ '/ws/chat/'+ roomName+ '/'
}

const chatSocket = new WebSocket(socketurl);

chatSocket.onopen = function(e){
    chatSocket.send(JSON.stringify({ 
        'command': 'fetch_messages',
        'chatID' : roomName
    }));
}
chatSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    console.log('message', data)
    if (data['messages']) {
        for (i = 0; i < data['messages'].length; i++) {
            var message = data['messages'][i].content;
            var author = data['messages'][i].author;
            add_to_chat(author, message)
            
        }   
    }
    else {
        var message = data['message'].content;
        var author = data['message'].author;
        add_to_chat(author, message)
        // document.querySelector('#chat-log').append(author + ': ' + message + '\n');
    }
    
    
    
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

function add_to_chat(author, message) {
    var msgDiv = document.createElement("div");
    if (author === username) {
        msgDiv.className = "msg-node-from";
    }
    else {
        msgDiv.className = "msg-node-to";
    }
    
    
    var textnode = document.createTextNode(author + ': ' + message);
    msgDiv.appendChild(textnode)
    document.getElementById("chat-log").appendChild(msgDiv);
    document.getElementById("chat-log").appendChild(emptyDiv = document.createElement("br") );
}
document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  
        document.querySelector('#chat-message-submit').click();
    }
};


function chat_send() {
    console.log("here")
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        'command': 'new_message',
        'from': username,
        'chatID': roomName,
    }));
    messageInputDom.value = '';
}