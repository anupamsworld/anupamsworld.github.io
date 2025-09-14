function loadCSS(url) {
    let link = document.createElement("link");
    link.rel = "stylesheet";
    link.type = "text/css";
    link.href = url;
    document.head.appendChild(link);
}

function load_all(){
    loadCSS("/doc/design/css/document.css");
}