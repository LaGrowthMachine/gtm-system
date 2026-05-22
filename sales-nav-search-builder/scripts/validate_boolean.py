#!/usr/bin/env python3
"""
Boolean Search String Validator

Validates LinkedIn Sales Navigator boolean strings against the known rules:
- Balanced parens
- Uppercase operators (AND, OR, NOT)
- Straight quotes only (no curly)
- No wildcards
- No exceeded limits (15 operators, 2000 chars)
- Warns on stop words used as standalone keywords

Usage:
    python3 validate_boolean.py 'your boolean string'
    python3 validate_boolean.py --test
"""

import re
import sys

# Hard limits from LinkedIn docs
MAX_CHARS = 2000
MAX_OPERATORS = 15

# Stop words LinkedIn ignores (waste of operator budget if used)
STOP_WORDS = {"by", "in", "with", "the", "a", "an", "to", "for", "of", "on"}

# Curly quote characters (smart quotes)
CURLY_QUOTES = {"\u201c", "\u201d", "\u2018", "\u2019"}


class ValidationResult:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []

    @property
    def ok(self):
        return not self.errors

    def report(self):
        lines = []
        for e in self.errors:
            lines.append(f"  ERROR    {e}")
        for w in self.warnings:
            lines.append(f"  WARNING  {w}")
        for i in self.info:
            lines.append(f"  INFO     {i}")
        return "\n".join(lines) if lines else "  All checks passed."


def validate(query):
    result = ValidationResult()

    if not query or not query.strip():
        result.errors.append("Empty boolean string")
        return result

    # --- Length checks ---
    if len(query) > MAX_CHARS:
        result.errors.append(
            f"Query is {len(query)} chars, exceeds limit of {MAX_CHARS}. Split into two searches."
        )
    elif len(query) > MAX_CHARS * 0.8:
        result.warnings.append(
            f"Query is {len(query)} chars, approaching limit of {MAX_CHARS}."
        )

    # --- Curly quote detection ---
    for c in CURLY_QUOTES:
        if c in query:
            result.errors.append(
                f"Curly quote detected ({repr(c)}). LinkedIn only accepts straight quotes (\"). "
                "Replace all curly quotes — they silently break the query."
            )
            break

    # --- Balanced parens ---
    depth = 0
    for i, ch in enumerate(query):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                result.errors.append(f"Unbalanced parens: extra closing paren at position {i}.")
                break
    if depth > 0:
        result.errors.append(f"Unbalanced parens: {depth} opening paren(s) not closed.")

    # --- Balanced quotes ---
    quote_count = query.count('"')
    if quote_count % 2 != 0:
        result.errors.append(f"Unbalanced quotes: found {quote_count} (must be even).")

    # --- Wildcards ---
    if "*" in query or "?" in query:
        result.errors.append(
            "Wildcard detected (* or ?). LinkedIn does not support wildcards. "
            "Spell out variations with OR: (Manager OR Management OR Managing)."
        )

    # --- Lowercase operator detection ---
    # Look for lowercase 'and', 'or', 'not' surrounded by spaces (likely operators)
    # but be careful: this can match words like "AND" inside a quoted phrase.
    # We'll do a rough check by stripping quoted strings first.
    stripped = re.sub(r'"[^"]*"', '""', query)  # remove quoted content
    lowercase_op_pattern = re.compile(r"\b(and|or|not)\b")
    for match in lowercase_op_pattern.finditer(stripped):
        op = match.group(1)
        result.warnings.append(
            f"Lowercase '{op}' found. LinkedIn requires operators in UPPERCASE "
            f"({op.upper()}). Lowercase is treated as a search keyword, not an operator."
        )
        break  # one warning is enough

    # --- Operator count ---
    # Count uppercase AND, OR, NOT outside quoted strings
    operator_pattern = re.compile(r"\b(AND|OR|NOT)\b")
    operators = operator_pattern.findall(stripped)
    n_ops = len(operators)
    if n_ops > MAX_OPERATORS:
        result.errors.append(
            f"Too many operators: {n_ops} (limit is {MAX_OPERATORS}). LinkedIn may truncate or reject."
        )
    elif n_ops > MAX_OPERATORS * 0.7:
        result.warnings.append(
            f"Operator count high: {n_ops}/{MAX_OPERATORS}. Consider simplifying."
        )

    # --- Stop word as standalone term ---
    # Split on operators and parens to get terms; flag unquoted stop words used alone.
    tokens = re.split(r"\s+(?:AND|OR|NOT)\s+|\(|\)", stripped)
    for tok in tokens:
        tok = tok.strip()
        if not tok or tok == '""':
            continue
        # If the whole token is one of the stop words, warn
        if tok.lower() in STOP_WORDS:
            result.warnings.append(
                f"Stop word '{tok}' used as a standalone term. LinkedIn silently ignores these. "
                "Remove or include in a quoted phrase."
            )

    # --- Multi-word terms without quotes ---
    # Look for clusters of 2+ unquoted words between operators that aren't already in parens
    # This is heuristic — multi-word unquoted terms are usually unintentional.
    # Tokens with 2+ words but no quotes are suspicious.
    raw_tokens = re.split(r"\s+(?:AND|OR|NOT)\s+", query)
    for tok in raw_tokens:
        tok_clean = tok.strip().strip("()")
        if not tok_clean:
            continue
        # Skip if it contains quotes
        if '"' in tok_clean:
            continue
        # Count alpha words
        words = re.findall(r"[A-Za-z][A-Za-z'-]+", tok_clean)
        # Filter stop words (which are dropped anyway)
        meaningful = [w for w in words if w.lower() not in STOP_WORDS]
        if len(meaningful) >= 2:
            result.warnings.append(
                f"Multi-word term '{tok_clean.strip()}' not quoted. "
                "Multi-word phrases should be in straight quotes: \"Head of Sales\"."
            )
            break  # one warning suffices

    # --- Nesting depth ---
    max_depth = 0
    cur = 0
    for ch in query:
        if ch == "(":
            cur += 1
            max_depth = max(max_depth, cur)
        elif ch == ")":
            cur -= 1
    if max_depth > 4:
        result.warnings.append(
            f"Parenthesis nesting depth is {max_depth} (recommended max: 4). "
            "Deep nesting causes unpredictable behavior."
        )

    if not result.errors and not result.warnings:
        result.info.append(
            f"Valid boolean string. {n_ops} operator(s), {len(query)} char(s), depth {max_depth}."
        )

    return result


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------

TEST_CASES = [
    # (description, query, should_have_error, should_have_warning)
    ("Clean simple", '(CMO OR "Chief Marketing Officer") NOT Fractional', False, False),
    ("Lowercase or", "CMO or Founder", False, True),
    ("Curly quote", '\u201cCMO\u201d OR CRO', True, False),
    ("Unbalanced paren", "(CMO OR CRO", True, False),
    ("Extra closing paren", "CMO OR CRO)", True, False),
    ("Unbalanced quotes", '"Head of Sales OR Director', True, False),
    ("Wildcard", "Manag*", True, False),
    ("Stop word alone", "by AND CMO", False, True),
    ("Multi-word unquoted", "Head of Sales OR Director", False, True),
    ("Too many operators", " OR ".join([f"X{i}" for i in range(20)]), True, False),
    ("Clean complex", '("CMO" OR "VP Marketing" OR "Head of Marketing") AND (SaaS OR B2B) NOT (Fractional OR Intern)', False, False),
]


def run_tests():
    print("Running boolean validator tests...\n")
    passed = 0
    failed = 0
    for desc, query, want_err, want_warn in TEST_CASES:
        r = validate(query)
        has_err = bool(r.errors)
        has_warn = bool(r.warnings)
        ok = (has_err == want_err)
        # For warning expectations, we just check at least one warning if expected
        if want_warn and not has_warn:
            ok = False
        if ok:
            print(f"  PASS  {desc}")
            passed += 1
        else:
            print(f"  FAIL  {desc}")
            print(f"    Query: {query[:80]}{'...' if len(query) > 80 else ''}")
            print(f"    Expected error={want_err} warn={want_warn}, got error={has_err} warn={has_warn}")
            for e in r.errors:
                print(f"      err: {e}")
            for w in r.warnings:
                print(f"      warn: {w}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed.")
    return 0 if failed == 0 else 1


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if args[0] == "--test":
        return run_tests()

    query = " ".join(args)
    result = validate(query)
    print(f"Query: {query}")
    print(f"Length: {len(query)} chars")
    print()
    print(result.report())
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())
