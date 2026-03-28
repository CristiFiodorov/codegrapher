import networkx as nx

from .base_driver import BaseDriver
from .ast_driver import ASTDriver
from .dfg_driver import DFGDriver

_DRIVER_CLASSES = {
    "ast": ASTDriver,
    "dfg": DFGDriver,
}

_COMPONENT_ORDER = ["ast", "dfg"]

_CROSS_EDGE_TYPES = {
    ("dfg", "ast"): "dfg_to_ast",
}


class CombinedDriver(BaseDriver):
    def __init__(self, language, lang_name: str, components: list[str]):
        super().__init__(language, lang_name)

        unknown = set(components) - _DRIVER_CLASSES.keys()

        if unknown:
            raise ValueError(f"Unknown graph components: {unknown}")
        
        self._components = [c for c in _COMPONENT_ORDER if c in set(components)]
        
        self._sub_drivers = {
            name: _DRIVER_CLASSES[name](language, lang_name)
            for name in self._components
        }

    def parse(self, source: str, preprocess: bool = True):
        self._graph = nx.DiGraph()
        self._counter = 0

        graphs = {
            name: driver.parse(source, preprocess)
            for name, driver in self._sub_drivers.items()
        }
        self._merge(graphs)
        return self._graph

    def _build_graph(self, tree_root):
        pass

    def _merge(self, graphs: dict[str, nx.DiGraph]):
        for name, g in graphs.items():
            for nid, data in g.nodes(data=True):
                self._graph.add_node(f"{name}_{nid}", **data, graph_type=name)
            for u, v, data in g.edges(data=True):
                self._graph.add_edge(f"{name}_{u}", f"{name}_{v}", **data)
        self._add_cross_edges(graphs)

    def _add_cross_edges(self, graphs: dict[str, nx.DiGraph]):
        """Add directed cross-edges between sub-graphs by matching (start, end) position."""

        # Build position index per graph: (start, end) -> prefixed node id
        pos_index = {}
        for name, g in graphs.items():
            idx = {}
            for nid, data in g.nodes(data=True):
                start = data.get("start")
                end = data.get("end")
                if start is not None and end is not None:
                    idx[(start, end)] = f"{name}_{nid}"
            pos_index[name] = idx

        for (src, tgt), edge_type in _CROSS_EDGE_TYPES.items():
            if src not in graphs or tgt not in graphs:
                continue
            for nid, data in graphs[src].nodes(data=True):
                start = data.get("start")
                end = data.get("end")
                if start is None or end is None:
                    continue
                tgt_nid = pos_index[tgt].get((start, end))
                if tgt_nid is not None:
                    self._graph.add_edge(f"{src}_{nid}", tgt_nid, edge_type=edge_type, label="ref")
