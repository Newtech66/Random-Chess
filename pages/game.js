import { getWebsocket } from "../main.js";

function showMessage(message) {
    window.setTimeout(() => window.alert(message), 50);
}

function updateBoard(board, svg_board){
    board.innerHTML = svg_board;
}

function sendMoves(move, socket) {
    let event = {
        event: "turn",
        move: move,
    };
    socket.send(JSON.stringify(event));
}

function updateOptions(options, socket, moves_list) {
    options.textContent = '';
    moves_list.forEach(move => {
      const button = document.createElement("button");
      button.onclick = () => {sendMoves(move, socket);};
      button.textContent = move;
      options.appendChild(button);
    });
}

function clearOptions(options, message) {
    options.textContent = message;
}

function gameEventListeners(board, options) {
    let socket = getWebsocket();
    socket.addEventListener("message", ({ data }) => {
        const event = JSON.parse(data);
        switch (event.event) {
            case "turn":
                // Update the UI with the move.
                updateBoard(board, event.svg_board);
                updateOptions(options, socket, event.move_list);
                break;
            case "wait":
                // Wait for other player to make a move.
                updateBoard(board, event.svg_board);
                clearOptions(options, "Waiting for other player to move.")
                break;
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
                // throw new Error(`Unsupported event type: ${event.type}.`);
        }
      });
}

export default function game(){
    const frame = document.querySelector(".frame");
    frame.innerHTML = '';
    const boardFrame = document.createElement("div");
    boardFrame.className = "board";
    const optionsFrame = document.createElement("div");
    optionsFrame.className = "options";
    frame.appendChild(boardFrame);
    frame.appendChild(optionsFrame);
    gameEventListeners(boardFrame, optionsFrame);
}