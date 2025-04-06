import { getWebsocket } from "../main.js";
import { loadContent } from "../routing.js";

var key;
function getKey(){
    return key;  
}

function hostGame() {
    let socket = getWebsocket();
    let event = {
        event: "init",
        type: "host",
    };
    socket.send(JSON.stringify(event));
    socket.addEventListener("message", ({ data }) => {
        const event = JSON.parse(data);
        switch (event.type) {
        case "host":
            // Create link for inviting the second player.
            key = event.key;
            loadContent('waiting');
            break;
        default:
            throw new Error(`Unsupported event type: ${event.type}.`);
        }
    });
}

function joinGame() {
    loadContent('join');
}

export default function home(){
    const frame = document.querySelector(".frame");
    frame.innerHTML = '';
    const fragment = document.createElement("div");
    fragment.className = "actions";
    const hostButton = document.createElement("button");
    hostButton.className = "action new";
    hostButton.textContent = "New";
    hostButton.onclick = hostGame;
    const joinButton = document.createElement("button");
    joinButton.className = "action join";
    joinButton.textContent = "Join";
    joinButton.onclick = joinGame;
    fragment.appendChild(hostButton);
    fragment.appendChild(joinButton);
    frame.appendChild(fragment);
}

export { getKey };