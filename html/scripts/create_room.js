import { addHandler, sendMsg } from "./main.js";
import { CreateRoomMsg } from "./messages/messages.js";

const selectors = {
    roomNameInput: "room-name",
    authorNameInput: "author-name",
    createRoomBtn: "create-room-btn",
    createRoomMsg: "create-room-message",
    roomPasswordInput: "room-password",
    roomPasswordEnabled: "room-password-enabled",
    roomPasswordLabel: "room-password-label"
}

function getElements(selectors, func) {
    const elements = {};
    
    for (let [k,v] of Object.entries(selectors)) {
        elements[k] = func(v);
    }
    
    return elements;
}


const elements = getElements(selectors, id => document.getElementById(id));


function getInputValue(input) {
    const value = input.value.trim();

    if (!value) {
        throw new Error("Campo vazio");
    }

    return value;
}


elements.roomPasswordEnabled.addEventListener("change", () => {
    if (!elements.roomPasswordEnabled.checked) {
        elements.roomPasswordLabel.classList.add("hidden");
        elements.roomPasswordInput.classList.add("hidden");
    } else {
        elements.roomPasswordLabel.classList.remove("hidden");
        elements.roomPasswordInput.classList.remove("hidden");
    }
});


elements.createRoomBtn.addEventListener("click", () => {
    try {
        const roomName = getInputValue(elements.roomNameInput);
        const authorName = getInputValue(elements.authorNameInput);
        // const password = getInputValue(passwordInput);

        sendMsg(new CreateRoomMsg(roomName, authorName));
        console.log("there");
    } catch (err) {
        elements.createRoomMsg.hidden = false;
        elements.createRoomMsg.textContent = err.message;
        elements.createRoomMsg.classList.add("failure");
        elements.createRoomMsg.classList.remove("success");
    }
});


addHandler("create_room", (data) => {
    console.log("here");
    elements.createRoomMsg.hidden = false;

    if (data.state) {
        elements.createRoomMsg.textContent = "Room created successfully";
        elements.createRoomMsg.classList.add("success");
        elements.createRoomMsg.classList.remove("failure");
    } else {
        elements.createRoomMsg.textContent = "Something went wrong";
        elements.createRoomMsg.classList.add("failure");
        elements.createRoomMsg.classList.remove("success");
    }
});


addHandler("room_connection", (data) => {
    console.log("Room connected:", data.room_name);
});