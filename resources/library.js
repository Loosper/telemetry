function  build_menu_button (button, callback, submenu = true) {
    var div = document.createElement('div');
    div.className = 'nav_btn' +
        (submenu ? ' secondary_btn': ' primary_btn') +
        (button == 'Device' ? ' offset_btn': '');
    div.textContent = button;
    div.id = button;
    div.onclick = callback;
    return div;
}

// to request info from server pass a callback 
// that executes with the request as a local variable
// maybe it can just be given the response? Does that work? Is it enough?
function request_info (URL, callback, parameters = '') {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (request.readyState == 4 && request.status == 200) {
            callback(this.response);
        }
    }

    // perhaps the parameters are a dict and we process here?
    request.open("GET", URL);
    request.send();
    return false;
}
// DO WE DELETE INFO (sim/device?)?

function remove_children (element) {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}