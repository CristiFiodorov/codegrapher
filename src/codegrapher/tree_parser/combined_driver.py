from .base_driver import BaseDriver
from .ast_driver import ASTDriver
from .dfg_driver import DFGDriver


class CombinedDriver(BaseDriver):
    """
    Builds an AST graph, then overlays DFG edges directly onto AST leaf nodes.
    No duplicate nodes — DFG edges connect existing AST nodes.
    """

    def __init__(self, language, lang_name: str, components: list[str] = None, normalize: bool = False, skip_comments: bool = False):
        super().__init__(language, lang_name, normalize=normalize, skip_comments=skip_comments)
        self._ast_driver = ASTDriver(language, lang_name, normalize=normalize, skip_comments=skip_comments)
        self._dfg_driver = DFGDriver(language, lang_name, normalize=False)

    def parse(self, source: str, preprocess: bool = True):
        # 1. Build the AST graph (this is our base graph)
        ast_graph = self._ast_driver.parse(source, preprocess)

        # 2. Build position -> AST node ID index from leaf nodes
        pos_to_ast_nid = {}
        for nid, data in ast_graph.nodes(data=True):
            if data.get("is_leaf", False):
                start = data.get("start")
                end = data.get("end")
                if start is not None and end is not None:
                    pos_to_ast_nid[(start, end)] = nid

        # 3. Run DFG extraction on the same (preprocessed) source
        dfg_graph = self._dfg_driver.parse(source, preprocess)

        # 4. Build DFG node ID -> position index
        dfg_id_to_pos = {}
        for nid, data in dfg_graph.nodes(data=True):
            start = data.get("start")
            end = data.get("end")
            if start is not None and end is not None:
                dfg_id_to_pos[nid] = (start, end)

        # 5. Add DFG edges between AST nodes
        for u, v, edata in dfg_graph.edges(data=True):
            u_pos = dfg_id_to_pos.get(u)
            v_pos = dfg_id_to_pos.get(v)
            if u_pos is None or v_pos is None:
                continue
            ast_u = pos_to_ast_nid.get(u_pos)
            ast_v = pos_to_ast_nid.get(v_pos)
            if ast_u is not None and ast_v is not None:
                ast_graph.add_edge(ast_u, ast_v, **edata)

        # 6. Normalize after everything is assembled
        self._graph = ast_graph
        if self._normalize:
            self._normalize_types()

        return self._graph

    def _build_graph(self, tree_root):
        pass
