export class Message {
    constructor(type) {
        this.id = crypto.randomUUID();
        this.type = type;
    }
}