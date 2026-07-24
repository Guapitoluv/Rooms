class Message {
    constructor(type) {
        this.id = crypto.randomUUID();
        this.type = type;
    }
}


export class CreateRoomMsg extends Message {
    constructor(room_name, author_name, password=null) {
        super("create_room");
        this.room_name = room_name;
        this.author_name = author_name;
        this.password = password;
    }
}

export class RequestRoomsListMsg extends Message {
    constructor() {
        super("request_rooms_list");
    }
}


export class RequestChatMsg extends Message {
    constructor() {
        super("request_chat_messages");
    }
}


export class ChatMsg extends Message {
    constructor(message, message_id, time) {
        super("chat_message");
        this.message = message;
        this.message_id = message_id;
        this.time = time;
    }
}


export class EnterRoomMsg extends Message {
    constructor(room_name) {
        super("enter_room");
        this.room_name = room_name;
    }
}


export class IdentifyMsg extends Message {
    constructor(user_name) {
        super("identify");
        this.user_name = user_name;
    }
}