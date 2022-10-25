var editor = ace.edit("editor");
editor.setFontSize(15);
editor.setShowPrintMargin(false);
// set theme
$("li#chrome").click(function () {
    editor.setTheme("ace/theme/chrome");
});
$("li#eclipse").click(function () {
    editor.setTheme("ace/theme/eclipse");
});
$("li#github").click(function () {
    editor.setTheme("ace/theme/github");
});
$("li#xcode").click(function () {
    editor.setTheme("ace/theme/xcode");
});
$("li#chaos").click(function () {
    editor.setTheme("ace/theme/chaos");
});
$("li#dracula").click(function () {
    editor.setTheme("ace/theme/dracula");
});
$("li#solarized_light").click(function () {
    editor.setTheme("ace/theme/solarized_light");
});
$("li#solarized_dark").click(function () {
    editor.setTheme("ace/theme/solarized_dark");
});

var JavaScriptMode = ace.require("ace/mode/java").Mode;
editor.session.setMode(new JavaScriptMode());

// set run click event
$("button#run").click(function () {
    $("textarea#output").empty();
    var code = editor.getValue();
    $.post("run",
        {
            code: code,
            user_id: getUniqueUserId()
        },
        function (data, status) {
            $("textarea#output").append(data.response);
        });
});

// load examples
$.post("examples", {},
    function (data, status) {
        var ems = data.examples;
        for (var k in ems) {
            $("ul#examples_list").append("<li class='nav-header'>" + k + "</li>");
            for (var n in ems[k]) {
                $("ul#examples_list").append("<li><a id="+ k +">" + ems[k][n] + "</a></li>");
            }
            $("a#" + k).click(function () {
                getExample(this.id, this.text);
            });
        }
    });

function getExample(folder, file) {
    $.post("example", {
        parent: folder,
        name: file
    }, function (data, status) {
        editor.setValue(data.code, -1);
        });
}