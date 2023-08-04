// websocket.js
const socket = new WebSocket('ws://your-server-address/ws/chat/');

socket.onopen = () => {
    console.log('WebSocket connection opened.');
};

socket.onclose = () => {
    console.log('WebSocket connection closed.');
};

socket.onmessage = (event) => {
    const message = JSON.parse(event.data);
    // Обработка полученного сообщения, например, добавление его в список сообщений на странице
    const messageList = document.getElementById('message-list');
    const li = document.createElement('li');
    li.innerText = `${message.sender}: ${message.text}`;
    messageList.appendChild(li);
};

// Функция для отправки сообщения на сервер через WebSocket
function sendMessage(text) {
    const messageData = {
        sender: 'Me', // Здесь можно указать имя пользователя, отправляющего сообщение
        text: text,
    };
    socket.send(JSON.stringify(messageData));
}
