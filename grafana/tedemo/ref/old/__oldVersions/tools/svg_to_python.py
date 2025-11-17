import sys
import os
import xml.etree.ElementTree as ET
from typing import TextIO

NS_SVG = "http://www.w3.org/2000/svg"


def strip_ns(tag: str) -> str:
    if tag.startswith("{"):
        return tag.split("}", 1)[1]
    return tag


def escape_str(s: str) -> str:
    return s.replace("\\", "\\\\").replace("\"", "\\\"")


def write_create_call(out: TextIO, var_parent: str, el: ET.Element, var_name: str, indent: str) -> None:
    tag = strip_ns(el.tag)
    attrs = {k: v for k, v in el.attrib.items()}
    # Skip scripts – embedded script is injected by generator
    if tag.lower() == "script":
        return
    # Build attributes literal
    if attrs:
        # Preserve attribute order by iterating items (in CPython 3.7+ it preserves insertion order)
        attrs_kv = ", ".join([f'"{escape_str(k)}": "{escape_str(v)}"' for k, v in attrs.items()])
        attrs_repr = "{" + attrs_kv + "}"
    else:
        attrs_repr = "None"
    text = el.text or ""
    text_arg = f'"{escape_str(text)}"' if text.strip() else "None"
    out.write(f"{indent}{var_name} = create_element({var_parent}, \"{tag}\", {attrs_repr}, {text_arg})\n")


def emit_children(out: TextIO, parent_var: str, parent_el: ET.Element, indent_level: int) -> None:
    indent = "  " * indent_level
    idx = 0
    for child in list(parent_el):
        tag = strip_ns(child.tag).lower()
        if tag == "script":
            continue
        child_var = f"n{indent_level}_{idx}"
        write_create_call(out, parent_var, child, child_var, indent)
        emit_children(out, child_var, child, indent_level + 1)
        idx += 1


def convert(svg_path: str, output_py: str) -> None:
    tree = ET.parse(svg_path)
    root = tree.getroot()
    with open(output_py, "w", encoding="utf-8") as out:
        out.write("# Auto-generated from SVG by tools/svg_to_python.py\n")
        out.write("# Recreates the SVG DOM structure using create_element helper from generate_svg.py\n\n")
        out.write("def apply_blueprint(svg_root, create_element):\n")
        # Build everything under the provided svg_root (assumes svg_root is an <svg>)
        # We skip scripts so that generator can inject embedded JS copy itself
        emit_children(out, "svg_root", root, 1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python tools/svg_to_python.py <input.svg> <output.py>")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
