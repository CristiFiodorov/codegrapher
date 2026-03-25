from abc import ABC, abstractmethod
import networkx as nx
from tree_sitter import Language, Parser

from utils.preprocessor import remove_comments, remove_empty_lines


class BaseDriver(ABC):
    def __init__(self, language: Language, lang_name: str):
        self._language = language
        self._lang_name = lang_name
        self._parser = Parser()
        self._parser.set_language(language)
        self._graph: nx.DiGraph = nx.DiGraph()
        self._counter = 0

    def _next_id(self):
        nid = self._counter
        self._counter += 1
        return nid
    
    def _sanitize_label(self, text: str, max_len: int = 80):
        text = text.replace('"', "'")
        text = text.replace("\n", " ").replace("\r", " ")
        text = text.replace("\\", "/")
        return text[:max_len]

    def parse(self, source: str, preprocess: bool = True):
        self._graph = nx.DiGraph()
        self._counter = 0

        if preprocess:
            source = remove_comments(self._lang_name, source)
            source = remove_empty_lines(source)

        self._source = source
        tree = self._parser.parse(bytes(source, "utf-8"))
        self._build_graph(tree.root_node)

        return self._graph

    @abstractmethod
    def _build_graph(self, tree_root):
        """
        This function should be implemented be subclasses to build graph
        """
        ...
