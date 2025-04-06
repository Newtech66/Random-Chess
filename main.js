import { updateBoard, updateOptions, clearOptions } from "./chess.js";
import { loadContent } from "./routing.js";

var websocket;
function getWebsocket(){
  return websocket;  
}

function initGame(websocket) {
  websocket.addEventListener("open", () => {
    // Send an "init" event according to who is connecting.
    const params = new URLSearchParams(window.location.search);
    let event = { type: "init" };
    if (params.has("join")) {
      // Second player joins an existing game.
      event.type = "join";
      event.key = params.get("join");
    } else {
      // First player starts a new game.
      event.type = "host";
    }
    websocket.send(JSON.stringify(event));
  });
}

function receiveMoves(board, options, websocket) {
  websocket.addEventListener("message", ({ data }) => {
    const event = JSON.parse(data);
    switch (event.type) {
      case "play":
        // Update the UI with the move.
        updateBoard(board, event.svg_board);
        updateOptions(options, websocket, event.move_list);
        break;
      case "hold":
        // Wait for other player to make a move.
        updateBoard(board, event.svg_board);
        clearOptions(options, "Waiting for other player to move.")
      case "game_over":
        updateBoard(board, event.svg_board);
        clearOptions(options, "");
        if (event.player == "Draw"){
          showMessage(`The game was drawn!`);
        }else{
          showMessage(`Player ${event.player} wins by ${event.termination}!`);
        }
        // No further messages are expected; close the WebSocket connection.
        websocket.close(1000);
        break;
      default:
        throw new Error(`Unsupported event type: ${event.type}.`);
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
  loadContent('home');
});

function showMessage(message) {
  window.setTimeout(() => window.alert(message), 50);
}

export { getWebsocket }