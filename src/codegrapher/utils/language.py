from tree_sitter_language_pack import get_language


def get_language_map():
    return {
        "java":   get_language("java"),
        "cs":     get_language("csharp"),
        "python": get_language("python"),
        "c":      get_language("c"),
        "cpp":    get_language("cpp"),
    }
