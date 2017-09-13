function read_cookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1,c.length);
        }
        if (c.indexOf(nameEQ) === 0) {
            return c.substring(nameEQ.length,c.length);
        }
    }
    return null;
}

var default_options = {"auto_dismissible": true, "dismiss_timeout": 4000};

function show_info_block(error_level, string, options) {
    /*
        Shows notification block at the top of the page.
     */
    // get date for alert ID
    var d = new Date();

    // prepare request
    var data = {
        "error_level": error_level, "string": string, "alert_id": d.getTime()
    };
    var template = "includes/decadence/alert_block.html";

    // check if options are defined
    if (options) {
        if (options.auto_dismissible) {
            // enable auto dismissing
            $(function() {
                setTimeout(function () {
                    $("#alert-"+data.alert_id).alert('close');
                }, options.dismiss_timeout);
            });
        }
        if (options.has_button) {
            data.has_button = true;
            data.button_text = options.button_text;
            data.button_href = options.button_href;
        }
        if (options.icon) {
            data.icon = options.icon;
        }
        if (options.custom_template) {
            // override template with provided in options
            template = options.custom_template
        }
        if (options.extra_data) {
            // if extra data is provided, replace data in data array
            var extra_keys = Object.keys(options.extra_data);
            for (var i=0; i<extra_keys.length; i++) {
                data[extra_keys[i]] = options.extra_data[extra_keys[i]];
            }
        }
    }

    // add block
    include_from_template("#body-alerts", template, data, "afterBegin");

    // we might want to have that one
    return data.alert_id
}

function include_from_template(selector, template, data, mode) {
    /*
        Uses API to generate blocks from Django templates and includes them in the page.
        Takes css selector (like "#bread"), template file name ("includes/cancer.html") and context data.
        Also you can switch between different inclusion modes.
        wow, this is probably insecure as fuck
     */
    // create Ajax request
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'decadence/template/', true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    data.template = template;

    // connect signal that gets fired after request is finished
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                // get block by css selector
                var block = document.querySelector(selector);

                // insert HTML
                block.insertAdjacentHTML(mode, xhr.responseText)
            } else {
                // stuff broke, show error
                show_info_block("danger", "Decadence failed to render template '"+template+"' with error '"+xhr.status+"'. Except stuff to be broken",
                default_options);
            }
        }
    };
    // send a request
    xhr.send("csrfmiddlewaretoken="+read_cookie("csrftoken")+"&data="+encodeURIComponent(JSON.stringify(data)));
}