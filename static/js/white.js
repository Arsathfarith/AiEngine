/* Minimal White.js helper utilities for SmartHire UI */
window.White = {
    on: function (selector, event, callback) {
        const element = document.querySelector(selector);
        if (element) {
            element.addEventListener(event, callback);
        }
    },
    addClass: function (selector, className) {
        const element = document.querySelector(selector);
        if (element) element.classList.add(className);
    },
    removeClass: function (selector, className) {
        const element = document.querySelector(selector);
        if (element) element.classList.remove(className);
    },
    createElement: function (tag, props) {
        const element = document.createElement(tag);
        for (const key in props) {
            if (key === "text") element.textContent = props[key];
            else if (key === "html") element.innerHTML = props[key];
            else element.setAttribute(key, props[key]);
        }
        return element;
    },
};
