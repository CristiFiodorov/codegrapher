from .base_driver import BaseDriver
from .normalize_map import AST_SKIP_TYPES, AST_TRANSPARENT_TYPES


class ASTDriver(BaseDriver):
    def __init__(self, language, lang_name: str, normalize: bool = False) -> None:
        super().__init__(language, lang_name, normalize=normalize)
        self._normalize_labels = normalize

    def _build_graph(self, tree_root):
        self._visit(tree_root, parent_id=None)

    def _visit(self, ts_node, parent_id):
        if not ts_node.is_named:
            return
        
        if self._normalize:
            if ts_node.type in AST_SKIP_TYPES.get(self._lang_name, frozenset()):
                return
            
            transparent = AST_TRANSPARENT_TYPES.get(self._lang_name, frozenset())
            if ts_node.type in transparent:
                for child in ts_node.children:
                    self._visit(child, parent_id=parent_id)
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
            is_leaf=is_leaf
        )

        if parent_id is not None:
            self._graph.add_edge(parent_id, nid, edge_type="ast_child", label="")

        for child in ts_node.children:
            self._visit(child, parent_id=nid)
