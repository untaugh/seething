#!/usr/bin/python3

from pycparser import c_parser, c_ast, parse_file

class FuncDefVisitor(c_ast.NodeVisitor):

    jsCode = ''

    def visit_FuncDef(self, node):
        self.jsCode += ('funcs.push( new funcDef(\'%s\', %d));\n' % (node.decl.name, len(node.body.block_items)))

def getJsFuncDefs(filename):
    ast = parse_file(filename)
    v = FuncDefVisitor()
    v.visit(ast)
    return v.jsCode
