import argparse
import sys

from utils.language import get_language_map
from utils.postprocessor import write_networkx_to_json, write_to_dot
from tree_parser import ASTDriver, DFGDriver


DRIVER_MAP = {"ast": ASTDriver, "dfg": DFGDriver}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="codegrapher",
        description="Parse source code into AST or DFG graphs"
    )
    p.add_argument(
        "source_file"
    )
    p.add_argument(
        "--lang",
        required=True,
        choices=["c", "cpp", "python", "java", "cs"],
        help="Language of the source file"
    )
    p.add_argument(
        "--mode",
        required=True,
        choices=DRIVER_MAP.keys(),
        help="Graph type to generate"
    )
    p.add_argument(
        "--output",
        required=True,
        choices=["dot", "json"]
    )
    p.add_argument(
        "--out-file",
        required=True
    )
    p.add_argument(
        "--preprocess",
        action="store_true",
        help="Strip comments and empty lines before parsing"
    )
    p.add_argument(
        "--png",
        action="store_true",
        help="Render a PNG"
    )
    return p


def main():
    parser = build_parser()
    args = parser.parse_args()

    with open(args.source_file, "r", encoding="utf-8") as fh:
        source = fh.read()

    lang_map = get_language_map()
    language = lang_map[args.lang]

    DriverClass = DRIVER_MAP[args.mode]
    driver = DriverClass(language, args.lang)
    graph = driver.parse(source, preprocess=args.preprocess)

    if args.output == "dot":
        write_to_dot(graph, args.out_file, output_png=args.png)
        print(f"DOT written to {args.out_file}", file=sys.stderr)
        if args.png:
            png_path = args.out_file.rsplit(".", 1)[0] + ".png"
            print(f"PNG written to {png_path}", file=sys.stderr)
    else:
        write_networkx_to_json(graph, args.out_file)
        print(f"JSON written to {args.out_file}", file=sys.stderr)


if __name__ == "__main__":
    main()
