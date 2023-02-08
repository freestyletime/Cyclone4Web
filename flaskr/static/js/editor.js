// setup
var editor = ace.edit("editor");
editor.setFontSize(15);
editor.setShowPrintMargin(false);
editor.setOptions({
    enableBasicAutocompletion: true,
    enableLiveAutocompletion: true,
    enableSnippets: true
});

// set mode
var JavaMode = ace.require("ace/mode/java").Mode;
editor.session.setMode(new JavaMode());

// shortcut - run
editor.commands.addCommand({
    name: 'run-script',
    bindKey: { win: 'Ctrl-R', mac: 'Command-R' },
    exec: function (editor) {
        $("button#run").click();
    },
    readOnly: true
});

// shortcut - upload
editor.commands.addCommand({
    name: 'save-script',
    bindKey: { win: 'Ctrl-U', mac: 'Command-U' },
    exec: function (editor) {
        $("button#upload").click();
    },
    readOnly: true
});

// set theme
var preTheme;
var themelist = ace.require("ace/ext/themelist");
for (let item of themelist.themes.values()) {
    $("ul#theme").append("<li id=" + item['name'] + "><a>" + item['caption'] + "</a></li>")
    $("li#" + item['name']).click(function () {
        if (preTheme != null) $("li#" + preTheme).attr("class", "");
        $(this).attr("class", "active");
        editor.setTheme(item['theme']);
        preTheme = item['name'];
    });
}

$("ul#theme").css({
    'height': '500px',
    'overflow-y': 'scroll'
});

// fit the size of the editor when its changes
var resizeTimer = null;
const resizeObserver = new ResizeObserver((e) => {
    if (resizeTimer) {
        clearTimeout(resizeTimer);
    }
    resizeTimer = setTimeout(function () {
        editor.resize();
    }, 500)
});
resizeObserver.observe(document.querySelector('#editor'));

// set run click event
$("button#run").click(function () {
    var code = editor.getValue();
    $(".notifyjs-foo-base .yes").trigger('notify-hide');
    $.post("run",
        {
            code: code,
            unique_user_id: getUniqueUserId()
        },
        function (data, status) {
            if (status == 'success') {
                var text = data.response;
                var pattern = /<a\s+[^>]*href\s*=\s*(["'])([^"']+)\1[^>]*>(.*?)<\/a>/g;
                var match = pattern.exec(text);

                if (match != null) {
                    var updatedText = text.replace(pattern, function (tag) {
                        return ' Trace download link is below';
                    });
                    $('textarea#output').val(updatedText);
                    var aTag = match[0];
                    var title = $("<h4/>").append(aTag);

                    //add a new style 'foo'
                    $.notify.addStyle('foo', {
                        html:
                            "<div>" +
                            "<div class='clearfix'>" +
                            "<div class='title' data-notify-html='title'/>" +
                            "<div class='buttons'>" +
                            "<button class='yes' data-notify-text='button'></button>" +
                            "</div>" +
                            "</div>" +
                            "</div>"
                    });

                    $(document).on('click', '.notifyjs-foo-base .yes', function () {
                        //hide notification
                        $(this).trigger('notify-hide');
                    });

                    $("textarea#output").notify({
                        title: title,
                        button: 'dismiss'
                    }, {
                        style: 'foo',
                        autoHide: false,
                        clickToHide: false
                    });
                } else $("textarea#output").val(text);
            } else {
                alert("Failed to run the code.");
            }
        });
});

// set save click event
$("button#save").click(function () {
    var code = editor.getValue();
    $.post("save2LocalFile", {
        code: code,
    }, function (data, status, xhr) {
        if (status == 'success') {
            var header = xhr.getResponseHeader('Content-Disposition');
            if (header && header.indexOf('attachment') !== -1) {
                const parts = header.split(';');
                const link = document.createElement('a');
                link.style.display = 'none';
                link.download = parts[1].split('=')[1];
                var blob = new Blob([data], { type: 'text/plain' });
                link.href = window.URL.createObjectURL(blob);
                link.click();
            }
        } else {
            alert("Failed to save the file.");
        }
    });
});

// set clear click event
$("button#clear").click(function () {
    var value = editor.getValue();
    if (value != "") editor.setValue("", -1);
});

// set upload click event
$("button#upload").click(function () {
    var form = $("<form method='post'></form>");
    var input_file = $("<input id='file1' name='file 'type='file' accept='*'>");
    var url = 'upload';
    form.attr({ "action": url, "enctype": "multipart/form-data" });
    form.append(input_file);
    input_file.change(function (e) {
        var fileMsg = e.currentTarget.files;
        var fileSize = fileMsg[0].size;
        // Let sever to check
        // var fileType = fileMsg[0].type;
        // var type = (fileType.substr(fileType.lastIndexOf("."))).toLowerCase();
        if (fileSize > 10240) {
            alert("The file size should be less than 10KB.");
            return false;
        }

        var formData = new FormData();
        formData.append("file", fileMsg[0]);
        $.ajax({
            url: url,
            type: 'POST',
            async: false,
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            success: function (data) {
                if (data.response) alert(data.response);
                if (data.code) editor.setValue(data.code, -1);
            }
        });
    })
    input_file.click();
});

const container1 = 'graph';
const container2 = 'machine';
function insertInStart(content) {
    var r = editor.find("(" + container1 + "|" + container2 + "){1}.*{", { caseSensitive: true, regExp: true });
    editor.moveCursorTo(r.start.row, 0);
    editor.insert(content + "\n");
}

// set trace click event
$("button#trace").click(function () {
    const opt = 'option-trace=true;';
    var code = editor.getValue();
    if (code.includes(opt)) {
        var r = editor.find(opt);
        editor.moveCursorTo(r.start.row, 0);
        editor.removeLines();
    } else {
        if (code.includes(container1) || code.includes(container2)) insertInStart(opt);
    }
});

// set timeout
let count = 0;
const timeout = "option-timeout="
function clearTimeoutText() {
    if (editor.getValue().includes(timeout)) {
        var r = editor.find(timeout);
        editor.moveCursorTo(r.start.row, 0);
        editor.removeLines();
    }
}

$("button#increment").click(function () {
    count++;
    $("span#count-value").text(count);
    clearTimeoutText();
    insertInStart(timeout + count + ";");
});
$("button#decrement").click(function () {
    clearTimeoutText();
    if (count > 0) {
        count--;
        $("span#count-value").text(count);
        if (count > 0) insertInStart(timeout + count + ";");
    }
});

// load examples in the cyclone folder
$.post("examples", {},
    function (data, status) {
        if (status == 'success') {
            var ems = data.examples;
            for (var k in ems) {
                $("ul#examples_list").append("<li class='nav-header'>" + k + "</li>");
                for (var n in ems[k]) {
                    $("ul#examples_list").append("<li><a id=" + k + ">" + ems[k][n] + "</a></li>");
                }
                $("a#" + k).click(function () {
                    getExample(this.id, this.text);
                });
            }
        } else {
            alert("Failed to get the examples.");
        }
    });

function getExample(folder, file) {
    $.post("example", {
        folder: folder,
        name: file
    }, function (data, status) {
        if (status == 'success') {
            editor.setValue(data.code, -1);
        } else {
            alert("Failed to get the code.");
        }
    });
}