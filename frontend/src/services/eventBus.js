// For Vue 3, we use a simple event emitter instead of Vue instance

class EventEmitter {
  constructor() {
    this.events = {};
  }

  $on(eventName, fn) {
    if (!this.events[eventName]) {
      this.events[eventName] = [];
    }
    this.events[eventName].push(fn);
    return this;
  }

  $off(eventName) {
    if (eventName) {
      delete this.events[eventName];
    } else {
      this.events = {};
    }
    return this;
  }

  $emit(eventName, data) {
    if (this.events[eventName]) {
      this.events[eventName].forEach(fn => fn(data));
    }
    return this;
  }
}

export const EventBus = new EventEmitter();
