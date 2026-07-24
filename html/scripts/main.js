import { IdentifyMsg } from "./messages/messages.js"

//lock: <a href="https://www.flaticon.com/free-icons/lock" title="lock icons">Lock icons created by Gregor Cresnar - Flaticon</a>

/**************************************************
 * VARIABLES
 **************************************************/

const protocol = window.location.protocol === "https:" ? "wss://" : "ws://";

const host = window.location.protocol === "file:"
    ? "localhost:8000"
    : window.location.host;

const socketUrl = `${protocol}${host}/socket`;
const handlers = {};

export const socket = new WebSocket(socketUrl);
export const socketReady = new Promise(resolve => {
    socket.addEventListener("open", () => resolve());
});
export const identified = new Promise(resolve => {
    addHandler("identified", resolve);
});

/**************************************************
 * FUNCTIONS
 **************************************************/

export function addHandler(type, handler) {
    handlers[type] = handler;
}


export function sendMsg(msg) {
    if (socket.readyState !== WebSocket.OPEN) {
        console.warn("Socket não conectado.");
        return;
    }

    socket.send(JSON.stringify(msg));
}

/**************************************************
 * EVENTS
 **************************************************/

socket.addEventListener("open", () => {
    console.log("opened");
    sendMsg(new IdentifyMsg(localStorage.getItem("userName")));
});


socket.addEventListener("error", (event) => {
    console.error("WebSocket error:", event);
});


socket.addEventListener("close", (event) => {
    console.log("WebSocket closed:", event.code, event.reason);
});


socket.addEventListener("message", (event) => {
    const data = JSON.parse(event.data);
    console.log("received msg: "+data.type);
    if (!data.type) return;
    console.log("msgtype: "+data.type);
    handlers[data.type]?.(data);
});