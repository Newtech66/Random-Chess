import { getWebsocket } from "../main.js";
import { loadContent } from "../routing.js";

function sendJoinKey(key){
    let socket = getWebsocket();
    let event = {
        event: "join",
        key: key,
    }
    socket.send(JSON.stringify(event));
}

export default function join() {
    const frame = document.querySelector(".frame");
    frame.innerHTML = '';
    const fragment = document.createElement("div");
    fragment.className = "join form";
    const joinText = document.createElement("p");
    joinText.textContent = "Enter join key:";
    const inputField = document.createElement("input");
    inputField.type = "text";
    inputField.required = true;
    inputField.placeholder = "Join key";
    const joinButton = document.createElement("button");
    joinButton.className = "action join";
    joinButton.textContent = "Join";
    joinButton.onclick = () => sendJoinKey(inputField.value);
    const backButton = document.createElement("button");
    backButton.className = "action home";
    backButton.textContent = "Back";
    backButton.onclick = () => loadContent('home');
    fragment.appendChild(joinText);
    fragment.appendChild(inputField);
    fragment.appendChild(joinButton);
    fragment.appendChild(backButton);
    frame.appendChild(fragment);
}