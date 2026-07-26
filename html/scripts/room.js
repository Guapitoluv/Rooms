import { identified, socketReady, addHandler, sendMsg } from "./main.js";
import { EnterRoomMsg, RequestChatMsg, ChatMsg } from "./messages/messages.js";

const params = new URLSearchParams(window.location.search);
const roomName = params.get("room");

//console.log("author="+params.get("author"));

const msgInput = document.getElementById("message-input");
const sendBtn = document.getElementById("send-message");
const chat = document.getElementById("chat");
const chatMessages = chat.querySelector(".painel-table");
const roomNameDOM = document.getElementById("room-name");

roomNameDOM.textContent = roomName;
await socketReady;
await identified;
console.log("roomName: "+roomName);
sendMsg(new EnterRoomMsg(roomName));
sendMsg(new RequestChatMsg());

addHandler("chat_messages", (data) => {
    console.log("received chat messages");
    
    const ids = [];

    for (const msg of chatMessages.querySelectorAll(".painel-item")) {
        ids.push(msg.dataset.id);
    }

    for (const msg of data.messages) {
        if (!ids.includes(msg.id)) {
            const newMsg = document.createElement("li");

            newMsg.classList.add("painel-item");
            if (msg.author == localStorage.getItem("userName")) {
                newMsg.textContent = `[${msg.time}][You]:${msg.message}`;
            } else {
                newMsg.textContent = `[${msg.time}][${msg.author}]: ${msg.message}`;
            }
            newMsg.dataset.id = msg.id;

            chatMessages.append(newMsg);
        }
    }
});

addHandler("chat_message", (data) => {
    console.log("received chat message");
    
    const ids = [];

    for (const msg of chatMessages.querySelectorAll(".painel-item")) {
        ids.push(msg.dataset.id);
    }
    
    const msg = data.message;
    
    if (!ids.includes(data.message_id)) {
        const newMsg = document.createElement("li");
        
        newMsg.classList.add("painel-item");
        if (msg.author == localStorage.getItem("userName")) {
            newMsg.textContent = `[${msg.time}][You]: ${msg.message}`;
        } else {
            newMsg.textContent = `[${msg.time}][${msg.author}]: ${msg.message}`;
        }
        newMsg.dataset.id = data.message.id;
        
        chatMessages.append(newMsg);
    }
});
console.log
sendBtn.addEventListener("click", async () => {
    console.log("clicked");
    if (!msgInput.value.trim()) return;
    
    const msg_id = crypto.randomUUID();
    const now = new Date();
    
    const n = now.toLocaleTimeString();
    
    await sendMsg(new ChatMsg(msgInput.value, msg_id, n));
    msgInput.value = "";
});