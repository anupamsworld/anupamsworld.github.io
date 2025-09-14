import os

def build_tree(root_dir):
    """
    Build a nested dictionary representing only folders that contain HTML files (directly or in subfolders).
    """
    tree = {}
    for dirpath, _, filenames in os.walk(root_dir):
        rel_dir = os.path.relpath(dirpath, root_dir)
        parts = rel_dir.split(os.sep) if rel_dir != "." else []
        node = tree
        for part in parts:
            node = node.setdefault(part, {})
        for file in filenames:
            if file.lower().endswith(".html"):
                node[file] = None
    return tree

def prune_tree(node):
    """
    Remove folders that do not contain any HTML files.
    """
    keys_to_delete = []
    for key, child in node.items():
        if child is not None:  # it's a folder
            prune_tree(child)
            if not child:  # remove empty folder
                keys_to_delete.append(key)
    for key in keys_to_delete:
        del node[key]

def render_tree(node, prefix=""):
    """
    Render the nested dictionary into HTML <details>/<summary> structure.
    """
    html = ""
    for name, child in sorted(node.items()):
        if child is None:
            # It's a file
            if name.lower()=="index.html":
                path = os.path.join(prefix, name).replace("\\", "/")
                html += f"<li><a href='{path}' target='_blank'>{name}</a></li>\n"
        else:
            # It's a folder
            sub_prefix = os.path.join(prefix, name)
            html += f"<li><details><summary>{name}</summary>\n<ul>\n"
            html += render_tree(child, sub_prefix)
            html += "</ul></details></li>\n"
    return html

def generate_sitemap(root_dir, output_file="sitemap.html"):
    tree = build_tree(root_dir)
    prune_tree(tree)  # remove folders without .html files

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n<html>\n<head>\n")
        f.write("<meta charset='UTF-8'>\n<title>Sitemap</title>\n")
        f.write("<style>body{font-family:Arial;} ul{list-style:none;}</style>\n")
        f.write("</head>\n<body>\n")
        f.write("<h1>Sitemap</h1>\n")
        f.write("<h2>Click the topics to unfold/fold them</h2>\n<ul>\n")
        f.write(render_tree(tree, prefix=root_dir))
        f.write("</ul>\n</body>\n</html>\n")

    print(f"Sitemap generated: {output_file}")

# Example usage
if __name__ == "__main__":
    generate_sitemap(root_dir="./")  # Change '.' to the target directory
