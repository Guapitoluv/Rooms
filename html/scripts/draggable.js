export class DraggableBox {
    constructor(elementId) {
        this.box = document.getElementById(elementId);
        if (!this.box) return;
        
        this.exception = false;

        this.offsetX = 0;
        this.offsetY = 0;
        

        this.init();
    }

    init() {
        // Bind methods to 'this' context to ensure correct scope inside listeners
        this.onTouchStart = this.onTouchStart.bind(this);
        this.onTouchMove = this.onTouchMove.bind(this);
        this.onTouchEnd = this.onTouchEnd.bind(this);

        // Attach touch events
        this.box.addEventListener('touchstart', this.onTouchStart);
        this.box.addEventListener('touchmove', this.onTouchMove);
        this.box.addEventListener('touchend', this.onTouchEnd);
    }

    onTouchStart(e) {
        if (this.exception) return;
        
        const touch = e.touches[0];
        const rect = this.box.getBoundingClientRect();
        
        // Calculate offset between touch point and top-left of the box
        this.offsetX = touch.clientX - rect.left;
        this.offsetY = touch.clientY - rect.top;
    }

    onTouchMove(e) {
        if (this.exception) return;
        
        const touch = e.targetTouches[0];
        
        // Remove center alignment transforms once movement starts
        this.box.style.transform = 'none';
        
        // Calculate new coordinate positions
        const newX = touch.clientX - this.offsetX;
        const newY = touch.clientY - this.offsetY;
        
        // Update DOM styles
        this.box.style.left = `${newX}px`;
        this.box.style.top = `${newY}px`;
    }

    onTouchEnd() {
        //console.log(`Element ${this.box.id} stopped at: ${this.box.style.left}, ${this.box.style.top}`);
    }
    
    add_exception(exc) {
        exc.addEventListener("touchstart", () => {
            if (!this.exception) this.exception = true;
        })
        
        exc.addEventListener("touchend", () => {
            if (this.exception) this.exception = false;
        })
        
        exc.addEventListener("touchcancel", () => {
            if (this.exception) this.exception = false;
        })
    }

    // Optional: Clean up event listeners if the element is removed from DOM
    destroy() {
        this.box.removeEventListener('touchstart', this.onTouchStart);
        this.box.removeEventListener('touchmove', this.onTouchMove);
        this.box.removeEventListener('touchend', this.onTouchEnd);
    }
}
