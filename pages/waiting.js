import { getKey } from "./home.js";

export default function waiting(){
    const frame = document.querySelector(".frame");
    frame.innerHTML = '';
    const fragment = document.createElement("div");
    fragment.className = "waiting";
    const joinText = document.createElement("p");
    joinText.textContent = `Your session token is: ${getKey()}`;
    const waitText = document.createElement("p");
    waitText.textContent = "Waiting for black player to join...";
    fragment.appendChild(joinText);
    fragment.appendChild(waitText);
    frame.appendChild(fragment);
}