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


# AST style
_AST_FILL    = "#d4edda"   # light green
_AST_BORDER  = "#5a9a6e"   # dark green
_AST_EDGE    = "#2e7d32"   # green

# DFG style
_DFG_FILL    = "#cfe2f3"   # light blue
_DFG_BORDER  = "#1565c0"   # dark blue
_DFG_COMES   = "#1565c0"   # blue  (comesFrom)
_DFG_COMPUTED= "#6a1b9a"   # purple (computedFrom)

# Combined graph
_CROSS_EDGE  = "#e67e22"   # orange


def _detect_graph_kind(graph: nx.DiGraph):
    for _, data in graph.nodes(data=True):
        if "graph_type" in data:
            return "combined"
    for _, _, data in graph.edges(data=True):
        et = data.get("edge_type", "")
        if et == "ast_child":
            return "ast"
        if et.startswith("dfg_"):
            return "dfg"
    return "ast"


def _node_style(data: dict, graph_kind: str):
    gt = data.get("graph_type", "")
    
    if graph_kind == "combined":
        if gt == "ast":
            return f'fillcolor="{_AST_FILL}", color="{_AST_BORDER}"'
        else:
            return f'fillcolor="{_DFG_FILL}", color="{_DFG_BORDER}"'
    elif graph_kind == "dfg":
        return f'fillcolor="{_DFG_FILL}", color="{_DFG_BORDER}"'
    else:
        return f'fillcolor="{_AST_FILL}", color="{_AST_BORDER}"'


def _edge_style(data: dict, graph_kind: str):
    et    = data.get("edge_type", "")
    label = data.get("label", "")

    parts = []

    if et == "dfg_comesFrom":
        parts.append(f'color="{_DFG_COMES}"')
    elif et == "dfg_computedFrom":
        parts.append(f'color="{_DFG_COMPUTED}", style=dashed')
    elif et == "ast_child":
        parts.append(f'color="{_AST_EDGE}"')
    elif et == "dfg_to_ast":
        parts.append(f'color="{_CROSS_EDGE}", style=dashed')
    else:
        if graph_kind == "dfg":
            parts.append(f'color="{_DFG_COMES}"')
        else:
            parts.append(f'color="{_AST_EDGE}"')

    if label:
        parts.append(f'label={_dot_quote(label)}')

    return ", ".join(parts)


def graph_to_dot_string(graph: nx.DiGraph):
    kind = _detect_graph_kind(graph)

    lines = [f"strict digraph {{"]
    lines.append('\tgraph [rankdir=TB, nodesep=0.5, ranksep=0.7, bgcolor=white];')
    lines.append('\tnode [shape=box, style="rounded,filled",'
                 ' fontname="Arial", fontsize=12, penwidth=1.5];')
    lines.append('\tedge [arrowsize=0.8, penwidth=1.5, fontname="Arial", fontsize=10];')
    lines.append('')

    for node, data in graph.nodes(data=True):
        label = _dot_quote(str(data.get("label", node)))
        style = _node_style(data, kind)
        lines.append(f"\t{node} [label={label}, {style}];")

    lines.append('')
    for u, v, data in graph.edges(data=True):
        style = _edge_style(data, kind)
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
