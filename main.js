import { updateBoard, updateOptions } from "./chess.js";

window.addEventListener("DOMContentLoaded", () => {
  // Initialize the UI.
  const board = document.getElementsByClassName("board")[0];
  const options = document.getElementsByClassName("options")[0];
  // Open the WebSocket connection and register event handlers.
  const websocket = new WebSocket("ws://localhost:8001/");
  receiveMoves(board, options, websocket);
});

function showMessage(message) {
  window.setTimeout(() => window.alert(message), 50);
}

function receiveMoves(board, options, websocket) {
  websocket.addEventListener("message", ({ data }) => {
    const event = JSON.parse(data);
    switch (event.type) {
      case "play":
        // Update the UI with the move.
        updateBoard(board, event.svg_board)
        updateOptions(options, websocket, event.move_list);
        break;
      case "game_over":
        updateBoard(board, event.svg_board)
        updateOptions(options, websocket, []);
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