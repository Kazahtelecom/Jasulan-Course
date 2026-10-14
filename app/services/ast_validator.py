"""AST security validator for untrusted code execution."""

import ast

DISALLOWED_MODULES = frozenset({"os", "sys", "subprocess", "shutil", "socket"})
DISALLOWED_CALLS = frozenset({"eval", "exec", "__import__"})


class SecurityVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.errors: list[str] = []

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            base_module = alias.name.split(".")[0]
            if base_module in DISALLOWED_MODULES:
                self.errors.append(f"Forbidden module import: '{alias.name}'")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module:
            base_module = node.module.split(".")[0]
            if base_module in DISALLOWED_MODULES:
                self.errors.append(f"Forbidden module import: '{node.module}'")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name):
            if node.func.id in DISALLOWED_CALLS:
                self.errors.append(f"Forbidden function call: '{node.func.id}'")
        self.generic_visit(node)


class ASTValidator:
    """Performs static AST inspection of student code."""

    @classmethod
    def validate(cls, code: str) -> tuple[bool, str | None]:
        """Validate code syntax and security constraints.

        Returns:
            (True, None) if safe.
            (False, error_message) if syntax error or security violation.
        """
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"Syntax error at line {e.lineno}: {e.msg}"

        visitor = SecurityVisitor()
        visitor.visit(tree)

        if visitor.errors:
            return False, "; ".join(visitor.errors)

        return True, None
