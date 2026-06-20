# codegrapher

Parse source code into AST, DFG, or combined graphs for downstream analysis (ML, code review, static analysis).

Supports **Python, Java, C, C++, C#** via [tree-sitter](https://tree-sitter.github.io/).

## Install

```bash
pip install -e .
```

Requires Python 3.8+. Pulls in `tree-sitter`, `tree-sitter-language-pack`, and `networkx`. For PNG rendering you also need [Graphviz](https://graphviz.org/) installed system-wide (provides the `dot` binary).

## CLI

```bash
codegrapher path/to/source.py \
    --lang python \
    --mode ast+dfg \
    --output dot \
    --out-file out.dot \
    --png
```

| Flag | Values | Notes |
|---|---|---|
| `--lang` | `c`, `cpp`, `python`, `java`, `cs` | Required |
| `--mode` | `ast`, `dfg`, `ast+dfg` | Required. `ast+dfg` overlays DFG edges onto the AST graph |
| `--output` | `dot`, `json` | Required |
| `--out-file` | path | Required |
| `--preprocess` | flag | Strip comments and empty lines before parsing |
| `--skip-comments` | flag | Drop comment nodes from the AST |
| `--png` | flag | Also render a PNG (requires `dot` on PATH) |

## Python API

```python
from codegrapher import ASTDriver, DFGDriver, CombinedDriver, get_language_map

lang_map = get_language_map()
language = lang_map["python"]

# Single-mode
ast = ASTDriver(language, "python").parse(source)

# Combined AST + DFG (DFG edges overlay onto AST nodes — no duplicate nodes)
combined = CombinedDriver(
    language, "python", components=["ast", "dfg"]
).parse(source)
```

All drivers return a `networkx.DiGraph`. Nodes carry `type`, `label`, `start`, `end`, `is_leaf`, `depth`, and `subtree_size`. Edges carry `edge_type` (`ast_child`, `dfg_comesFrom`, `dfg_computedFrom`) and a short `label`.

## Output formats

- **DOT**: human-readable graph description; color-coded by edge kind. Render to PNG/SVG with Graphviz.
- **JSON**: NetworkX node-link format; consume directly from any language with a JSON parser.

## License

[MIT](LICENSE).
