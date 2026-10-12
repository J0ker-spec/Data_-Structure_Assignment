from main import evaluate_expression, Stack


def test_stack():
    print("=" * 60)
    print("STACK CLASS UNIT TESTS")
    print("=" * 60)
    passed = 0
    failed = 0

    s = Stack()
    try:
        assert s.is_empty() == True, "New stack should be empty"
        print("[PASS] Stack.is_empty() returns True for new stack")
        passed += 1
    except AssertionError as e:
        print(f"[FAIL] {e}")
        failed += 1

    try:
        assert s.size() == 0, "New stack size should be 0"
        print("[PASS] Stack.size() returns 0 for new stack")
        passed += 1
    except AssertionError as e:
        print(f"[FAIL] {e}")
        failed += 1

    try:
        s.push(10)
        assert s.is_empty() == False, "Stack should not be empty after push"
        assert s.size() == 1, "Stack size should be 1 after one push"
        print("[PASS] Stack.push() adds item correctly")
        passed += 1
    except AssertionError as e:
        print(f"[FAIL] {e}")
        failed += 1

    try:
        s.push(20)
        s.push(30)
        assert s.peek() == 30, "Peek should return last pushed item"
        assert s.size() == 3, "Stack size should be 3"
        print("[PASS] Stack.peek() returns top without removing")
        passed += 1
    except AssertionError as e:
        print(f"[FAIL] {e}")
        failed += 1

    try:
        val = s.pop()
        assert val == 30, "Pop should return last pushed item (LIFO)"
        assert s.size() == 2, "Stack size should decrease after pop"
        assert s.peek() == 20, "Top should now be previous item"
        print("[PASS] Stack.pop() returns top item (LIFO order)")
        passed += 1
    except AssertionError as e:
        print(f"[FAIL] {e}")
        failed += 1

    try:
        s.pop()
        s.pop()
        assert s.is_empty() == True, "Stack should be empty after popping all"
        print("[PASS] Stack properly empties after popping all items")
        passed += 1
    except AssertionError as e:
        print(f"[FAIL] {e}")
        failed += 1

    try:
        s.pop()
        print("[FAIL] Stack.pop() should raise IndexError on empty stack")
        failed += 1
    except IndexError:
        print("[PASS] Stack.pop() raises IndexError on empty stack")
        passed += 1

    try:
        s.peek()
        print("[FAIL] Stack.peek() should raise IndexError on empty stack")
        failed += 1
    except IndexError:
        print("[PASS] Stack.peek() raises IndexError on empty stack")
        passed += 1

    total = passed + failed
    print(f"\nStack Tests: {passed}/{total} PASSED, {failed} FAILED")
    return failed == 0


def run_test(name, expression, expected):
    try:
        result = evaluate_expression(expression)
        if result == expected:
            print(f"[PASS] {name}: {expression} = {result}")
            return True
        else:
            print(f"[FAIL] {name}: {expression} = {result} (expected {expected})")
            return False
    except Exception as e:
        print(f"[FAIL] {name}: {expression} raised exception: {e}")
        return False


def run_error_test(name, expression):
    try:
        result = evaluate_expression(expression)
        print(f"[FAIL] {name}: {expression} should have raised error, got {result}")
        return False
    except (ValueError, ZeroDivisionError, IndexError):
        print(f"[PASS] {name}: {expression} correctly raised error")
        return True
    except Exception as e:
        print(f"[FAIL] {name}: {expression} raised unexpected exception type: {type(e).__name__}: {e}")
        return False


def test_expression_evaluator():
    print()
    print("=" * 60)
    print("EXPRESSION EVALUATOR TESTS")
    print("=" * 60)
    passed = 0
    failed = 0

    print("\n--- MANDATORY TEST CASES (7 required) ---")
    mandatory_tests = [
        ("M1: Basic Addition", "3+5", 8),
        ("M2: Basic Multiplication", "5*4", 20),
        ("M3: Operator Precedence", "3+5*2", 13),
        ("M4: Parentheses", "(3+5)*2", 16),
        ("M5: Basic Division (Integer)", "10/2", 5),
        ("M6: Division (Decimal)", "3/4", 0.75),
        ("M7: Complex Expression", "10-(2+3)*4", -10),
    ]
    for name, expr, expected in mandatory_tests:
        if run_test(name, expr, expected):
            passed += 1
        else:
            failed += 1

    print("\n--- ADDITIONAL TEST CASES ---")
    additional_tests = [
        ("A1: Addition with spaces", "100 + 200", 300),
        ("A2: Decimal addition", "12.5 + 7.5", 20),
        ("A3: Left-associative subtraction", "10 - 3 - 2", 5),
        ("A4: Left-associative division", "8 / 2 / 2", 2),
        ("A5: Multiple precedence levels", "2 * 3 + 4 * 5", 26),
        ("A6: Nested parentheses", "((2+3)*(4-1))", 15),
        ("A7: Parentheses with division", "(10 + 5) / (3 - 0)", 5),
        ("A8: Mixed operations", "5 * (2 + 3) / 5", 5),
        ("A9: Decimal multiplication", "2.5 * 4", 10),
        ("A10: Repeating decimal division", "100 / 3", 100 / 3),
        ("A11: Unary minus", "-5+3", -2),
        ("A12: Unary plus", "+7-2", 5),
    ]
    for name, expr, expected in additional_tests:
        if run_test(name, expr, expected):
            passed += 1
        else:
            failed += 1

    print("\n--- ERROR HANDLING TESTS ---")
    error_tests = [
        ("E1: Division by zero", "10/0"),
        ("E2: Mismatched parens (open only)", "(3+5"),
        ("E3: Mismatched parens (close only)", "3+5)"),
        ("E4: Invalid letters", "abc"),
        ("E5: Invalid symbol", "5*@3"),
        ("E6: Double decimal point", "..5"),
        ("E7: Multiple decimals", "3..2"),
        ("E8: Empty expression", ""),
    ]
    for name, expr in error_tests:
        if run_error_test(name, expr):
            passed += 1
        else:
            failed += 1

    total = passed + failed
    print(f"\nExpression Tests: {passed}/{total} PASSED, {failed} FAILED")
    return failed == 0


def main():
    print()
    print("*" * 60)
    print(" DCOMP320 ASSIGNMENT 1 - OFFICIAL TEST SUITE")
    print("*" * 60)
    print()

    stack_ok = test_stack()
    expr_ok = test_expression_evaluator()

    print()
    print("=" * 60)
    print("FINAL TEST SUMMARY")
    print("=" * 60)

    if stack_ok and expr_ok:
        print("ALL TESTS PASSED. Ready for submission.")
        print("=" * 60)
        return 0
    else:
        if not stack_ok:
            print("ISSUE: Some Stack tests FAILED")
        if not expr_ok:
            print("ISSUE: Some Expression tests FAILED")
        print("NOT all tests passed - review and fix before submission.")
        print("=" * 60)
        return 1


if __name__ == '__main__':
    exit(main())
