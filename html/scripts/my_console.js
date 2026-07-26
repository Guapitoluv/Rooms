import { DraggableBox } from "./draggable.js";

class Console {
    constructor(e) {
        this.element = e;
        
        const h = document.createElement("h4");
        
        h.id = "console-title";
        h.textContent = "Console";
        
        this.logsDOM = document.createElement("ul");
        this.logsDOM.id = "console-logs";
        
        this.element.append(h);
        this.element.append(this.logsDOM);
    }
    
    init() {
        document.body.append(this.element)
        const td = new DraggableBox("console");
        td.add_exception(this.logsDOM);
    }
    
    log(text) {
        const fileName = import.meta.url.substring(import.meta.url.lastIndexOf('/') + 1);
        const log = document.createElement("li");
        
        log.classList.add("log");
        log.textContent += `[${fileName}]: ${text}`;
        
        this.logsDOM.append(log);
    }
    
    remove() {
        this.element.remove();
    }
}

const terminal = document.createElement("div");
terminal.id = "console";

export const myConsole = new Console(terminal);