var menu = {
    'Transfer': 0,
    'Couple': 0,
    'Enter': 2,
    'Edit': 3,
    'Reference': 4,
}
var mapping = ['Device', 'SIM', 'Couple', 'Transfer'];
// menu = {'Enter': '', 'Couple': '', 'Edit': '', 'Reference': '', 'Transfer': ''};
var subelements = {'Device': '', 'SIM': '', 'Couple': '', 'Transfer': ''};
var mode = '';
var body = '';

// function load_enter(){
//     if(mode[1] == 'SIM'){
//         body.innerHTML = 'SIM';
//     }else{
//         body.innerHTML = 'Device';
//     }
//     // placeholder. illustrates what will kind of happen
// }

// function load_couple(){
//     body.innerHTML = 'Couple';
// }

// function load_edit(){
//     // ...create stuff in common
//     if(mode[1] == 'Device'){
//         body.innerHTML = 'Edit device';
//     }else if(mode[1] == 'SIM'){
//         body.innerHTML = 'Edit SIM';
//     }else{
//         body.innerHTML = 'Edit a couple';
//     }
// }

// function load_reference(){
//     // ...create stuff in common
//     if(mode[1] == 'Device'){
//         body.innerHTML = 'Query for device';
//     }else if(mode[1] == 'SIM'){
//         body.innerHTML = 'Query for SIM';
//     }else{
//         body.innerHTML = 'Wuery for a couple';
//     }   
// }

// function load_transfer(){
//     body.innerHTML = 'Transfer';
// }

function load_body(){
    mode = mode.split('_');

    
}

function set_submenu(){
    var nav_bar = document.getElementById('secondary_bar');
    // nav_bar.innerHTML = '';
    while(nav_bar.firstChild){
        nav_bar.removeChild(nav_bar.firstChild);
    }

    for(var i = 0; i < menu[mode]; i++){
        nav_bar.appendChild(subelements[mapping[i]]);
    }
    load_body();
}

function main(){
    body = document.getElementById('content');

    for(var key in menu){
        var element = document.getElementById(key);
        element.onclick = function(i) {
            return function(event) {
                // console.log(event);
                mode = i;
                set_submenu();
            }
            // make Mr. document listen for these things and only parse the [event] object.
            // Simplifies a lot
        }(key);
    }

    for(key in subelements){
        var link = document.createElement('a');
        var div = document.createElement('div');
        link.setAttribute('href', 'javascript:;');
        div.className = 'nav_btn secondary_btn';
        link.appendChild(div);
        div.textContent = key;
        div.onclick = function(){
            mode += '_' + key;
            load_body();
            document.getElementById('secondary_bar').innerHTML = '';
        };

        if (key == 'Device') {
            div.id = 'offset_btn';
        }
        subelements[key] = link;
    }
}

// new elements are hard to add. make more dynamic

window.addEventListener('load', main);
