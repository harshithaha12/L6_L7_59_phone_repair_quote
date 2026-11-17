# Software Engineering Lab Repository: Phone Repair Quote System

**Student Name:** Harshitha Vangaveti  
**SRN:** PES2UG24AM064  
**Assignment Repository:** `L6_L7_59_phone_repair_quote`  
**Course:** Software Engineering  

---

## Overview

This repository contains the complete implementation, test suites, coverage reports, and security hardening for **Lab 6** and **Lab 7** of the Software Engineering curriculum.

- **Lab 6**: Code and Branch Coverage Analysis using Python's `coverage` and `pytest` frameworks.
- **Lab 7**: Dynamic Fuzz Testing for input validation vulnerabilities using the `Hypothesis` property-based testing library and defensive programming.

---

## Repository Structure

```text
L6_L7_59_phone_repair_quote/
│
├── README.md                                   # Comprehensive repository documentation
├── .gitignore                                  # Git ignore rules for Python, caches, and test artifacts
│
├── LAB6/                                       # Lab 6: Code and Branch Coverage Analysis
│   ├── phone_repair_quote.py                   # Core business logic module under test
│   ├── test_phone_repair_quote.py              # Baseline/starter test file with coverage tests
│   ├── CodeCoverageTest_phone_repair_quote.py  # Targeted test suite achieving 100% Line Coverage
│   ├── BranchCoverageTest_phone_repair_quote.py# Targeted test suite achieving 100% Branch Coverage
│   ├── code_coverage_report.png                # Terminal execution screenshot for Code Coverage
│   ├── code_coverage_report.txt                # Raw terminal output log for Code Coverage
│   ├── branch_coverage_report.png              # Terminal execution screenshot for Branch Coverage
│   └── branch_coverage_report.txt              # Raw terminal output log for Branch Coverage
│
└── LAB7/                                       # Lab 7: Fuzz Testing for Input Validation Bugs
    ├── phone_repair_quote_parser.py            # Security-hardened input parsing module
    ├── test_phone_repair_quote_parser.py       # Hypothesis property-based fuzz tests
    ├── PES2UG24AM064_Harshitha_Vangaveti_LAB7.pdf # Final submission report with SS1–SS4 & reflections
    ├── SS1_buggy_run.png                       # SS1: Original buggy parser execution
    ├── SS2_failing_tests.png                   # SS2: Hypothesis fuzz tests failing on buggy code
    ├── SS3_fixed_run.png                       # SS3: Hardened parser execution on standard input
    └── SS4_passing_tests.png                   # SS4: Hypothesis fuzz tests passing on hardened code
```

---

## Lab 6: Code & Branch Coverage Analysis

### Objective
Measure, evaluate, and maximize test completeness for the `phone_repair_quote` application by writing comprehensive test suites that achieve **>90% line and branch coverage** and eliminate untested paths and dead code.

### Delivered Test Suites
1. **`CodeCoverageTest_phone_repair_quote.py`**
   - Contains 13 unit tests targeting every statement and error condition.
   - **Result:** **100% Line Coverage** (40/40 statements covered).
2. **`BranchCoverageTest_phone_repair_quote.py`**
   - Contains 18 unit tests systematically exercising all true/false decision paths, logical combinations (`and`/`or`), and boundary conditions.
   - **Result:** **100% Branch Coverage** (28/28 branches covered).

### Coverage Summary Table
| Module | Statements | Missed | Branches | Missed Branches | Total Coverage |
|:---|:---:|:---:|:---:|:---:|:---:|
| `phone_repair_quote.py` | 40 | 0 | 28 | 0 | **100%** |
| `CodeCoverageTest_phone_repair_quote.py` | 32 | 0 | 0 | 0 | **100%** |
| `BranchCoverageTest_phone_repair_quote.py` | 43 | 0 | 0 | 0 | **100%** |

### How to Run Lab 6 Coverage

```bash
cd LAB6

# 1. Run Line Coverage
coverage run -m pytest CodeCoverageTest_phone_repair_quote.py
coverage report -m

# 2. Run Branch Coverage
coverage run --branch -m pytest BranchCoverageTest_phone_repair_quote.py
coverage report -m
```

---

## Lab 7: Fuzz Testing for Input Validation Bugs

### Objective
Apply property-based fuzz testing via `Hypothesis` to detect hidden input validation bugs, crashes, and unhandled exceptions in `phone_repair_quote_parser.py`, and harden the module using defensive programming.

### Bugs Discovered by Fuzzing
When running property-based tests across random string strategies and `None` (`st.text() | st.none()`), Hypothesis exposed three critical failure modes:
1. **`AttributeError` on `NoneType`**: Calling `.replace()`, `.split()`, or `.strip()` when input was `None`.
2. **`ValueError: not enough values to unpack`**: Empty inputs (`""`) or strings lacking expected delimiters (`'x'` or space separator) crashing tuple unpacking.
3. **`ValueError: invalid literal for int()`**: Corrupted non-numeric quantities (e.g. `'screen x'` or `'x'`).

### Hardening & Defensive Programming Applied
- **Type Guarding**: Added upfront `isinstance(..., str)` checks returning safe defaults (`""`, `{}`, or `("", "")`).
- **Delimiter & Structure Validation**: Checked for required delimiters before splitting and used `rsplit('x', 1)` to handle names safely.
- **Exception Handling**: Wrapped integer conversion in `try...except (ValueError, TypeError)` to ignore corrupted entries instead of crashing the process.

### Screenshot Deliverables Overview
- **SS1 (`SS1_buggy_run.png`)**: Interactive run of the baseline module with sample inputs.
- **SS2 (`SS2_failing_tests.png`)**: Hypothesis identifying failing counterexamples on the unhardened module.
- **SS3 (`SS3_fixed_run.png`)**: Clean execution of the hardened module with valid inputs.
- **SS4 (`SS4_passing_tests.png`)**: All Hypothesis fuzz tests passing 100% across hundreds of random and malformed inputs.
- **PDF Report (`PES2UG24AM064_Harshitha_Vangaveti_LAB7.pdf`)**: Formatted submission document including all 4 screenshots and answers to reflection questions.

### How to Run Lab 7 Fuzz Tests

```bash
cd LAB7

# Run parser interactively
python phone_repair_quote_parser.py

# Run Hypothesis fuzz tests
pytest test_phone_repair_quote_parser.py -v
```

---

## Environment Setup & Requirements

- Python 3.8+
- Install required packages:
  ```bash
  pip install pytest coverage hypothesis reportlab pillow
  ```
