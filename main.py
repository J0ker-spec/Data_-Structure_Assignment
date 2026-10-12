class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def __str__(self):
        return str(self._items)


OPERATOR_PRECEDENCE = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2
}


def get_precedence(operator):
    return OPERATOR_PRECEDENCE.get(operator, 0)


def apply_operator(operator, right_operand, left_operand):
    if operator == '+':
        return left_operand + right_operand
    elif operator == '-':
        return left_operand - right_operand
    elif operator == '*':
        return left_operand * right_operand
    elif operator == '/':
        if right_operand == 0:
            raise ZeroDivisionError("Division by zero is not allowed")
        return left_operand / right_operand
    else:
        raise ValueError(f"Unknown operator: {operator}")


def tokenize(expression):
    tokens = []
    i = 0
    n = len(expression)

    while i < n:
        char = expression[i]

        if char.isspace():
            i += 1
            continue

        if char.isdigit() or char == '.':
            j = i
            has_decimal = False
            while j < n and (expression[j].isdigit() or expression[j] == '.'):
                if expression[j] == '.':
                    if has_decimal:
                        raise ValueError(f"Invalid number: multiple decimal points")
                    has_decimal = True
                j += 1
            number_str = expression[i:j]
            if number_str == '.':
                raise ValueError("Invalid number: standalone decimal point")
            tokens.append(('NUMBER', float(number_str)))
            i = j
            continue

        if char in '+-*/()':
            tokens.append(('OPERATOR', char))
            i += 1
            continue

        raise ValueError(f"Invalid character: '{char}'")

    return tokens


def evaluate_expression(expression):
    if not expression or expression.strip() == '':
        raise ValueError("Empty expression")

    tokens = tokenize(expression)

    operand_stack = Stack()
    operator_stack = Stack()

    prev_token_type = None

    for token_type, token_value in tokens:
        if token_type == 'NUMBER':
            operand_stack.push(token_value)
            prev_token_type = 'NUMBER'

        elif token_type == 'OPERATOR':
            if token_value == '(':
                operator_stack.push(token_value)
                prev_token_type = 'OPEN_PAREN'

            elif token_value == ')':
                if prev_token_type == 'OPERATOR' or prev_token_type == 'OPEN_PAREN':
                    raise ValueError("Invalid expression: unexpected closing parenthesis")

                found_open = False
                while not operator_stack.is_empty():
                    top_op = operator_stack.pop()
                    if top_op == '(':
                        found_open = True
                        break
                    if operand_stack.size() < 2:
                        raise ValueError("Invalid expression: insufficient operands")
                    right = operand_stack.pop()
                    left = operand_stack.pop()
                    result = apply_operator(top_op, right, left)
                    operand_stack.push(result)

                if not found_open:
                    raise ValueError("Mismatched parentheses: no opening parenthesis found")
                prev_token_type = 'CLOSE_PAREN'

            else:
                if prev_token_type is None and token_value in ('+', '-'):
                    operand_stack.push(0.0)

                elif prev_token_type in ('OPERATOR', 'OPEN_PAREN', None):
                    if token_value in ('+', '-'):
                        operand_stack.push(0.0)
                    else:
                        raise ValueError(f"Invalid expression: unexpected operator '{token_value}'")

                while not operator_stack.is_empty():
                    top_op = operator_stack.peek()
                    if top_op == '(':
                        break
                    if get_precedence(top_op) >= get_precedence(token_value):
                        if operand_stack.size() < 2:
                            raise ValueError("Invalid expression: insufficient operands")
                        operator_stack.pop()
                        right = operand_stack.pop()
                        left = operand_stack.pop()
                        result = apply_operator(top_op, right, left)
                        operand_stack.push(result)
                    else:
                        break

                operator_stack.push(token_value)
                prev_token_type = 'OPERATOR'

    while not operator_stack.is_empty():
        top_op = operator_stack.pop()
        if top_op == '(':
            raise ValueError("Mismatched parentheses: no closing parenthesis found")
        if operand_stack.size() < 2:
            raise ValueError("Invalid expression: insufficient operands")
        right = operand_stack.pop()
        left = operand_stack.pop()
        result = apply_operator(top_op, right, left)
        operand_stack.push(result)

    if operand_stack.size() != 1:
        raise ValueError("Invalid expression: too many operands")

    final_result = operand_stack.pop()

    if isinstance(final_result, float) and final_result.is_integer():
        return int(final_result)
    return final_result


def process_input_file(input_file_path):
    lines = []
    with open(input_file_path, 'r') as f:
        for line in f:
            lines.append(line.rstrip('\n'))
    return lines


def is_separator_line(line):
    stripped = line.strip()
    if not stripped:
        return False
    only_dashes = all(c in '-' for c in stripped) and len(stripped) >= 3
    only_equals = all(c in '=' for c in stripped) and len(stripped) >= 3
    return only_dashes or only_equals


def is_blank_line(line):
    return line.strip() == ''


def _contains_letters(s):
    for c in s:
        if c.isalpha():
            return True
    return False


def is_comment_line(line):
    stripped = line.strip()
    if not stripped:
        return False

    if not _contains_letters(stripped):
        return False

    if '---' in stripped:
        return True

    space_count = stripped.count(' ')
    if space_count >= 2:
        return True

    return False


def evaluate_and_format_lines(lines):
    output_lines = []

    for line in lines:
        if is_blank_line(line):
            output_lines.append(line)
            continue

        if is_separator_line(line):
            output_lines.append(line)
            continue

        if is_comment_line(line):
            output_lines.append(line)
            continue

        try:
            result = evaluate_expression(line)
            output_lines.append(f"{line} = {result}")
        except ZeroDivisionError as e:
            output_lines.append(f"{line} = ERROR: {str(e)}")
        except Exception as e:
            output_lines.append(f"{line} = ERROR: {str(e)}")

    return output_lines


def write_output_file(output_lines, output_file_path):
    with open(output_file_path, 'w') as f:
        for line in output_lines:
            f.write(line + '\n')


def main():
    input_file = 'input.txt'
    output_file = 'output.txt'

    print("=" * 60)
    print("DCOMP320 Stack-Based Mathematical Expression Evaluator")
    print("=" * 60)
    print()

    try:
        lines = process_input_file(input_file)
        print(f"[OK] Successfully read input file: {input_file}")
        print(f"     Total lines read: {len(lines)}")
        print()
    except FileNotFoundError:
        print(f"[ERROR] Input file '{input_file}' not found.")
        print(f"        Please ensure '{input_file}' exists in the same directory.")
        return
    except Exception as e:
        print(f"[ERROR] Failed to read input file: {str(e)}")
        return

    print("[INFO] Evaluating expressions...")
    print()
    output_lines = evaluate_and_format_lines(lines)

    try:
        write_output_file(output_lines, output_file)
        print(f"[OK] Successfully wrote output file: {output_file}")
        print()
    except Exception as e:
        print(f"[ERROR] Failed to write output file: {str(e)}")
        return

    print("=" * 60)
    print("EVALUATION RESULTS")
    print("=" * 60)
    for line in output_lines:
        print(line)
    print("=" * 60)
    print()
    print("Evaluation complete.")


if __name__ == '__main__':
    main()
