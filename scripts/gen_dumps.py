import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from utils.language import get_language_map
from tree_sitter import Parser


STATEMENTS = {}

STATEMENTS["if"] = {
    "c": b"""void f() {
    if (x > 0) {
        a = 1;
    } else if (x == 0) {
        a = 2;
    } else {
        a = 3;
    }
}
""",
    "cpp": b"""void f() {
    if (x > 0) {
        a = 1;
    } else if (x == 0) {
        a = 2;
    } else {
        a = 3;
    }
}
""",
    "python": b"""def f():
    if x > 0:
        a = 1
    elif x == 0:
        a = 2
    else:
        a = 3
""",
    "java": b"""class Main {
    void f() {
        if (x > 0) {
            a = 1;
        } else if (x == 0) {
            a = 2;
        } else {
            a = 3;
        }
    }
}
""",
    "cs": b"""class Main {
    void f() {
        if (x > 0) {
            a = 1;
        } else if (x == 0) {
            a = 2;
        } else {
            a = 3;
        }
    }
}
""",
}

STATEMENTS["while"] = {
    "c": b"""void f() {
    while (x < 10) {
        x = x + 1;
    }
}
""",
    "cpp": b"""void f() {
    while (x < 10) {
        x = x + 1;
    }
}
""",
    "python": b"""def f():
    while x < 10:
        x = x + 1
""",
    "java": b"""class Main {
    void f() {
        while (x < 10) {
            x = x + 1;
        }
    }
}
""",
    "cs": b"""class Main {
    void f() {
        while (x < 10) {
            x = x + 1;
        }
    }
}
""",
}

STATEMENTS["for"] = {
    "c": b"""void f() {
    for (int i = 0; i < 10; i++) {
        x = x + 1;
    }
}
""",
    "cpp": b"""void f() {
    for (int i = 0; i < 10; i++) {
        x = x + 1;
    }
}
""",
    "python": None,
    "java": b"""class Main {
    void f() {
        for (int i = 0; i < 10; i++) {
            x = x + 1;
        }
    }
}
""",
    "cs": b"""class Main {
    void f() {
        for (int i = 0; i < 10; i++) {
            x = x + 1;
        }
    }
}
""",
}

STATEMENTS["foreach"] = {
    "c": None,
    "cpp": b"""void f() {
    for (auto& item : vec) {
        process(item);
    }
}
""",
    "python": b"""def f():
    for item in data:
        process(item)
""",
    "java": b"""class Main {
    void f() {
        for (String item : list) {
            process(item);
        }
    }
}
""",
    "cs": b"""class Main {
    void f() {
        foreach (var item in list) {
            process(item);
        }
    }
}
""",
}

STATEMENTS["do_while"] = {
    "c": b"""void f() {
    do {
        x = x + 1;
    } while (x < 10);
}
""",
    "cpp": b"""void f() {
    do {
        x = x + 1;
    } while (x < 10);
}
""",
    "python": None,
    "java": b"""class Main {
    void f() {
        do {
            x = x + 1;
        } while (x < 10);
    }
}
""",
    "cs": b"""class Main {
    void f() {
        do {
            x = x + 1;
        } while (x < 10);
    }
}
""",
}

STATEMENTS["return"] = {
    "c": b"""int f() {
    return 42;
}
""",
    "cpp": b"""int f() {
    return 42;
}
""",
    "python": b"""def f():
    return 42
""",
    "java": b"""class Main {
    int f() {
        return 42;
    }
}
""",
    "cs": b"""class Main {
    int f() {
        return 42;
    }
}
""",
}

STATEMENTS["break"] = {
    "c": b"""void f() {
    while (1) {
        break;
    }
}
""",
    "cpp": b"""void f() {
    while (true) {
        break;
    }
}
""",
    "python": b"""def f():
    while True:
        break
""",
    "java": b"""class Main {
    void f() {
        while (true) {
            break;
        }
    }
}
""",
    "cs": b"""class Main {
    void f() {
        while (true) {
            break;
        }
    }
}
""",
}

STATEMENTS["continue"] = {
    "c": b"""void f() {
    while (1) {
        continue;
    }
}
""",
    "cpp": b"""void f() {
    while (true) {
        continue;
    }
}
""",
    "python": b"""def f():
    while True:
        continue
""",
    "java": b"""class Main {
    void f() {
        while (true) {
            continue;
        }
    }
}
""",
    "cs": b"""class Main {
    void f() {
        while (true) {
            continue;
        }
    }
}
""",
}

STATEMENTS["switch"] = {
    "c": b"""void f() {
    switch (x) {
        case 1:
            a = 1;
            break;
        case 2:
            a = 2;
            break;
        default:
            a = 0;
            break;
    }
}
""",
    "cpp": b"""void f() {
    switch (x) {
        case 1:
            a = 1;
            break;
        case 2:
            a = 2;
            break;
        default:
            a = 0;
            break;
    }
}
""",
    "python": b"""def f():
    match x:
        case 1:
            a = 1
        case 2:
            a = 2
        case _:
            a = 0
""",
    "java": b"""class Main {
    void f() {
        switch (x) {
            case 1:
                a = 1;
                break;
            case 2:
                a = 2;
                break;
            default:
                a = 0;
                break;
        }
    }
}
""",
    "cs": b"""class Main {
    void f() {
        switch (x) {
            case 1:
                a = 1;
                break;
            case 2:
                a = 2;
                break;
            default:
                a = 0;
                break;
        }
    }
}
""",
}

STATEMENTS["try"] = {
    "c": None,
    "cpp": b"""void f() {
    try {
        x = 1;
    } catch (int e) {
        x = 0;
    }
}
""",
    "python": b"""def f():
    try:
        x = 1
    except ValueError:
        x = 0
    finally:
        cleanup()
""",
    "java": b"""class Main {
    void f() {
        try {
            x = 1;
        } catch (Exception e) {
            x = 0;
        } finally {
            cleanup();
        }
    }
}
""",
    "cs": b"""class Main {
    void f() {
        try {
            x = 1;
        } catch (Exception e) {
            x = 0;
        } finally {
            cleanup();
        }
    }
}
""",
}

STATEMENTS["raise"] = {
    "c": None,
    "cpp": b"""void f() {
    throw 42;
}
""",
    "python": b"""def f():
    raise ValueError("error")
""",
    "java": b"""class Main {
    void f() {
        throw new RuntimeException("error");
    }
}
""",
    "cs": b"""class Main {
    void f() {
        throw new Exception("error");
    }
}
""",
}

STATEMENTS["goto"] = {
    "c": b"""void f() {
    goto done;
    x = 1;
done:
    y = 2;
}
""",
    "cpp": b"""void f() {
    goto done;
    x = 1;
done:
    y = 2;
}
""",
    "python": None,
    "java": None,
    "cs": b"""class Main {
    void f() {
        goto done;
        x = 1;
    done:
        y = 2;
    }
}
""",
}

STATEMENTS["labels"] = {
    "c": b"""void f() {
start:
    x = 1;
}
""",
    "cpp": b"""void f() {
start:
    x = 1;
}
""",
    "python": None,
    "java": b"""class Main {
    void f() {
        outer:
        for (int i = 0; i < 10; i++) {
            break outer;
        }
    }
}
""",
    "cs": b"""class Main {
    void f() {
    start:
        x = 1;
    }
}
""",
}

STATEMENTS["function"] = {
    "c": b"""int add(int a, int b) {
    return a + b;
}
""",
    "cpp": b"""int add(int a, int b) {
    return a + b;
}
""",
    "python": b"""def add(a, b):
    return a + b
""",
    "java": b"""class Main {
    int add(int a, int b) {
        return a + b;
    }
}
""",
    "cs": b"""class Main {
    int add(int a, int b) {
        return a + b;
    }
}
""",
}

STATEMENTS["call"] = {
    "c": b"""int x = add(a, b);
""",
    "cpp": b"""int x = add(a, b);
""",
    "python": b"""x = add(a, b)
""",
    "java": b"""int x = add(a, b);
""",
    "cs": b"""int x = add(a, b);
""",
}

langs = get_language_map()


def dump(node, indent=0, field_name=None):
    prefix = "  " * indent
    field_prefix = f"{field_name}: " if field_name else ""
    if node.is_named:
        text = ""
        if node.child_count == 0:
            text = " '" + node.text.decode("utf-8", errors="replace") + "'"
        line = f"{prefix}{field_prefix}{node.type}{text}"
    else:
        text = node.text.decode("utf-8", errors="replace")
        line = f"{prefix}{field_prefix}{node.type} '{text}'"
    lines = [line]
    for i, child in enumerate(node.children):
        lines.extend(dump(child, indent + 1, node.field_name_for_child(i)))
    return lines


def parse_and_dump(lang_name, source_bytes):
    parser = Parser()
    parser.set_language(langs[lang_name])
    tree = parser.parse(source_bytes)
    return dump(tree.root_node)


def main():
    out_dir = "dumps"
    os.makedirs(out_dir, exist_ok=True)

    for stmt_name, lang_sources in STATEMENTS.items():
        path = os.path.join(out_dir, f"{stmt_name}.txt")

        with open(path, "w", encoding="utf-8") as f:
            for lang_name in ["c", "cpp", "python", "java", "cs"]:
                src = lang_sources.get(lang_name)

                if src is None:
                    continue

                f.write(f"=== {lang_name.upper()} ===\n")
                f.write("--- source ---\n")
                f.write(src.decode("utf-8"))
                f.write("--- tree ---\n")
                tree_lines = parse_and_dump(lang_name, src)
                f.write("\n".join(tree_lines))
                f.write("\n\n")

        print(f"  wrote {path}")

    print("Done.")

if __name__ == "__main__":
    main()
