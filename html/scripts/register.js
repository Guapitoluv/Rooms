import { addHandler, sendMsg } from "./main.js";
//import { RegisterUserMsg } from "./messages.js";

const registerBtn = document.getElementById("register-btn");
const userNameInput = document.getElementById("user-name");
const registerMsg = document.getElementById("register-message");

registerBtn.addEventListener("click", () => {
    const un = userNameInput.value;
    
    if (!un) {
        registerMsg.hidden = false;
        registerMsg.classList.remove("success");
        registerMsg.classList.add("failure");
        registerMsg.textContent = "Empty user name: Invalid";
        return;
    }
    
    localStorage.setItem("userName", un);
    registerMsg.hidden = false;
    registerMsg.classList.add("success");
    registerMsg.classList.remove("failure");
    registerMsg.textContent = un;
});