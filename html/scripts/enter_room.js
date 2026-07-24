import { socketReady, addHandler, sendMsg } from "./main.js";
import { RequestRoomsListMsg, EnterRoomMsg } from "./messages/messages.js";


const roomNameInput = document.getElementById("room-name");
const enterRoomBtn = document.getElementById("enter-room");
const roomsDOM = document.getElementById("rooms");
const roomsTable = roomsDOM.querySelector(".painel-table");
let rooms = [];

socketReady.then(() => sendMsg(new RequestRoomsListMsg()));

addHandler("rooms_list", (data) => {
    rooms = data.rooms;
    
    const alreadyRooms = (() => {
        const rooms = [];
        const tableRooms = roomsTable.querySelectorAll(".painel-item");
        
        for (let room of tableRooms) {
            rooms.push(room.textContent);
        };
        
        return rooms;
    })();
    
    for (let room of rooms) {
        if (!alreadyRooms.includes(room.name)) {
            const rdom = document.createElement("li");
            
            rdom.classList.add("painel-item");
            rdom.classList.add("room");
            rdom.textContent = room.name;
            
            if (room.has_password) {
                const i = document.createElement("img");
                i.src = "../midia/images/padlock.png";
                i.classList.add("padlock");
                rdom.append(i);
            }
            
            roomsTable.append(rdom);
        }
    }
});


enterRoomBtn.addEventListener("click", () => {
    if (!roomNameInput.value) return;
    sendMsg(new EnterRoomMsg(roomNameInput.value));
});


addHandler("enter_room", (data) => {
    if (!data.state) {
        alert("Room not found.");
        return;
    }

    window.location.href =
        `room.html?room=${encodeURIComponent(data.room_name)}`;
});