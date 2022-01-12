const clientUsername = JSON.parse(
  document.getElementById("client_username").textContent
);

const ChatWebsocketUrl = `ws://${location.host}/ws/chat/${clientUsername}/`;

const chatWebSocket = new WebSocket(ChatWebsocketUrl);

const ownMessageHTML = (message) => {
  return `<div class="my-1 d-flex justify-content-end">
    <button class="btn btn-sm btn-success">${message}</button>
</div>`;
};

const opponentMessageHTML = (message) => {
  // play message audio
  const audio = new Audio("/static/sounds/chat.mp3");
  audio.play();
  return `<div class="my-1 d-flex justify-content-start">
    <button class="btn btn-sm btn-primary">${message}</button>
</div>`;
};

const displayMessage = (message) => {
  let html;
  if (message.sender == username) {
    html = ownMessageHTML(message.body);
  } else {
    html = opponentMessageHTML(message.body);
  }
  return html;
};

const displayMessages = (messages) => {
  let html = "";
  messages.forEach((msg) => {
    html += displayMessage(msg);
  });
  return html;
};

chatWebSocket.onopen = (e) => {
  console.log("Chat Websocket connected!");
  // fetch all messages
  chatWebSocket.send(
    JSON.stringify({
      type: "fetch_messages",
    })
  );
};

chatWebSocket.onclose = (e) => {
  console.error("Chat Websocket disconnected!");
};

chatWebSocket.onerror = (e) => {
  console.error("Chat Websocket Error:" + e.data);
};

chatWebSocket.onmessage = (e) => {
  let data = JSON.parse(e.data);
  if (data.type === "send_message") {
    let html = displayMessage(data);
    // show the html
    document.getElementById("chatStore").innerHTML += html;
  } else if (data.type === "fetch_messages") {
    let html = displayMessages(data.data);
    document.getElementById("chatStore").innerHTML = html;
  }
};

// send chat message
document.getElementById("sendMsgForm").addEventListener("submit", (e) => {
  e.preventDefault();
  let body = document.getElementById("msgBody").value;
  chatWebSocket.send(
    JSON.stringify({
      type: "send_message",
      body,
      sender: username,
    })
  );
});

document.getElementById("msgBody").focus();
