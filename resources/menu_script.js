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
        // perhaps have a checkmark for deletion?
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
    'Transfer': function (content) {
        content.innerHTML = 'Transfer';

        var text_template = document.getElementById('transfer_template').innerHTML;
        var template = Handlebars.compile(text_template);
        var context = {
            'dropdown': [{
                'name': 'couples',
                'option': [
                    '0987654321',
                    '1234567890'
                ]
            }, {
                'name': 'company',
                'option': [
                    'mtel',
                    'vivacom'
                ]
            }]
        }
        content.innerHTML = template(context);

        function fill_info () {
            
            template(context);
        }

        request_info('localhost/data',{'couple': 'id'});
    }
};

const menu_order = ['Enter', 'Couple', 'Edit', 'Reference', 'Transfer'];
const submenu_order = ['Device', 'SIM', 'Couple', 'Transfer'];

// combine the two in one
// remove the Transfer collision and figure out to make recursively
function main () {
    let elements = {};

    function building_submenu_callback () {
        let elements = {};
        let menu = document.getElementById('submenu');
        remove_children(menu);

        for (let button_type in mapping[this.id]) {
            elements[button_type] = build_menu_button(
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
        elements[button_type] = build_menu_button(
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


window.addEventListener('load', main);
window.addEventListener('load', function(){console.log('SHIT')});
