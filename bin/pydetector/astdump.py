#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__description__ = """
Script to dump to stdout or export as JSON/msgpack the AST of Python
modules.
"""
__author__ = 'Juanjo Alvarez <juanjo@sourced.tech>'

import ast
import sys
import json


class DictVisitor:
    ast_type_field = "_ast_type"

    def __init__(self):
        self.type2method = {
            'field': {
                '_DEFAULT': self.visit_field_default,
                'NameConstant': self.visit_constant_value,
                'Num': self.visit_numeric_literal,
                'Str': self.visit_str_literal,
            },
            'attribute': {
                '_DEFAULT': self.visit_field_default,
            },
            'other': {
                '_DEFAULT': self.visit_default,
                'Str': self.visit_str_literal,
            }
        }


    def method_match(self, node, subtype):
        """
        Find the right method or default visitor method for the given node
        and sub field. This uses the self.types2method dictionary
        for matching specific types
        """
        node_type = node.__class__.__name__
        t2m = self.type2method

        visitor_group = t2m.get(subtype, t2m['other'])
        visitor = visitor_group.get(node_type, visitor_group['_DEFAULT'])
        return visitor

    def visit(self, node):
        return self.method_match(node, 'other')(node)

    def visit_default(self, node):
        print('XXX node: {}'.format(node))
        print(node.__dict__)
        node_type = node.__class__.__name__
        # Add node type
        args = {}
        args[self.ast_type_field] = node_type

        # Visit fields
        for field in node._fields:
            field_visitor = self.method_match(node, 'field')
            args[field] = field_visitor(getattr(node, field))

        # Visit attributes
        for attr in node._attributes:
            attr_visitor = self.method_match(node, 'attribute')
            args[attr] = attr_visitor(getattr(node, attr, None))
        return args

    def visit_field_default(self, val):
        res = None
        if isinstance(val, ast.AST):
            res = self.visit(val)
        elif isinstance(val, list) or isinstance(val, tuple):
            res = [self.visit(x) for x in val]
        else:
            res = val

        return res

    def visit_constant_value(self, val):
        return str(val)

    def visit_str_literal(self, val):
        return dict(_ast_type = "string", value = val.__dict__)

    def visit_numeric_literal(self, val):
        if isinstance(val, int):
            return dict(_ast_type = "int", value = val)
        elif isinstance(val, float):
            return dict(_ast_type = "float", value = val)
        elif isinstance(val, complex):
            return dict(
                _ast_type = "complex",
                realvalue = val.real,
                imaginaryvalue = val.imag
            )

def as_dict(tree):
    return DictVisitor().visit(tree)

def as_json(tree, pretty_print=False):
    return json.dumps(
        as_dict(tree),
        indent=4 if pretty_print else None,
        sort_keys=True,
        separators=(",", ": ") if pretty_print else (",", ":")
    )


if __name__ == '__main__':
    import optparse

    parser = optparse.OptionParser(usage="%prog [options] <filename.py>",
            description=__description__)
    opts, args = parser.parse_args()

    if len(args) == 0:
        parser.print_help()
        sys.exit(-1)
    filename = args[0]

    with open(filename, 'r') as code:
        root = ast.parse(code.read())

    print(as_json(root, True))
