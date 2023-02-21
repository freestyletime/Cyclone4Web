$(document).ready(function () {
    init_document_ready();
});

function init_document_ready() {
    create_themeSwitch();
}

// web theme switch
function create_themeSwitch() {
    const key_theme = "current_theme";
    const value_theme_light = 0;
    const value_theme_dark = 1;
    if (Cookies.get(key_theme) == value_theme_dark) {
        do_themeSwitch_dark();
    } else {
        do_themeSwitch_light();
    }

    $("div#theme_web").click(function () {
        if ($("img#light").css("display") === "none") {
            $("img#light").css("display", "inline");
            $("img#dark").css("display", "none");
            $("body").css("background-color", "white");
            $("img#github-logo").attr("src", "/static/img/github-mark.png")
            $("#theme-link").attr("href", "/static/css/style_light.css");
            Cookies.set(key_theme, value_theme_light, { expires: 90 });
        } else {
            $("img#light").css("display", "none");
            $("img#dark").css("display", "inline");
            $("body").css("background-color", "black");
            $("img#github-logo").attr("src", "/static/img/github-mark-white.png")
            $("#theme-link").attr("href", "/static/css/style_dark.css");
            Cookies.set(key_theme, value_theme_dark, { expires: 90 });
        }
    });

    $('div#theme_web').on('click', function () {
        // const customEvent = new CustomEvent('onThemeChange', { theme: { current: Cookies.get(key_theme) }});
        const customEvent = new CustomEvent('onThemeChange', { detail: { theme: Cookies.get(key_theme) } });
        document.dispatchEvent(customEvent);
    });
}

function do_themeSwitch_dark() {
    $("ul#header_btns").prepend(`
        <li>
        <div id='theme_web'>
        <img id="dark" src="/static/img/theme_dark.svg" alt="dark">
        <img style="display:none;" id="light" src="/static/img/theme_light.svg" alt="light">
        </div>
        </li>
    `);

    $("body").css("background-color", "black");
    $("img#github-logo").attr("src", "/static/img/github-mark-white.png")
    $("#theme-link").attr("href", "/static/css/style_dark.css");
}

function do_themeSwitch_light() {
    $("ul#header_btns").prepend(`
        <li>
        <div id='theme_web'>
        <img id="light" src="/static/img/theme_light.svg" alt="light">
        <img style="display:none;" id="dark" src="/static/img/theme_dark.svg" alt="dark">
        </div>
        </li>
    `);

    $("body").css("background-color", "white");
    $("img#github-logo").attr("src", "/static/img/github-mark.png")
    $("#theme-link").attr("href", "/static/css/style_light.css");
}