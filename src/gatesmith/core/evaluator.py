"""Expression evaluator for AST nodes."""

from __future__ import annotations

from gatesmith.core.ast import And, Const, Expression, Not, Or, Var, Xor


def evaluate(node: Expression, assignment: dict[str, bool]) -> bool:
    """Recursively evaluate `node` under `assignment`.

    `assignment` must provide boolean values for any variables referenced
    by `node`.

    Returns the computed boolean result.
    """

    if isinstance(node, Var):
        return bool(assignment[node.name])
    if isinstance(node, Const):
        return node.value
    if isinstance(node, Not):
        return not evaluate(node.node, assignment)
    if isinstance(node, And):
        return all(evaluate(child, assignment) for child in node.nodes)
    if isinstance(node, Or):
        return any(evaluate(child, assignment) for child in node.nodes)
    if isinstance(node, Xor):
        result = False
        for child in node.nodes:
            result ^= evaluate(child, assignment)
        return result
    raise TypeError(f"Unsupported expression node: {type(node)!r}")
