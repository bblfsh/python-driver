# Modified from: https://github.com/fpoli/python-astexport/blob/master/astexport/export.py
# Changes: sorting order, add comment nodes, msgpack export

import ast
import json # TODO: try with ujson
import msgpack

def export_dict(tree):
    return DictExportVisitor().visit(tree)

def export_json(tree, pretty_print=False):
    return json.dumps(
        export_dict(tree),
        indent=2 if pretty_print else 0,
        ensure_ascii=False
    )

def export_msgpack(tree):
    return msgpack.packb(export_json(tree))

class DictExportVisitor:
    ast_type_field = "ast_type"

    def visit(self, node):
        node_type = node.__class__.__name__
        meth = getattr(self, "visit_" + node_type, self.default_visit)
        return meth(node)

    def default_visit(self, node):
        node_type = node.__class__.__name__
        # Add node type
        args = {
            self.ast_type_field: node_type
        }
        # Visit fields
        for field in node._fields:
            meth = getattr(
                self, "visit_field_" + node_type + "_" + field,
                self.default_visit_field
            )
            args[field] = meth(getattr(node, field))
        # Visit attributes
        for attr in node._attributes:
            meth = getattr(
                self, "visit_attribute_" + node_type + "_" + attr,
                self.default_visit_field
            )
            # Use None as default when lineno/col_offset are not set
            args[attr] = meth(getattr(node, attr, None))
        return args

    def default_visit_field(self, val):
        if isinstance(val, ast.AST):
            return self.visit(val)
        elif isinstance(val, list) or isinstance(val, tuple):
            return [self.visit(x) for x in val]
        else:
            return val

    # Special visitors

    def visit_str(self, val):
        return str(val)

    def visit_NoneType(self, val):
        return None

    def visit_field_NameConstant_value(self, val):
        return str(val)

    def visit_field_Num_n(self, val):
        if isinstance(val, int):
            return {
                self.ast_type_field: "int",
                "n": val
            }
        elif isinstance(val, float):
            return {
                self.ast_type_field: "float",
                "n": val
            }
        elif isinstance(val, complex):
            return {
                self.ast_type_field: "complex",
                "n": val.real,
                "i": val.imag
            }


if __name__ == '__main__':
    import sys
    f = sys.argv[1]

    print(export_json(ast.parse(open(f).read()), pretty_print=True))
