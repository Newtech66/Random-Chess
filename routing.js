import home from "./pages/home.js";
import waiting from "./pages/waiting.js";
import game from "./pages/game.js";
import join from "./pages/join.js";

function loadContent(page){
    switch (page){
        case "home":
            home();
            break;
        case "waiting":
            waiting();
            break;
        case "join":
            join();
            break;
        case "game":
            game();
            break;
        default:
            console.log("Page does not exist!");
    }
}

export { loadContent };