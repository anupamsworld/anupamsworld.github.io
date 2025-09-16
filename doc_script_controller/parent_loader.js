function loadCSS(url) {
    let link = document.createElement("link");
    link.rel = "stylesheet";
    link.type = "text/css";
    link.href = url;
    document.head.appendChild(link);
}
function loadJS(url, callback) {
    let script = document.createElement("script");
    script.src = url;
    script.type = "text/javascript";
    script.onload = callback; // Run after script loads
    document.head.appendChild(script);
	
}
function load_all(){
    loadCSS("/doc/design/css/document.css");
    // Load meta.html automatically
    loadMetaTags("/doc/design/meta/meta.html");
}


function loadMetaTags(filePath) {
      fetch(filePath)
        .then(response => {
          if (!response.ok) throw new Error("Failed to load " + filePath);
          return response.text();
        })
        .then(html => {
          // Parse the loaded HTML snippet
          let tempDiv = document.createElement("div");
          tempDiv.innerHTML = html;

          tempDiv.querySelectorAll("meta").forEach(newMeta => {
            let selector = "";
            if (newMeta.hasAttribute("name")) {
              selector = `meta[name="${newMeta.getAttribute("name")}"]`;
            } else if (newMeta.hasAttribute("property")) {
              selector = `meta[property="${newMeta.getAttribute("property")}"]`;
            } else if (newMeta.hasAttribute("charset")) {
              selector = "meta[charset]";
            }

            let existingMeta = selector ? document.head.querySelector(selector) : null;

            if (existingMeta) {
              // Update attributes if already exists
              [...newMeta.attributes].forEach(attr => {
                existingMeta.setAttribute(attr.name, attr.value);
              });
            } else {
              // Append if not found
              document.head.appendChild(newMeta);
            }
          });
        })
        .catch(err => console.error("Error:", err));
    }

    