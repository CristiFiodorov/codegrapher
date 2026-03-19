# A part from this code is from https://github.com/IBM/tree-sitter-codeviews/blob/main/src/comex/utils/postprocessor.py

import json
from subprocess import check_call

import networkx as nx
from networkx.readwrite import json_graph


def write_networkx_to_json(graph, filename):
    graph_json = json_graph.node_link_data(graph)
    with open(filename, "w") as f:
        json.dump(graph_json, f)


def _dot_quote(s: str):
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace('\n', '\\n').replace('\r', '')
    return f'"{s}"'


# Color palette
_AST_FILL    = "#d4edda"   # light green
_AST_BORDER  = "#5a9a6e"   # dark green
_AST_EDGE    = "#2e7d32"   # green


def _node_style(data: dict):
    return f'fillcolor="{_AST_FILL}", color="{_AST_BORDER}"'


def _edge_style(data: dict):
    label = data.get("label", "")
    parts = [f'color="{_AST_EDGE}"']
    if label:
        parts.append(f'label={_dot_quote(label)}')
    return ", ".join(parts)


def graph_to_dot_string(graph: nx.DiGraph):

    lines = [f"strict digraph {{"]
    lines.append('\tgraph [rankdir=TB, nodesep=0.5, ranksep=0.7, bgcolor=white];')
    lines.append('\tnode [shape=box, style="rounded,filled",'
                 ' fontname="Arial", fontsize=12, penwidth=1.5];')
    lines.append('\tedge [arrowsize=0.8, penwidth=1.5, fontname="Arial", fontsize=10];')
    lines.append('')

    for node, data in graph.nodes(data=True):
        label = _dot_quote(str(data.get("label", node)))
        style = _node_style(data)
        lines.append(f"\t{node} [label={label}, {style}];")

    lines.append('')
    for u, v, data in graph.edges(data=True):
        style = _edge_style(data)
        lines.append(f"\t{u} -> {v} [{style}];")

    lines.append("}")
    return "\n".join(lines)


def write_to_dot(og_graph, filename, output_png=False):
    with open(filename, "w", encoding="utf-8") as fh:
        fh.write(graph_to_dot_string(og_graph))
    if output_png:
        try:
            check_call(
                ["dot", "-Tpng", filename, "-o", filename.rsplit(".", 1)[0] + ".png"]
            )
        except FileNotFoundError:
            print(f"'dot' command not found: {filename}")
