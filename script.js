const mapping = {
    'Enter': {
        'Device': function (content) {
            content.innerHTML = 'Enter Device';
        },
        'SIM': function (content) {
            content.innerHTML = 'Enter SIM';
        }
    },
    'Couple': function (content) {
        content.innerHTML = 'Couple';
    },
    'Edit': {
        'Device': function (content) {
            content.innerHTML = 'Edit Device';
        },
        'SIM': function (content) {
            content.innerHTML = 'Edit SIM';
        },
        'Couple': function (content) {
            content.innerHTML = 'Edit Couple';
        }
    },
    'Reference': {
        'Device': function (content) {
            content.innerHTML = 'Reference Device';
        },
        'SIM': function (content) {
            content.innerHTML = 'Reference SIM';
        },
        'Couple': function (content) {
            content.innerHTML = 'Reference Couple';
        },
        'Transfer': function (content) {
            content.innerHTML = 'Reference Transfer';
        }
    },
    'Transfer': function (content ){
        content.innerHTML = 'Transfer';
    }
};

const menu_order = ['Enter', 'Couple', 'Edit', 'Reference', 'Transfer'];
const submenu_order = ['Device', 'SIM', 'Couple', 'Transfer'];

function  build_button (button, callback, submenu = true) {
    var div = document.createElement('div');
    div.className = 'nav_btn' +
        (submenu ? ' secondary_btn': ' primary_btn') +
        (button == 'Device' ? ' offset_btn': '');
    div.textContent = button;
    div.id = button;
    div.onclick = callback;
    return div;
}

function remove_children (element) {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}

// ITS TWICE
// PLEASE MAKE IT ONE
function main () {
    let elements = {};

    function building_submenu_callback () {
        let elements = {};
        let menu = document.getElementById('submenu');
        menu.innerHTML = '';

        for (let button_type in mapping[this.id]) {
            elements[button_type] = build_button(
                button_type,
                function (button, parent) {
                    return function () {
                        remove_children(document.getElementById('submenu'));
                        mapping[parent][button](document.getElementById('content'));
                    }
                }(button_type, this.id),
                true
            );
        }

        for (let element of submenu_order) {
            try {
                // other typerrors that may arise are silenced. Make better checks
                menu.appendChild(elements[element]);
            } catch (exception) {
                if (exception.name !== 'TypeError') throw exception;
                // else console.log('Move on. This one isn\'t needed 2');
            }
        }
    }

    for (let button_type in mapping) {
        // console.log(mapping[button_type]);
        elements[button_type] = build_button(
            button_type,
            (typeof mapping[button_type] === 'function') ?
            function (){
                remove_children(document.getElementById('submenu'));
                mapping[button_type](document.getElementById('content'));
            } :
            building_submenu_callback,
            false
        );
    }

    let menu = document.getElementById('menu');
    for (let element of menu_order) {
        try {
            menu.appendChild(elements[element]);
        } catch (exception) {
            if (exception.name !== 'TypeError') throw exception;
            // else console.log('Move on. This one isn\'t needed');
        }
    }
}

// new elements are hard to add. make more dynamic

window.addEventListener('load', main);
