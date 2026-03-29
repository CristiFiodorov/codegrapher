def nested_try(a, b):
    result = 0
    try:
        try:
            if b == 0:
                raise ZeroDivisionError("zero")
            result = a // b
        except ZeroDivisionError:
            if a > 0:
                result = a
            else:
                raise ValueError("both bad")
        result += 1
    except ValueError:
        result = -999
    finally:
        print("outer finally")
    return result


def try_in_loop(items):
    results = []
    for item in items:
        try:
            if item is None:
                raise TypeError("null item")
            if item == 0:
                raise ValueError("zero item")
            results.append(100 // item)
        except TypeError:
            continue
        except ValueError:
            results.append(-1)
            if len(results) > 5:
                break
        finally:
            print("processed")
    return results


def deep_match(data):
    output = []
    for item in data:
        match item:
            case {"type": "a", "val": v}:
                if v > 0:
                    match v % 3:
                        case 0:
                            output.append("a-triple")
                        case 1:
                            output.append("a-rem1")
                        case _:
                            output.append("a-other")
                else:
                    output.append("a-neg")
            case {"type": "b", "val": v}:
                if v == 0:
                    continue
                output.append("b")
            case _:
                break
    return output


def complex_while_for(matrix):
    total = 0
    row = 0
    while row < len(matrix):
        if not matrix[row]:
            row += 1
            continue
        for col, val in enumerate(matrix[row]):
            if val is None:
                break
            if val < 0:
                continue
            if val == 0:
                total += col
            elif val > 100:
                return total
            else:
                total += val
        else:
            row += 1
            continue
        row += 2
    return total


def multi_except_finally(path, mode):
    result = None
    try:
        with open(path) as f:
            data = f.read()
            if not data:
                raise IOError("empty")
            match mode:
                case "upper":
                    result = data.upper()
                case "lower":
                    result = data.lower()
                case _:
                    raise ValueError("bad mode")
    except IOError:
        result = "io_error"
    except ValueError:
        result = "val_error"
    except Exception:
        raise
    finally:
        print("cleanup")
    return result


def generator_with_control(items):
    for i, item in enumerate(items):
        if item is None:
            continue
        if item < 0:
            return
        if item == 0:
            yield i
        else:
            for sub in range(item):
                if sub > 3:
                    break
                yield sub


def recursive_descent(tokens, pos):
    if pos >= len(tokens):
        return None, pos

    match tokens[pos]:
        case "(":
            inner, new_pos = recursive_descent(tokens, pos + 1)
            if new_pos < len(tokens) and tokens[new_pos] == ")":
                return inner, new_pos + 1
            else:
                raise SyntaxError("missing )")
        case ")":
            return None, pos
        case _:
            return tokens[pos], pos + 1


def main():
    nested_try(10, 0)
    nested_try(-5, 0)
    try_in_loop([1, None, 0, 2, None, 0, 3])
    deep_match([
        {"type": "a", "val": 9},
        {"type": "a", "val": -1},
        {"type": "b", "val": 0},
        {"type": "b", "val": 5},
        42,
    ])
    complex_while_for([[1, 2, None], [], [3, -1, 4]])
    list(generator_with_control([0, 2, -1, 5]))
    recursive_descent(["(", "x", ")"], 0)
