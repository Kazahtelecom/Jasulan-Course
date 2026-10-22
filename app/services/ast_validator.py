"""AST security validator for untrusted code execution."""

from __future__ import annotations

import ast

MAX_CODE_SIZE_BYTES = 15 * 1024  # 15 KB strict limit

ALLOWED_MODULES = frozenset({
    "math",
    "typing",
    "abc",
    "random",
    "datetime",
    "decimal",
    "fractions",
    "copy",
    "collections",
    "itertools",
    "functools",
    "string",
    "enum",
    "dataclasses",
})

DISALLOWED_MODULES = frozenset({
    "os",
    "sys",
    "subprocess",
    "shutil",
    "socket",
    "importlib",
    "pathlib",
    "ctypes",
    "builtins",
    "posix",
    "nt",
    "io",
    "urllib",
    "requests",
    "http",
    "inspect",
    "pickle",
    "shelve",
    "marshal",
    "threading",
    "multiprocessing",
    "signal",
    "asyncio",
})

DISALLOWED_CALLS = frozenset({
    "eval",
    "exec",
    "__import__",
    "open",
    "compile",
    "getattr",
    "setattr",
    "delattr",
    "globals",
    "locals",
    "vars",
    "dir",
    "breakpoint",
    "memoryview",
    "input",
})

ALLOWED_MAGIC_METHODS = frozenset({
    "__init__",
    "__str__",
    "__repr__",
    "__eq__",
    "__ne__",
    "__lt__",
    "__gt__",
    "__le__",
    "__ge__",
    "__len__",
    "__getitem__",
    "__setitem__",
    "__delitem__",
    "__iter__",
    "__next__",
    "__contains__",
    "__add__",
    "__sub__",
    "__mul__",
    "__truediv__",
    "__floordiv__",
    "__mod__",
    "__pow__",
    "__enter__",
    "__exit__",
    "__call__",
    "__hash__",
    "__bool__",
    "__format__",
})

ALLOWED_NODE_TYPES = (
    ast.Module,
    ast.Interactive,
    ast.Expression,
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.ClassDef,
    ast.Return,
    ast.Delete,
    ast.Assign,
    ast.AugAssign,
    ast.AnnAssign,
    ast.For,
    ast.AsyncFor,
    ast.While,
    ast.If,
    ast.With,
    ast.AsyncWith,
    ast.Match,
    ast.match_case,
    ast.MatchValue,
    ast.MatchSingleton,
    ast.MatchSequence,
    ast.MatchMapping,
    ast.MatchClass,
    ast.MatchStar,
    ast.MatchAs,
    ast.MatchOr,
    ast.Raise,
    ast.Try,
    ast.Assert,
    ast.Import,
    ast.ImportFrom,
    ast.Global,
    ast.Nonlocal,
    ast.Expr,
    ast.Pass,
    ast.Break,
    ast.Continue,
    ast.BoolOp,
    ast.NamedExpr,
    ast.BinOp,
    ast.UnaryOp,
    ast.Lambda,
    ast.IfExp,
    ast.Dict,
    ast.Set,
    ast.ListComp,
    ast.SetComp,
    ast.DictComp,
    ast.GeneratorExp,
    ast.Await,
    ast.Yield,
    ast.YieldFrom,
    ast.Compare,
    ast.Call,
    ast.FormattedValue,
    ast.JoinedStr,
    ast.Constant,
    ast.Attribute,
    ast.Subscript,
    ast.Starred,
    ast.Name,
    ast.List,
    ast.Tuple,
    ast.Slice,
    ast.Load,
    ast.Store,
    ast.Del,
    ast.And,
    ast.Or,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.MatMult,
    ast.Div,
    ast.Mod,
    ast.Pow,
    ast.LShift,
    ast.RShift,
    ast.BitOr,
    ast.BitXor,
    ast.BitAnd,
    ast.FloorDiv,
    ast.Invert,
    ast.Not,
    ast.UAdd,
    ast.USub,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.Is,
    ast.IsNot,
    ast.In,
    ast.NotIn,
    ast.comprehension,
    ast.ExceptHandler,
    ast.arguments,
    ast.arg,
    ast.keyword,
    ast.alias,
    ast.withitem,
)


class SecurityVisitor(ast.NodeVisitor):
    """Enforces strict AST whitelist and exploit protections."""

    def __init__(self) -> None:
        self.errors: list[str] = []

    def visit(self, node: ast.AST) -> None:
        if not isinstance(node, ALLOWED_NODE_TYPES):
            self.errors.append(f"Forbidden syntax element: '{type(node).__name__}'")
            return
        super().visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            base_module = alias.name.split(".")[0]
            if base_module in DISALLOWED_MODULES or base_module not in ALLOWED_MODULES:
                self.errors.append(f"Forbidden module import: '{alias.name}'")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module:
            base_module = node.module.split(".")[0]
            if base_module in DISALLOWED_MODULES or base_module not in ALLOWED_MODULES:
                self.errors.append(f"Forbidden module import: '{node.module}'")
        else:
            self.errors.append("Relative imports are forbidden")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name):
            if node.func.id in DISALLOWED_CALLS:
                self.errors.append(f"Forbidden function call: '{node.func.id}'")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if node.attr.startswith("__"):
            if node.attr not in ALLOWED_MAGIC_METHODS:
                self.errors.append(f"Forbidden system attribute access: '{node.attr}'")
        elif node.attr in {"_getframe", "_as_parameter_", "_fields_"}:
            self.errors.append(f"Forbidden system attribute access: '{node.attr}'")
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        if node.id.startswith("__") and node.id not in ALLOWED_MAGIC_METHODS:
            self.errors.append(f"Forbidden system identifier: '{node.id}'")
        self.generic_visit(node)


class ASTValidator:
    """Performs static AST inspection of student code."""

    @classmethod
    def validate(cls, code: str) -> tuple[bool, str | None]:
        """Validate code syntax and security constraints.

        Returns:
            (True, None) if safe.
            (False, error_message) if syntax error, size overflow or security violation.
        """
        code_bytes = code.encode("utf-8")
        if len(code_bytes) > MAX_CODE_SIZE_BYTES:
            return (
                False,
                f"Code size exceeds maximum limit of 15 KB ({len(code_bytes)} bytes > {MAX_CODE_SIZE_BYTES} bytes)",
            )

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"Syntax error at line {e.lineno}: {e.msg}"

        visitor = SecurityVisitor()
        visitor.visit(tree)

        if visitor.errors:
            return False, "; ".join(visitor.errors)

        return True, None
