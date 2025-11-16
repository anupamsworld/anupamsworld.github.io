import os

def build_tree(root_dir):
    """
    Build a nested dictionary representing only folders that contain index.html
    (directly or in subfolders).
    """
    tree = {}
    for dirpath, _, filenames in os.walk(root_dir):
        rel_dir = os.path.relpath(dirpath, root_dir)
        parts = rel_dir.split(os.sep) if rel_dir != "." else []
        node = tree
        for part in parts:
            node = node.setdefault(part, {})

        # Only record index.html
        for file in filenames:
            if file.lower() == "index.html":
                node[file] = None
    return tree


def prune_tree(node):
    """
    Remove folders that do not contain index.html (directly or indirectly).
    """
    keys_to_delete = []
    for key, child in list(node.items()):
        if isinstance(child, dict):  # it's a folder
            prune_tree(child)
            if not child:  # empty folder after pruning
                keys_to_delete.append(key)
    for key in keys_to_delete:
        del node[key]


def render_tree(node, prefix=""):
    """
    Render the nested dictionary into HTML <details>/<summary> structure.
    Ensure index.html appears at the top of each list.
    """
    html = ""

    # Sort keys but ensure index.html comes first
    items = sorted(node.items(), key=lambda x: (x[0].lower() != "index.html", x[0].lower()))

    for name, child in items:
        if child is None:  # index.html file
            path = os.path.join(prefix, name).replace("\\", "/")
            html += f"<li><a href='{path}' target='_blank'>{name}</a></li>\n"
        else:  # folder
            sub_prefix = os.path.join(prefix, name)
            html += f"<li><details><summary>{name}</summary>\n<ul>\n"
            html += render_tree(child, sub_prefix)
            html += "</ul></details></li>\n"
    return html


def generate_sitemap(root_dir, output_file="sitemap.html"):
    tree = build_tree(root_dir)
    prune_tree(tree)  # remove folders without index.html

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n<html>\n<head>\n")
        f.write("<meta charset='UTF-8'>\n<title>Sitemap</title>\n<meta name='viewport' content='width=device-width, initial-scale=1.0' />")

        # ⭐ ONLY THIS STYLE BLOCK UPDATED ⭐
        f.write("""
<style>
body {
    background: linear-gradient(135deg, #bad6f9, #bbf8e5);
    font-family: Arial;
    padding: 20px;
}

/* Tree styling */
ul {
    list-style-type: none;
    margin-left: 15px;
    padding-left: 12px;
    border-left: 2px solid #e0e0e0;
}

/* Folder label */
details > summary {
    font-size: 15px;
    font-weight: 600;
    padding: 4px 6px;
    cursor: pointer;
    border-radius: 6px;
    transition: background 0.2s ease;
}

/* Hover folder */
details > summary:hover {
    background: #f0f4ff;
}

/* File links */
li a {
    text-decoration: none;
    font-size: 14px;
    padding: 4px 6px;
    display: inline-block;
    border-radius: 6px;
    transition: background 0.2s ease, padding-left 0.2s;
}

/* Hover file */
li a:hover {
    background: #e9f0ff;
    padding-left: 10px;
}

/* Folder icons */
/* Closed folder */
details:not([open]) > summary::before {
    content: "📁 ";
}

/* Open folder */
details[open] > summary::before {
    content: "📂 ";
}

/* File icon */
li a::before {
    content: "📄 ";
}
</style>
""")

        f.write("</head>\n<body>\n")
        f.write("<h1>Sitemap</h1>\n")
        f.write("<h2>Click the topics/directory names to unfold/fold them</h2>\n<ul>\n")
        f.write(render_tree(tree, prefix=""))  # start with relative paths
        f.write("</ul>\n</body>\n</html>\n")

    print(f"Sitemap generated: {output_file}")


# Example usage
if __name__ == "__main__":
    generate_sitemap(root_dir="./")  # Change '.' to the target directory
