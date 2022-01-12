const username = JSON.parse(document.getElementById("username").textContent);

const websocketUrl = `ws://${location.host}/ws/user/notification/${username}/`;

// websocket connect
const notificationWebSocket = new WebSocket(websocketUrl);

notificationWebSocket.onopen = (e) => {
  console.log("Notification Websocket Connected!");
};

notificationWebSocket.onclose = (e) => {
  console.error("Notification Websocket Disconnected!");
};

notificationWebSocket.onerror = (e) => {
  console.error("Notification Error: " + e.data);
};

notificationWebSocket.onmessage = async (e) => {
  const data = JSON.parse(e.data);
  console.log(data);
  Toastify({
    text: `Admin: ${data["body"]}`,
    duration: 3000,
  }).showToast();

  // play notification
  const audio = new Audio("/static/sounds/notification.mp3");
  await audio.play();
};

const notificationInput = document.getElementById("notificationInput");

if (notificationInput) {
  document
    .getElementById("notificationSendBtn")
    .addEventListener("click", () => {
      // send notification functionality
      notificationWebSocket.send(
        JSON.stringify({
          body: notificationInput.value,
          self: true,
        })
      );
      document.getElementById("notificationInput").value = "";
    });
}
