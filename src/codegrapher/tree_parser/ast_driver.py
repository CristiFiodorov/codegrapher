import networkx as nx

from .base_driver import BaseDriver
from .normalize_map import (
    AST_SKIP_TYPES,
    AST_TRANSPARENT_TYPES,
    AST_UNIVERSAL_SKIP_TYPES,
    COMMENT_TYPES,
)


class ASTDriver(BaseDriver):
    def __init__(self, language, lang_name: str, normalize: bool = False, skip_comments: bool = False) -> None:
        super().__init__(language, lang_name, normalize=normalize, skip_comments=skip_comments)
        self._normalize_labels = normalize

    def _build_graph(self, tree_root):
        self._visit(tree_root, parent_id=None, depth=0, child_index=0)
        self._compute_subtree_sizes()

    def _visit(self, ts_node, parent_id, depth, child_index):
        if not ts_node.is_named:
            return

        if (self._skip_comments or self._normalize) and ts_node.type in COMMENT_TYPES:
            return

        if self._normalize:
            if ts_node.type in AST_UNIVERSAL_SKIP_TYPES:
                return

            if ts_node.type in AST_SKIP_TYPES.get(self._lang_name, frozenset()):
                return

            transparent = AST_TRANSPARENT_TYPES.get(self._lang_name, frozenset())
            if ts_node.type in transparent:
                named_idx = 0
                for child in ts_node.children:
                    if child.is_named:
                        self._visit(child, parent_id=parent_id, depth=depth, child_index=child_index + named_idx)
                        named_idx += 1
                    else:
                        self._visit(child, parent_id=parent_id, depth=depth, child_index=child_index + named_idx)
                return

        nid = self._next_id()
        named_children = [c for c in ts_node.children if c.is_named]
        is_leaf = len(named_children) == 0

        if is_leaf:
            raw = ts_node.text.decode("utf-8", errors="replace")
            label = self._sanitize_label(raw)
        else:
            label = ts_node.type

        self._graph.add_node(
            nid,
            type=ts_node.type,
            label=label,
            start="{0}_{1}".format(*ts_node.start_point),
            end="{0}_{1}".format(*ts_node.end_point),
            is_leaf=is_leaf,
            depth=depth,
            child_index=child_index,
        )

        if parent_id is not None:
            self._graph.add_edge(parent_id, nid, edge_type="ast_child", label="")

        named_idx = 0
        for child in ts_node.children:
            if child.is_named:
                self._visit(child, parent_id=nid, depth=depth + 1, child_index=named_idx)
                named_idx += 1
            else:
                self._visit(child, parent_id=nid, depth=depth + 1, child_index=named_idx)

    def _compute_subtree_sizes(self):
        for nid in reversed(list(nx.topological_sort(self._graph))):
            children = list(self._graph.successors(nid))
            size = 1 + sum(self._graph.nodes[c].get("subtree_size", 1) for c in children)
            self._graph.nodes[nid]["subtree_size"] = size
