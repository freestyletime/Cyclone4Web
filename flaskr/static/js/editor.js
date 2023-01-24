// setup
var editor = ace.edit("editor");
editor.setFontSize(15);
editor.setShowPrintMargin(false);
editor.setOptions({
    enableBasicAutocompletion: true,
    enableLiveAutocompletion: true,
    enableSnippets: true
});

// set theme
var themelist = ace.require("ace/ext/themelist");
for(let item of themelist.themes.values()) {
    $("ul#theme").append("<li id=" + item['name'] + "><a>" + item['caption'] + "</a></li>")
    $("li#" + item['name']).click(function () {
        editor.setTheme(item['theme']);
    });
}

$("ul#theme").css({
    'height':'500px',
    'overflow-y':'scroll'
});

// set mode
var JavaMode = ace.require("ace/mode/java").Mode;
editor.session.setMode(new JavaMode());

// set run click event
$("button#run").click(function () {
    $("textarea#output").empty();
    var code = editor.getValue();
    $.post("run",
        {
            code: code,
            unique_user_id: getUniqueUserId()
        },
        function (data, status) {
            $("textarea#output").append(data.response);
        });
});

$("button#save").click(function () {
    var code = editor.getValue();
    $.post("files", {
        code: code,
    }, function (data, status, xhr) {
        if(status == 'success'){
            var header = xhr.getResponseHeader('Content-Disposition');
            if (header && header.indexOf('attachment') !== -1) {
                const parts = header.split(';');
                const link = document.createElement('a');
                link.style.display = 'none';
                link.download =  parts[1].split('=')[1];
                var blob = new Blob([data], {type: 'text/plain'});
                link.href = window.URL.createObjectURL(blob);
                link.click();
            }
        } else {
            //TODO
        }
    });
});

$("button#clear").click(function () {
    var value = editor.getValue();
    if(value != "") editor.setValue("", -1);
});

$("button#upload").click(function () {
    var form = $("<form method='post'></form>");
    var input_file = $("<input id='file1' name='file 'type='file' accept='*'>");
    var url = 'upload';
    form.attr({"action": url, "enctype":"multipart/form-data"});
    form.append(input_file);
    input_file.change(function(e){
        var fileMsg = e.currentTarget.files;
        // var fileName = fileMsg[0].name;
        var fileSize = fileMsg[0].size;
        // Let sever to check
        // var fileType = fileMsg[0].type;
        // var type = (fileType.substr(fileType.lastIndexOf("."))).toLowerCase();
        if(fileSize > 10240) {
            alert("The file size should be less than 10KB.");
            return false;
        }

        var formData = new FormData();
        formData.append("file", fileMsg[0]);
        $.ajax({
            url: 'upload',
            type: 'POST',
            async: false,
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            success: function (data) {
                if(data.response) alert(data.response);
                if(data.code)  editor.setValue(data.code, -1);
            }
        });
      })
    input_file.click();
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
        folder: folder,
        name: file
    }, function (data, status) {
        editor.setValue(data.code, -1);
    });
}