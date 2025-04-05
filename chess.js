function sendMoves(move_uci, websocket) {
  // When clicking a button, send a "play" event for that move.
  const event = {
    type: "play",
    move_uci: move_uci,
  };
  websocket.send(JSON.stringify(event));
}

function updateBoard(board, svg_board) {
  board.textContent = ''; 
  board.insertAdjacentHTML("afterbegin", svg_board)
}

function updateOptions(options, websocket, moves_list) {
  options.textContent = '';
  moves_list.forEach(move => {
    const button = document.createElement("button");
    button.onclick = () => {sendMoves(move, websocket);};
    button.textContent = move;
    options.appendChild(button);
  });
}

export { updateBoard, updateOptions };