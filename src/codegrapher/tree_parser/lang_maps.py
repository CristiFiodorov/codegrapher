SKIP_NODE_TYPES = {
    "c":      frozenset({"primitive_type", "type_identifier", "sized_type_specifier"}),
    "cpp":    frozenset({"primitive_type", "type_identifier", "sized_type_specifier",
                         "qualified_identifier", "template_type"}),
    "python": frozenset(),
    "java":   frozenset({"integral_type", "floating_point_type", "boolean_type",
                         "void_type", "type_identifier", "generic_type"}),
    "cs":     frozenset({"predefined_type", "void_keyword", "identifier_name"}),
}

DO_FIRST_TYPES = {
    "c":      frozenset(),
    "cpp":    frozenset(),
    "python": frozenset({"for_in_clause"}),
    "java":   frozenset(),
    "cs":     frozenset(),
}

DEF_TYPES = {
    "c":      frozenset({"init_declarator"}),
    "cpp":    frozenset({"init_declarator"}),
    "python": frozenset({"default_parameter"}),
    "java":   frozenset({"variable_declarator"}),
    "cs":     frozenset({"variable_declarator"}),
}

ASSIGNMENT_TYPES = {
    "c":      frozenset({"assignment_expression"}),
    "cpp":    frozenset({"assignment_expression"}),
    "python": frozenset({"assignment", "augmented_assignment", "for_in_clause"}),
    "java":   frozenset({"assignment_expression"}),
    "cs":     frozenset({"assignment_expression"}),
}

AUGMENTED_ASSIGNMENT_TYPES = {
    "c":      frozenset(),
    "cpp":    frozenset(),
    "python": frozenset({"augmented_assignment"}),
    "java":   frozenset(),
    "cs":     frozenset(),
}

INCREMENT_TYPES = {
    "c":      frozenset({"update_expression"}),
    "cpp":    frozenset({"update_expression"}),
    "python": frozenset(),
    "java":   frozenset({"update_expression"}),
    "cs":     frozenset({"postfix_unary_expression"}),
}

IF_TYPES = {
    "c":      frozenset({"if_statement"}),
    "cpp":    frozenset({"if_statement"}),
    "python": frozenset({"if_statement"}),
    "java":   frozenset({"if_statement"}),
    "cs":     frozenset({"if_statement"}),
}

ELSE_TYPES = {
    "c":      frozenset({"else_clause"}),
    "cpp":    frozenset({"else_clause"}),
    "python": frozenset({"elif_clause", "else_clause"}),
    "java":   frozenset({"else"}),
    "cs":     frozenset({"else_clause"}),
}

FOR_TYPES = {
    "c":      frozenset({"for_statement"}),
    "cpp":    frozenset({"for_statement"}),
    "python": frozenset(),
    "java":   frozenset({"for_statement"}),
    "cs":     frozenset({"for_statement"}),
}

FOREACH_TYPES = {
    "c":      frozenset(),
    "cpp":    frozenset({"for_range_loop"}),
    "python": frozenset({"for_statement"}),
    "java":   frozenset({"enhanced_for_statement"}),
    "cs":     frozenset({"for_each_statement"}),
}

WHILE_TYPES = {
    "c":      frozenset({"while_statement"}),
    "cpp":    frozenset({"while_statement"}),
    "python": frozenset({"while_statement"}),
    "java":   frozenset({"while_statement"}),
    "cs":     frozenset({"while_statement"}),
}

DO_WHILE_TYPES = {
    "c":      frozenset({"do_statement"}),
    "cpp":    frozenset({"do_statement"}),
    "python": frozenset(),
    "java":   frozenset({"do_statement"}),
    "cs":     frozenset({"do_statement"}),
}

SWITCH_TYPES = {
    "c":      frozenset({"switch_statement"}),
    "cpp":    frozenset({"switch_statement"}),
    "python": frozenset({"match_statement"}),
    "java":   frozenset({"switch_expression", "switch_statement"}),
    "cs":     frozenset({"switch_statement"}),
}

CASE_CLAUSE_TYPES = {
    "c":      frozenset({"case_statement"}),
    "cpp":    frozenset({"case_statement"}),
    "python": frozenset({"case_clause"}),
    "java":   frozenset({"switch_block_statement_group"}),
    "cs":     frozenset({"switch_section"}),
}

FUNCTION_TYPES = {
    "c":      frozenset({"function_definition"}),
    "cpp":    frozenset({"function_definition"}),
    "python": frozenset({"function_definition"}),
    "java":   frozenset({"method_declaration", "constructor_declaration"}),
    "cs":     frozenset({"method_declaration", "constructor_declaration"}),
}

CALL_EXPRESSION_TYPES = {
    "c":      frozenset({"call_expression"}),
    "cpp":    frozenset({"call_expression"}),
    "python": frozenset({"call"}),
    "java":   frozenset({"method_invocation"}),
    "cs":     frozenset({"invocation_expression"}),
}

FUNCTION_PARAMETER_TYPES = {
    "c":      frozenset({"parameter_declaration"}),
    "cpp":    frozenset({"parameter_declaration"}),
    "python": frozenset({"identifier", "typed_parameter", "default_parameter",
                         "list_splat_pattern", "dictionary_splat_pattern"}),
    "java":   frozenset({"formal_parameter", "spread_parameter"}),
    "cs":     frozenset({"parameter"}),
}

