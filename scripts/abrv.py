import ast
import astor
import sys


class OmitBodies(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        if node.name.startswith("_"):
            return None  # Remove functions starting with _
        self.generic_visit(node)
        new_body = []
        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            new_body.append(node.body[0])
        new_body.append(ast.Expr(value=ast.Constant(value=Ellipsis)))
        node.body = new_body
        return node

    def visit_AsyncFunctionDef(self, node):
        if node.name.startswith("_"):
            return None  # Remove async functions starting with _
        self.generic_visit(node)
        new_body = []
        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            new_body.append(node.body[0])
        new_body.append(ast.Expr(value=ast.Constant(value=Ellipsis)))
        node.body = new_body
        return node


def omit_function_bodies():
    source = sys.stdin.read()
    tree = ast.parse(source)
    tree = OmitBodies().visit(tree)
    ast.fix_missing_locations(tree)
    new_source = astor.to_source(tree)
    sys.stdout.write(new_source)


if __name__ == "__main__":
    omit_function_bodies()
