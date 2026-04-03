# From tree sitter type to canocical
_COMMON = {
    # --- functions / methods ---
    "function_definition":       "function_def",
    "method_declaration":        "function_def",
    "constructor_declaration":   "constructor_def",
    "constructor_body":          "block",
    "lambda_expression":         "lambda",
    "lambda":                    "lambda",

    # --- classes / structs ---
    "class_definition":          "class_def",
    "class_specifier":           "class_def",
    "class_declaration":         "class_def",
    "struct_specifier":          "struct_def",
    "struct_declaration":        "struct_def",
    "interface_declaration":     "interface_def",
    "enum_declaration":          "enum_def",
    "enum_specifier":            "enum_def",

    # --- control flow ---
    "if_statement":              "if",
    "elif_clause":               "elif",
    "else_if_clause":            "elif",
    "if_clause":                 "if",
    "case_switch_label":         "case",
    "switch_label":              "case",
    "while_statement":           "while",
    "do_statement":              "do_while",
    "for_range_loop":            "foreach",
    "enhanced_for_statement":    "foreach",
    "for_each_statement":        "foreach",
    "for_in_clause":             "foreach",
    "switch_statement":          "switch",
    "switch_expression":         "switch",
    "match_statement":           "switch",
    "case_statement":            "case",
    "case_clause":               "case",
    "switch_block_statement_group": "case",
    "switch_section":            "case",
    "try_statement":             "try",
    "try_with_resources_statement": "try",
    "except_clause":             "catch",
    "catch_clause":              "catch",
    "finally_clause":            "finally",
    "with_statement":            "with",
    "using_statement":           "with",
    "lock_statement":            "with",
    "synchronized_statement":    "with",
    "using_directive":           "import",
    "import_statement":          "import",
    "import_from_statement":     "import",

    # --- jumps ---
    "return_statement":          "return",
    "break_statement":           "break",
    "continue_statement":        "continue",
    "raise_statement":           "throw",
    "throw_statement":           "throw",
    "goto_statement":            "goto",
    "labeled_statement":         "label",
    "yield":                     "return",
    "yield_statement":           "return",

    # --- blocks ---
    "compound_statement":        "block",
    "block":                     "block",
    "class_body":                "block",
    "switch_body":               "block",
    "switch_block":              "block",
    "field_declaration_list":    "block",
    "declaration_list":          "block",
    "expression_statement":      "expr_stmt",
    "parenthesized_expression":  "condition",
    "local_declaration_statement": "assignment",
    "condition_clause":          "condition",
    "declaration":               "assignment",
    "local_variable_declaration": "assignment",
    "variable_declaration":      "assignment",
    "field_declaration":         "assignment",
    "catch_declaration":         "assignment",

    # --- initializers ---
    "array_initializer":         "initializer",
    "initializer_expression":    "initializer",
    "initializer_list":          "initializer",
    "object_creation_expression": "new_expr",
    "object_creation":           "new_expr",

    # --- expressions ---
    "binary_expression":         "binary_expr",
    "binary_operator":           "binary_expr",
    "comparison_operator":       "binary_expr",
    "boolean_operator":          "binary_expr",
    "unary_expression":          "unary_expr",
    "unary_operator":            "unary_expr",
    "not_operator":              "unary_expr",
    "update_expression":         "update_expr",
    "postfix_unary_expression":  "update_expr",
    "prefix_unary_expression":   "update_expr",
    "assignment_expression":     "assignment",
    "assignment":                "assignment",
    "augmented_assignment":      "assignment",
    "conditional_expression":    "ternary",
    "call_expression":           "call",
    "call":                      "call",
    "method_invocation":         "call",
    "invocation_expression":     "call",
    "member_expression":         "member_access",
    "member_access_expression":  "member_access",
    "conditional_access_expression": "member_access",
    "attribute":                 "member_access",
    "field_expression":          "member_access",
    "field_access":              "member_access",
    "dotted_name":               "member_access",
    "subscript_expression":      "index",
    "element_access_expression": "index",
    "array_access":              "index",
    "subscript":                 "index",

    # --- C++ generics / templates ---
    "template_argument_list":    "argument_list",
    "subscript_argument_list":   "argument_list",

    # --- C++ misc ---
    "preproc_include":           "import",
    "cast_expression":           "unary_expr",

    # --- Python pattern matching ---
    "case_pattern":              "pattern",
    "dict_pattern":              "pattern",
    "as_pattern":                "pattern",
    "pattern_list":              "pattern",

    # --- identifiers ---
    "identifier":                "identifier",
    "field_identifier":          "identifier",
    "true":                      "identifier",
    "false":                     "identifier",
    "null_literal":              "identifier",
    "none":                      "identifier",
    "null":                      "identifier",
    "None":                      "identifier",
    "True":                      "identifier",
    "False":                     "identifier",

    # --- access modifiers ---
    "modifiers":                 "modifier",
    "modifier":                  "modifier",

    # --- literals ---
    "number_literal":            "literal",
    "integer":                   "literal",
    "float":                     "literal",
    "decimal_integer_literal":   "literal",
    "hex_integer_literal":       "literal",
    "octal_integer_literal":     "literal",
    "integer_literal":           "literal",
    "real_literal":              "literal",
    "decimal_floating_point_literal": "literal",
    "string_literal":            "literal",
    "string":                    "literal",
    "concatenated_string":       "literal",
    "string_content":            "literal",
    "interpolated_string_expression": "literal",
    "character_literal":         "literal",
    "char_literal":              "literal",

    # --- parameters / arguments ---
    "parameters":                "params",
    "parameter_list":            "params",
    "formal_parameters":         "params",
    "spread_parameter":          "param",
    "argument_list":             "argument_list",
    "bracketed_argument_list":   "argument_list",

    # --- any ---
    "module":                    "module",
    "translation_unit":          "module",
    "program":                   "module",
    "compilation_unit":          "module",
}


_LANG_OVERRIDES: dict[str, dict[str, str]] = {
    # Python for_statement is a foreach
    "python": {"for_statement": "foreach"},
    # C/C++/Java/C#
    "c":    {"for_statement": "for"},
    "cpp":  {"for_statement": "for"},
    "java": {"for_statement": "for"},
    "cs":   {"for_statement": "for"},
}


_COMMENT_TYPES = frozenset({"comment", "line_comment", "block_comment"})

AST_SKIP_TYPES: dict[str, frozenset] = {
    "c":      frozenset({
                  "primitive_type", "type_identifier", "sized_type_specifier",
              }) | _COMMENT_TYPES,
    "cpp":    frozenset({
                  "primitive_type", "type_identifier", "sized_type_specifier",
                  "template_type", "qualified_identifier",
                  "access_specifier",
                  "storage_class_specifier", "type_qualifier",
              }) | _COMMENT_TYPES,
    "python": frozenset({"string_start", "string_end", "pass_statement"}) | _COMMENT_TYPES,
    "java":   frozenset({
                  "integral_type", "floating_point_type", "boolean_type",
                  "void_type", "type_identifier", "generic_type", "array_type",
                  "scoped_type_identifier", "catch_type",
                  "modifiers",
              }) | _COMMENT_TYPES,
    "cs":     frozenset({
                  "predefined_type", "void_keyword", "nullable_type",
                  "array_type", "identifier_name",
                  "scoped_type_identifier", "implicit_type",
                  "assignment_operator",
                  "modifier",
              }) | _COMMENT_TYPES,
}

# This nodes are skiped and its named children are directly attach to the parent node
AST_TRANSPARENT_TYPES: dict[str, frozenset] = {
    "c":      frozenset({
                  "pointer_declarator",
                  "array_declarator",
                  "function_declarator",
                  "parameter_declaration",
                  "type_descriptor",
                  "parenthesized_expression",
                  "init_declarator",
                  "else_clause",
                  "expression_statement",
              }),
    "cpp":    frozenset({
                  "pointer_declarator",
                  "reference_declarator",
                  "array_declarator",
                  "function_declarator",
                  "parameter_declaration",
                  "type_descriptor",
                  "condition_clause",
                  "qualified_identifier",
                  "parenthesized_expression",
                  "init_declarator",
                  "else_clause",
                  "expression_statement",
              }),
    "python": frozenset({
                  "with_clause",
                  "with_item",
                  "expression_list",
                  "else_clause",
                  "list_comprehension",
                  "set_comprehension",
                  "dict_comprehension",
                  "generator_expression",
                  "expression_statement",
              }),
    "java":   frozenset({
                  "parenthesized_expression",
                  "variable_declarator",
                  "resource_specification",
                  "resource",
                  "catch_formal_parameter",
                  "expression_statement",
                  "equals_value_clause",
                  "formal_parameter",
                  "argument",
              }),
    "cs":     frozenset({
                  "parenthesized_expression",
                  "variable_declarator",
                  "local_declaration_statement",
                  "member_binding_expression",
                  "expression_statement",
                  "equals_value_clause",
                  "parameter",
                  "argument",
              }),
}

def normalize_type(lang: str, ts_type: str) -> str:
    overrides = _LANG_OVERRIDES.get(lang, {})
    if ts_type in overrides:
        return overrides[ts_type]
    return _COMMON.get(ts_type, ts_type)
