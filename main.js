import { updateBoard, updateOptions, clearOptions } from "./chess.js";
import { loadContent } from "./routing.js";

var websocket;
function getWebsocket(){
  return websocket;  
}

function prepare(websocket) {
  websocket.addEventListener("message", ({ data }) => {
    const event = JSON.parse(data);
    switch (event.event) {
      case "ready":
        loadContent('game');
        let event = {event: "ready"};
        websocket.send(JSON.stringify(event));
        break;
      default:
        // throw new Error(`Unsupported event type: ${event.type}.`);
    }
  });
}

window.addEventListener("DOMContentLoaded", () => {
  // Initialize the UI.
  const frame = document.querySelector(".frame");
  // Open the WebSocket connection and register event handlers.
  console.log('Opening connection...')
  websocket = new WebSocket("ws://localhost:8001/");
  websocket.addEventListener('close', () => console.log('Closing connection...'));
  prepare(websocket);
  loadContent('home');
});

export { getWebsocket }