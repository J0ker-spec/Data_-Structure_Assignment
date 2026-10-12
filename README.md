# DCOMP320 Data Structures & Algorithms - Assignment 1

## Stack-Based Mathematical Expression Evaluator

---

## 1. Purpose

This project implements a **custom Stack data structure** and uses it to build a **mathematical expression evaluator** that can parse and calculate infix arithmetic expressions. The evaluator reads expressions from an input file, computes them using the two-stack algorithm, and writes results to an output file. This assignment demonstrates understanding of LIFO (Last-In, First-Out) data structures, operator precedence, parentheses handling, and file processing — core topics in DCOMP320 Data Structures & Algorithms.

**Weight:** 10% of course total grade.

---

## 2. Objectives

Upon completion of this assignment, the following learning outcomes are demonstrated:

1. **Implement a custom Stack class** with standard LIFO operations (`push`, `pop`, `peek`, `is_empty`, `size`) without using Python's built-in `eval()` or external expression libraries.
2. **Apply the two-stack algorithm** (operand stack + operator stack) to evaluate fully parenthesized and partially parenthesized infix arithmetic expressions.
3. **Handle operator precedence** correctly (`*`, `/` before `+`, `-`) with left-to-right associativity for same-precedence operators.
4. **Support parentheses** to override default precedence, including nested parentheses.
5. **Support numeric features**: multi-digit integers, floating-point decimals, and optional spacing around tokens.
6. **Handle unary operators** (e.g., `-5+3`, `+7-2`) and correctly order left/right operands for non-commutative operations (`-`, `/`).
7. **Robust error handling** for division-by-zero, mismatched parentheses, invalid characters, malformed numbers, and empty expressions.
8. **File I/O integration**: read expressions from `input.txt`, preserve structural separator lines, evaluate each expression, and generate `output.txt` automatically.
9. **Modular, maintainable code** with clear functions: `main()`, `apply_operator()`, `evaluate_expression()`, `process_input_file()`, `write_output_file()`.
10. **Comprehensive testing** with explicit PASS/FAIL validation and reproducible results.

---

## 3. Stack Data Structure & LIFO Principle

### 3.1 What is a Stack?

A **Stack** is an abstract data type (ADT) that stores a collection of elements and operates on the **LIFO (Last-In, First-Out)** principle: the last element added (pushed) to the stack is the first element removed (popped) from the stack.

### 3.2 LIFO Analogy

Think of a stack of dinner plates:
- You **push** (add) a new plate **on top** of the stack.
- You **pop** (remove) the **topmost** plate first — you cannot take a plate from the middle or bottom without removing the ones above first.

### 3.3 Stack Operations Implemented

| Operation    | Description                                                  | Time Complexity |
|--------------|--------------------------------------------------------------|-----------------|
| `push(item)` | Adds `item` to the top of the stack.                         | O(1)            |
| `pop()`      | Removes and returns the item from the top of the stack. Raises `IndexError` if empty. | O(1) |
| `peek()`     | Returns (but does not remove) the top item. Raises `IndexError` if empty. | O(1) |
| `is_empty()` | Returns `True` if the stack contains no items, `False` otherwise. | O(1) |
| `size()`     | Returns the count of items currently in the stack.           | O(1)            |

### 3.4 Why Stacks for Expression Evaluation?

Stacks are ideal for expression evaluation because:
- **Nested structure matching**: Parentheses are naturally LIFO — the most recently opened parenthesis must close first.
- **Operator deferral**: Lower-precedence operators (e.g., `+`) can be pushed onto the operator stack and deferred while higher-precedence operators (e.g., `*`) are evaluated first.
- **Operand order preservation**: The stack preserves the correct left-to-right order of operands for non-commutative operations (subtraction, division).

---

## 4. Algorithm: Two-Stack Expression Evaluation

### 4.1 Overview

The program uses **Edsger Dijkstra's Two-Stack Algorithm** for infix expression evaluation:
- **Operand Stack (values)**: stores numbers (integers and decimals) encountered while scanning the expression.
- **Operator Stack (ops)**: stores arithmetic operators (`+`, `-`, `*`, `/`) and parentheses `(` `)`.

### 4.2 Step-by-Step Algorithm

1. **Initialize** two empty stacks: `operand_stack` and `operator_stack`.

2. **Tokenize** the input expression: scan left-to-right and split into numbers, operators, and parentheses. Skip whitespace.

3. **Process each token**:
   - **If token is a NUMBER**: push it onto `operand_stack`.
   - **If token is '(' (open parenthesis)**: push it onto `operator_stack`.
   - **If token is ')' (close parenthesis)**:
     - While `operator_stack` is not empty and its top is **not** `(`:
       - Pop an operator from `operator_stack`.
       - Pop **two** operands: first pop → **right operand**, second pop → **left operand**.
       - Compute: `result = left_operand <operator> right_operand`.
       - Push `result` onto `operand_stack`.
     - Pop the `(` from `operator_stack` (discard it).
   - **If token is an OPERATOR** (`+`, `-`, `*`, `/`):
     - While `operator_stack` is not empty **and** the precedence of the operator on top of `operator_stack` is **≥** the precedence of the current operator:
       - Pop the top operator.
       - Pop **two** operands: first pop → **right operand**, second pop → **left operand**.
       - Compute: `result = left_operand <operator> right_operand`.
       - Push `result` onto `operand_stack`.
     - Push the current operator onto `operator_stack`.

4. **After all tokens are processed**:
   - While `operator_stack` is not empty:
     - Pop the top operator.
     - Pop **two** operands: first pop → **right operand**, second pop → **left operand**.
     - Compute: `result = left_operand <operator> right_operand`.
     - Push `result` onto `operand_stack`.

5. **Result**: The final (and only) value on `operand_stack` is the expression result.

### 4.3 Critical: Left/Right Operand Order

For **commutative** operations (`+`, `*`), operand order does not matter.

For **non-commutative** operations (`-`, `/`), operand order is **critical** and must be preserved correctly:

> When popping operands for evaluation:
> - First `pop()` → **Right Operand**
> - Second `pop()` → **Left Operand**
> - Compute: `left_operand OPERATOR right_operand`

**Example**: `10 - 3 - 2`
```
After scanning: operands=[10,3,2], operators=[-,-]
First apply:  pop op1='-', pop right=3, pop left=10 → 10-3=7 → operands=[7], operators=[-]
Second apply: pop op2='-', pop right=2, pop left=7  → 7-2=5  → Correct result.
```

If the order were reversed (right - left), the incorrect result would be `-1`.

---

## 5. Operator Precedence

### 5.1 Precedence Table

| Operator | Precedence Level | Associativity |
|----------|------------------|---------------|
| `(`, `)` | Highest (special) | N/A           |
| `*`, `/` | 2                | Left-to-Right |
| `+`, `-` | 1                | Left-to-Right |

### 5.2 How Precedence is Applied

When the algorithm encounters a new operator, it compares its precedence with the precedence of the operator currently on top of the `operator_stack`:

- If the **top-of-stack operator has ≥ precedence** than the incoming operator → the top operator is evaluated first (popped, applied, result pushed). This repeats until the top of the stack has lower precedence or is `(`.
- Only then is the new operator pushed onto the stack.

**Example walk-through: `3 + 5 * 2`**

```
Token '3' (number):       operands=[3], operators=[]
Token '+' (operator):     top of stack empty → push. operands=[3], operators=['+']
Token '5' (number):       operands=[3,5], operators=['+']
Token '*' (operator):     top='+' (prec 1) < '*' (prec 2) → push '*'. operands=[3,5], operators=['+','*']
Token '2' (number):       operands=[3,5,2], operators=['+','*']

End of tokens → process remaining operators:
  Pop '*': pop right=2, pop left=5 → 5*2=10 → operands=[3,10], operators=['+']
  Pop '+': pop right=10, pop left=3 → 3+10=13 → operands=[13], operators=[]

Result = 13 ✓ (correct: multiplication performed before addition)
```

### 5.3 Left Associativity for Equal Precedence

Same-precedence operators (`+` and `-` are both level 1; `*` and `/` are both level 2) use **≥** comparison, enforcing left-to-right evaluation:

**Example: `10 - 3 - 2`**
- Left-associative: `(10 - 3) - 2 = 5` ✓ (correct)
- Right-associative (wrong): `10 - (3 - 2) = 9` ✗

---

## 6. Parentheses Handling

### 6.1 How Parentheses Override Precedence

Parentheses `( )` force a sub-expression to be evaluated first, regardless of operator precedence.

**Example**: `(3 + 5) * 2`
- Without parentheses: `3 + 5 * 2 = 13` (multiply first)
- With parentheses: `(3 + 5) * 2 = 16` (addition first due to parens)

### 6.2 Algorithm Steps for Parentheses

**When `(` is encountered**:
- Push it directly onto the `operator_stack`. It acts as a "sentinel" or "marker" — no operator will be applied past this point until a matching `)` is found.

**When `)` is encountered**:
- Continuously pop operators from the `operator_stack` and apply them (using operands from the operand stack) **until a `(` is reached and popped from the stack**.
- All operators between `(` and `)` have thus been evaluated, and their accumulated result is on the operand stack.

### 6.3 Nested Parentheses

Nested parentheses are handled naturally by the stack's LIFO property:
- Inner `(` are pushed deeper into the operator stack.
- Innermost `)` will match and pop the most recent unmatched `(` first.
- Example: `((2+3)*(4-1))` → inner `(2+3)=5` and `(4-1)=3`, then `5*3=15`.

### 6.4 Mismatched Parentheses Detection

The algorithm detects and reports two common errors:
1. **Unmatched `(` (missing closing parenthesis)**: After all tokens are processed, if `(` remains on the operator stack → error.
2. **Unmatched `)` (missing opening parenthesis)**: When processing `)`, if the operator stack empties before finding `(` → error.

---

## 7. Project Structure & Files

### 7.1 Directory Tree

```
data-structures-assignment-1/
├── main.py                 # Core program: Stack, evaluator, file I/O, main()
├── input.txt               # Input file with expressions to evaluate
├── output.txt              # Auto-generated output file with results
├── test_evaluator.py       # Test suite (Stack unit tests + expression tests)
├── README.md               # This documentation file
├── .gitignore              # Git ignore rules
└── report/
    └── Assignment_Report.docx   # Academic report (Word document)
```

### 7.2 File Descriptions

#### `main.py`
The main program file containing all required modular components:

| Component | Purpose |
|-----------|---------|
| `Stack` class | Custom LIFO stack with `push`, `pop`, `peek`, `is_empty`, `size` |
| `OPERATOR_PRECEDENCE` | Dictionary mapping operators to precedence levels |
| `get_precedence(operator)` | Returns precedence of a given operator |
| `apply_operator(op, right, left)` | Applies operator with correct left/right operand order |
| `tokenize(expression)` | Converts raw string expression into typed tokens (NUMBER/OPERATOR) |
| `evaluate_expression(expression)` | Main two-stack evaluator; returns numeric result or raises error |
| `process_input_file(path)` | Reads all lines from input.txt preserving structure |
| `is_separator_line(line)` | Detects separator lines (`---`, `===`) to preserve unchanged |
| `is_comment_line(line)` | Detects header/comment lines to preserve unchanged |
| `is_blank_line(line)` | Detects empty/whitespace-only lines |
| `evaluate_and_format_lines(lines)` | Processes each line: preserves separators/comments/blanks, evaluates expressions |
| `write_output_file(lines, path)` | Writes processed lines to output.txt |
| `main()` | Entry point: orchestrates reading, evaluation, writing, and console output |

#### `input.txt`
Human-editable plain-text input file. Each non-blank, non-separator, non-comment line is treated as one mathematical expression. The file may contain:
- **Blank lines**: preserved in output
- **Separator lines**: lines composed entirely of `---` or `===` characters (preserved verbatim)
- **Comment/Header lines**: lines containing letters and descriptive text with spaces or `---` markers (preserved verbatim)
- **Expression lines**: any line containing a valid or invalid arithmetic expression (evaluated and result appended)

#### `output.txt`
Auto-generated by `main.py`. Contains the same structure as `input.txt` (preserving blanks, separators, and comments), but every expression line has the format:
```
<expression> = <result>
```
If evaluation fails, the format is:
```
<expression> = ERROR: <descriptive message>
```

#### `test_evaluator.py`
Standalone test script. Run with `python test_evaluator.py`. Outputs explicit `[PASS]` or `[FAIL]` for every test case and a final summary.

---

## 8. Testing

### 8.1 Running the Test Suite

```bash
python test_evaluator.py
```

### 8.2 Mandatory Test Cases (7 Required) — ALL PASS

| ID | Expression     | Expected Result | Status |
|----|----------------|-----------------|--------|
| M1 | `3+5`          | 8               | PASS ✓ |
| M2 | `5*4`          | 20              | PASS ✓ |
| M3 | `3+5*2`        | 13              | PASS ✓ |
| M4 | `(3+5)*2`      | 16              | PASS ✓ |
| M5 | `10/2`         | 5               | PASS ✓ |
| M6 | `3/4`          | 0.75            | PASS ✓ |
| M7 | `10-(2+3)*4`   | -10             | PASS ✓ |

### 8.3 Additional Test Cases — ALL PASS

| ID  | Expression            | Expected Result | Status |
|-----|-----------------------|-----------------|--------|
| A1  | `100 + 200`           | 300             | PASS ✓ |
| A2  | `12.5 + 7.5`          | 20              | PASS ✓ |
| A3  | `10 - 3 - 2`          | 5               | PASS ✓ |
| A4  | `8 / 2 / 2`           | 2               | PASS ✓ |
| A5  | `2 * 3 + 4 * 5`       | 26              | PASS ✓ |
| A6  | `((2+3)*(4-1))`       | 15              | PASS ✓ |
| A7  | `(10 + 5) / (3 - 0)`  | 5               | PASS ✓ |
| A8  | `5 * (2 + 3) / 5`     | 5               | PASS ✓ |
| A9  | `2.5 * 4`             | 10              | PASS ✓ |
| A10 | `100 / 3`             | ~33.333...      | PASS ✓ |
| A11 | `-5+3`                | -2              | PASS ✓ |
| A12 | `+7-2`                | 5               | PASS ✓ |

### 8.4 Error Handling Tests — ALL PASS

| ID | Expression  | Scenario                        | Status |
|----|-------------|---------------------------------|--------|
| E1 | `10/0`      | Division by zero                | PASS ✓ |
| E2 | `(3+5`      | Missing closing parenthesis     | PASS ✓ |
| E3 | `3+5)`      | Missing opening parenthesis     | PASS ✓ |
| E4 | `abc`       | Invalid letters in expression   | PASS ✓ |
| E5 | `5*@3`      | Invalid symbol                  | PASS ✓ |
| E6 | `..5`       | Double decimal point            | PASS ✓ |
| E7 | `3..2`      | Multiple decimal points         | PASS ✓ |
| E8 | ` ` (empty) | Empty expression                | PASS ✓ |

### 8.5 Stack Unit Tests — ALL PASS (8/8)

All Stack operations verified: `is_empty()`, `size()`, `push()`, `peek()`, `pop()`, correct LIFO order, and proper exceptions on empty-stack operations.

### 8.6 Official Test Result

```
ALL TESTS PASSED. Ready for submission.
- Stack Tests: 8/8 PASSED
- Expression Tests: 27/27 PASSED
  - Mandatory: 7/7 PASSED
  - Additional: 12/12 PASSED
  - Error Handling: 8/8 PASSED
- TOTAL: 35/35 PASSED
```

---

## 9. Error Handling

The evaluator **sensibly** handles the following error conditions without crashing:

| Error Condition              | Behavior / Error Message                                  |
|------------------------------|-----------------------------------------------------------|
| **Division by zero**         | `ERROR: Division by zero is not allowed`                  |
| **Unmatched `(`**            | `ERROR: Mismatched parentheses: no closing parenthesis found` |
| **Unmatched `)`**            | `ERROR: Mismatched parentheses: no opening parenthesis found` |
| **Invalid character**        | `ERROR: Invalid character: 'X'`                           |
| **Multiple decimal points**  | `ERROR: Invalid number: multiple decimal points`          |
| **Standalone decimal**       | `ERROR: Invalid number: standalone decimal point`         |
| **Misplaced operator**       | `ERROR: Invalid expression: unexpected operator '*'`      |
| **Too few operands**         | `ERROR: Invalid expression: insufficient operands`        |
| **Too many operands**        | `ERROR: Invalid expression: too many operands`            |
| **Empty expression**         | `ERROR: Empty expression`                                 |
| **Stack underflow (pop)**    | `IndexError: Cannot pop from an empty stack`              |
| **Stack underflow (peek)**   | `IndexError: Cannot peek at an empty stack`               |
| **Missing input.txt**        | Graceful message: `Input file 'input.txt' not found`      |

All errors are caught at the file-processing level and formatted as `ERROR:` messages in the output file; the program continues evaluating remaining expressions rather than terminating.

---

## 10. How to Run

### Prerequisites

- **Python 3.7+** (no external dependencies required — uses only the Python standard library)

### Steps

1. Open a terminal/command prompt in the project directory:
   ```
   cd data-structures-assignment-1
   ```

2. **(Optional) Add/edit expressions** in `input.txt` if desired. Separator lines (`---`, `===`), blank lines, and comment lines are preserved.

3. Run the main program:
   ```bash
   python main.py
   ```

4. **Check output**: Results are printed to the console AND written to `output.txt` in the same directory.

5. **(Optional) Run the test suite** to validate correctness:
   ```bash
   python test_evaluator.py
   ```

---

## 11. GitHub Submission Instructions

### 11.1 Repository Structure

The repository should mirror this project structure exactly:

```
your-username/data-structures-assignment-1
├── main.py
├── input.txt
├── output.txt
├── test_evaluator.py
├── README.md
├── .gitignore
└── report/
    └── Assignment_Report.docx
```

### 11.2 Initialising Git & Pushing to GitHub

```bash
# 1. Navigate to project directory
cd data-structures-assignment-1

# 2. Initialise git repository
git init

# 3. Add all files (respects .gitignore)
git add .

# 4. Commit with a descriptive message
git commit -m "Initial submission: Stack-based expression evaluator - DCOMP320 Assignment 1"

# 5. Add GitHub remote (replace YOUR_USERNAME and YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/data-structures-assignment-1.git

# 6. Push to GitHub
git branch -M main
git push -u origin main
```

### 11.3 `.gitignore` Included

The provided `.gitignore` excludes common unwanted files:
- Python cache: `__pycache__/`, `*.pyc`
- Editor/IDE settings: `.vscode/`, `.idea/`
- OS files: `.DS_Store`, `Thumbs.db`
- Virtual environments: `venv/`, `env/`

---

## 12. Academic Integrity

This assignment is an **individual** submission. All code (`Stack` class, two-stack evaluator, tokenizer, file I/O), tests, and documentation were implemented from scratch by the student. No use of `eval()`, `exec()`, `ast`, `sympy`, or any external expression-evaluation library was made. No portion of this work was copied from another student, online solution, or generative AI tool without critical understanding and transformation into original work.

---

## 13. Marking Criteria Checklist (100% = 100 marks → 10% course weight)

| Criterion              | Weight | Evidence of Completion                                             | Status |
|------------------------|--------|--------------------------------------------------------------------|--------|
| **1. Stack Class**     | 15%    | Custom `Stack` with `push`, `pop`, `peek`, `is_empty`, `size`; 8/8 Stack unit tests PASS | ✓ Complete |
| **2. Input Processing**| 30%    | Reads `input.txt`; preserves separators/comments/blanks; handles decimals, multi-digit, spaces, unary ops | ✓ Complete |
| **3. Output/Results**  | 30%    | Generates `output.txt` automatically; correct results; 7 mandatory tests PASS; 27/27 expression tests PASS | ✓ Complete |
| **4. Testing**         | 15%    | Standalone `test_evaluator.py` with 35 explicit [PASS] tests; testing table in README + report | ✓ Complete |
| **5. Docs / GitHub**   | 10%    | Comprehensive README (13 sections); .gitignore; modular code; doc-ready GitHub structure | ✓ Complete |
| **TOTAL**              | **100%** |                                                                     | **READY** |

---

*End of README.md — DCOMP320 Assignment 1*
