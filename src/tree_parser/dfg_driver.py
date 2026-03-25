# This code is based on https://github.com/microsoft/CodeBERT/blob/master/GraphCodeBERT/codesearch/parser/DFG.py

from .base_driver import BaseDriver
from . import lang_maps as maps


class DFGDriver(BaseDriver):
    def __init__(self, language, lang_name: str):
        super().__init__(language, lang_name)
        self._index_to_code: dict = {}

    def _build_graph(self, tree_root):
        self._source_lines = self._source.split("\n")

        # Build token position -> (idx, code_text) mapping
        token_positions = self._tree_to_token_index(tree_root)
        self._index_to_code = {}
        for idx, (start, end) in enumerate(token_positions):
            code = self._index_to_code_token(start, end)
            self._index_to_code[(start, end)] = (idx, code)

        dfg_entries, _ = self._extract_dfg(tree_root, {})

        node_set = set()
        for code, idx, rel_type, dep_codes, dep_idxs in dfg_entries:
            if dep_idxs:
                node_set.add(idx)
                node_set.update(dep_idxs)

        # Reverse lookup: idx -> (start, end, code)
        idx_to_pos = {}
        for (start, end), (idx, code) in self._index_to_code.items():
            idx_to_pos[idx] = (start, end, code)

        for idx in sorted(node_set):
            if idx in idx_to_pos:
                start, end, code = idx_to_pos[idx]
                self._graph.add_node(
                    idx,
                    type="identifier",
                    label=self._sanitize_label(code),
                    start=f"{start[0]}_{start[1]}",
                    end=f"{end[0]}_{end[1]}",
                )

        for code, idx, rel_type, dep_codes, dep_idxs in dfg_entries:
            edge_type = f"dfg_{rel_type}"
            for dep_idx in dep_idxs:
                if dep_idx != idx and dep_idx in node_set and idx in node_set:
                    self._graph.add_edge(dep_idx, idx, edge_type=edge_type, label=rel_type)

    def _extract_dfg(self, node, states):
        """
        Recursively extract data flow tuples from the tree

        Returns (dfg_list, updated_states) where each entry is
        (variable_name, token_idx, relationship, [dep_names], [dep_indices])
        """
        states = states.copy()
        lang = self._lang_name

        if (len(node.children) == 0 or node.type == "string") and node.type != "comment":
            return self._handle_leaf(node, states)

        if node.type in maps.DEF_TYPES.get(lang, frozenset()):
            return self._handle_def(node, states)
        
        if node.type in maps.ASSIGNMENT_TYPES.get(lang, frozenset()):
            return self._handle_assignment(node, states)

        if node.type in maps.INCREMENT_TYPES.get(lang, frozenset()):
            return self._handle_increment(node, states)

        if node.type in maps.IF_TYPES.get(lang, frozenset()):
            return self._handle_if(node, states)

        if node.type in maps.FOR_TYPES.get(lang, frozenset()):
            return self._handle_for(node, states)

        if node.type in maps.FOREACH_TYPES.get(lang, frozenset()):
            return self._handle_foreach(node, states)

        if node.type in maps.WHILE_TYPES.get(lang, frozenset()):
            return self._handle_while(node, states)

        do_first_types = maps.DO_FIRST_TYPES.get(lang, frozenset())
        return self._handle_default(node, states, do_first_types)

    def _handle_leaf(self, node, states):
        pos = (node.start_point, node.end_point)
        if pos not in self._index_to_code:
            return [], states
        idx, code = self._index_to_code[pos]

        if node.type == code:
            return [], states

        skip_types = maps.SKIP_NODE_TYPES.get(self._lang_name, frozenset())
        if node.type in skip_types:
            return [], states

        if code in states:
            return [(code, idx, "comesFrom", [code], states[code].copy())], states

        if node.type == "identifier":
            states[code] = [idx]

        return [(code, idx, "comesFrom", [], [])], states

    def _handle_def(self, node, states):
        name, value = self._get_def_name_value(node)
        if name is None:
            return [], states

        DFG = []
        if value is None:
            for index in self._tree_to_variable_index(name):
                idx, code = self._index_to_code[index]
                DFG.append((code, idx, "comesFrom", [], []))
                states[code] = [idx]
        else:
            name_indexs = self._tree_to_variable_index(name)
            value_indexs = self._tree_to_variable_index(value)
            temp, states = self._extract_dfg(value, states)
            DFG += temp
            for index1 in name_indexs:
                idx1, code1 = self._index_to_code[index1]
                for index2 in value_indexs:
                    idx2, code2 = self._index_to_code[index2]
                    DFG.append((code1, idx1, "computedFrom", [code2], [idx2]))
                states[code1] = [idx1]

        return sorted(DFG, key=lambda x: x[1]), states

    def _handle_assignment(self, node, states):
        left_nodes, right_nodes = self._get_assignment_sides(node)
        if not left_nodes or not right_nodes:
            return [], states

        DFG = []
        for rnode in right_nodes:
            temp, states = self._extract_dfg(rnode, states)
            DFG += temp

        for left_node, right_node in zip(left_nodes, right_nodes):
            left_indexs = self._tree_to_variable_index(left_node)
            right_indexs = self._tree_to_variable_index(right_node)
            for index1 in left_indexs:
                idx1, code1 = self._index_to_code[index1]
                dep_names = [self._index_to_code[x][1] for x in right_indexs]
                dep_idxs  = [self._index_to_code[x][0] for x in right_indexs]

                DFG.append((code1, idx1, "computedFrom", dep_names, dep_idxs))
                states[code1] = [idx1]

        return sorted(DFG, key=lambda x: x[1]), states

    def _handle_increment(self, node, states):
        DFG = []
        indexs = self._tree_to_variable_index(node)
        for index1 in indexs:
            idx1, code1 = self._index_to_code[index1]
            dep_idxs = states[code1].copy() if code1 in states else []
            dep_names = [code1] * len(dep_idxs)
            DFG.append((code1, idx1, "computedFrom", dep_names, dep_idxs))
            states[code1] = [idx1]

        return sorted(DFG, key=lambda x: x[1]), states
    
    def _handle_if(self, node, states):
        DFG = []
        current_states = states.copy()
        others_states = []
        has_else = False

        alternative = node.child_by_field_name("alternative")
        branch_types = maps.ELSE_TYPES.get(self._lang_name, frozenset())

        for child in node.children:
            if child == alternative or child.type in branch_types:
                has_else = True
                temp, new_states = self._extract_dfg(child, states)
                DFG += temp
                others_states.append(new_states)
            else:
                temp, current_states = self._extract_dfg(child, current_states)
                DFG += temp

        others_states.append(current_states)
        if not has_else:
            others_states.append(states)

        new_states = {}
        for dic in others_states:
            for key in dic:
                if key not in new_states:
                    new_states[key] = dic[key].copy()
                else:
                    new_states[key] += dic[key]
        for key in new_states:
            new_states[key] = sorted(list(set(new_states[key])))

        return sorted(DFG, key=lambda x: x[1]), new_states

    def _handle_for(self, node, states):
        DFG = []
        for child in node.children:
            temp, states = self._extract_dfg(child, states)
            DFG += temp

        flag = False
        for child in node.children:
            if flag:
                temp, states = self._extract_dfg(child, states)
                DFG += temp
            elif child.type in ("local_variable_declaration", "declaration"):
                flag = True

        return sorted(self._dedup_dfg(DFG), key=lambda x: x[1]), states

    def _handle_foreach(self, node, states):
        name, value, body = self._get_foreach_parts(node)
        if name is None or value is None:
            return self._handle_while(node, states)

        DFG = []
        for _ in range(2):
            temp, states = self._extract_dfg(value, states)
            DFG += temp

            name_indexs = self._tree_to_variable_index(name)
            value_indexs = self._tree_to_variable_index(value)
            for index1 in name_indexs:
                idx1, code1 = self._index_to_code[index1]
                for index2 in value_indexs:
                    idx2, code2 = self._index_to_code[index2]
                    DFG.append((code1, idx1, "computedFrom", [code2], [idx2]))
                states[code1] = [idx1]

            if body is not None:
                temp, states = self._extract_dfg(body, states)
                DFG += temp
        return sorted(self._dedup_dfg(DFG), key=lambda x: x[1]), states

    def _handle_while(self, node, states):
        DFG = []
        for _ in range(2):
            for child in node.children:
                temp, states = self._extract_dfg(child, states)
                DFG += temp
        return sorted(self._dedup_dfg(DFG), key=lambda x: x[1]), states
    
    def _handle_default(self, node, states, do_first_types):
        DFG = []
        for child in node.children:
            if child.type in do_first_types:
                temp, states = self._extract_dfg(child, states)
                DFG += temp
        for child in node.children:
            if child.type not in do_first_types:
                temp, states = self._extract_dfg(child, states)
                DFG += temp
        return sorted(DFG, key=lambda x: x[1]), states

    def _get_def_name_value(self, node):
        name = node.child_by_field_name("name")
        value = node.child_by_field_name("value")

        # C/C++
        if name is None:
            name = node.child_by_field_name("declarator")

        # Fallback: C#
        if name is None and len(node.children) >= 1:
            name = node.children[0]
            value = node.children[1] if len(node.children) >= 2 else None

        return name, value

    def _get_assignment_sides(self, node):
        """Extract ([left_nodes], [right_nodes]) from an assignment."""

        # Python for_in_clause: left field, last child is the iterable
        if node.type == "for_in_clause":
            left = node.child_by_field_name("left")
            right = node.children[-1] if node.children else None
            return ([left] if left else []), ([right] if right else [])

        left = node.child_by_field_name("left")
        right = node.child_by_field_name("right")
        if left is None or right is None:
            return [], []

        # Python tuple unpacking a, b = x, y
        if self._lang_name == "python" and node.type in ("assignment", "augmented_assignment"):
            left_ch = [c for c in left.children if c.type != ","]
            right_ch = [c for c in right.children if c.type != ","]
            if len(left_ch) == len(right_ch) and len(left_ch) > 0:
                return left_ch, right_ch
            if not left_ch:
                return [left], [right]
            if not right_ch:
                return [left], [right]

        return [left], [right]

    def _get_foreach_parts(self, node):
        # Java enhanced_for_statement: name, value, body
        name = node.child_by_field_name("name")
        value = node.child_by_field_name("value")
        body = node.child_by_field_name("body")

        # C#/Python for_each_statement: left, right, body
        if name is None:
            name = node.child_by_field_name("left")
            value = node.child_by_field_name("right")
            body = node.child_by_field_name("body")

        # C++ for_range_loop: declarator, right, body
        if name is None:
            name = node.child_by_field_name("declarator")
            value = node.child_by_field_name("right")
            body = node.child_by_field_name("body")

        return name, value, body

    def _dedup_dfg(self, dfg):
        merged: dict = {}
        for var_name, token_idx, rel_type, dep_names, dep_idxs in dfg:
            key = (var_name, token_idx, rel_type)
            if key not in merged:
                merged[key] = [list(dep_names), list(dep_idxs)]
            else:
                merged[key][0] = list(set(merged[key][0] + dep_names))
                merged[key][1] = sorted(set(merged[key][1] + dep_idxs))

        return [
            (var_name, token_idx, rel_type, dep_names, dep_idxs)
            for (var_name, token_idx, rel_type), (dep_names, dep_idxs)
            in sorted(merged.items(), key=lambda t: t[0][1])
        ]
    
    # Is from CodeBERT utils: https://github.com/microsoft/CodeBERT/blob/master/GraphCodeBERT/codesearch/parser/utils.py

    def _tree_to_token_index(self, node):
        if (len(node.children) == 0 or node.type == "string") and node.type != "comment":
            return [(node.start_point, node.end_point)]
        result = []
        for child in node.children:
            result += self._tree_to_token_index(child)
        return result

    def _index_to_code_token(self, start_point, end_point):
        if start_point[0] == end_point[0]:
            return self._source_lines[start_point[0]][start_point[1]:end_point[1]]
        s = self._source_lines[start_point[0]][start_point[1]:]
        for i in range(start_point[0] + 1, end_point[0]):
            s += self._source_lines[i]
        s += self._source_lines[end_point[0]][:end_point[1]]
        return s

    def _tree_to_variable_index(self, node):
        if (len(node.children) == 0 or node.type == "string") and node.type != "comment":
            index = (node.start_point, node.end_point)
            if index in self._index_to_code:
                _, code = self._index_to_code[index]
                if node.type != code:
                    return [index]
            return []
        result = []
        for child in node.children:
            result += self._tree_to_variable_index(child)
        return result

