import os
from markdown_blocks import markdown_to_html_node


def generate_page(from_path, template_path, dest_path, basepath):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    template = template.replace('href="/', f"href=\"{basepath}")
    template = template.replace('src="/', f"src=\"{basepath}")

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for root, _, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md'):
                md_path = os.path.join(root, file)
                relative_path = os.path.relpath(md_path, dir_path_content)
                html_relative_path = relative_path.replace('.md', '.html')
                dest_path = os.path.join(dest_dir_path, html_relative_path)
                generate_page(
                    md_path,
                    template_path,
                    dest_path,
                    basepath
                )