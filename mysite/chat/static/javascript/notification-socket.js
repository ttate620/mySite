

var socketurl = 'ws://'+ window.location.host+ '/ws/chat/'
if (window.location.protocol == 'https:') {
    socketurl =  'wss://'+ window.location.host+ '/ws/chat/'
}

const chatSocket = new WebSocket(socketurl);

chatSocket.onopen = function(e){
    console.log('open')
}
chatSocket.onmessage = function(e) {
    var data = JSON.parse(e.data)
    var message = data['message']
    
    var chat_rooms = document.getElementById('notification-bar')
    var new_chat_li = document.createElement("li");
    var new_chat_a = document.createElement("a");
    new_chat_a.setAttribute("href", "/chat/"+ message + "/")  
    var node = document.createTextNode('new chat' + message);
    new_chat_a.appendChild(node);
    new_chat_li.append(new_chat_a)
    chat_rooms.appendChild(new_chat_li);

    var icon = document.getElementById("notifications-icon") 
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};