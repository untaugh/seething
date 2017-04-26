#!/usr/bin/python3

from pycparser import c_parser, c_ast, parse_file

class FuncDefVisitor(c_ast.NodeVisitor):

    jsCode = ''

    def visit_FuncDef(self, node):
        self.jsCode += ('funcs.push( new funcDef(\'%s\', %d));\n' % (node.decl.name, len(node.body.block_items)))
        self.visit(node.body)
    def visit_FuncCall(self, node):
        self.jsCode += ('funcs[funcs.length - 1].calls.push(\'%s\');\n' % (node.name.name))

def getJsFuncDefs(filename):
    ast = parse_file(filename)
    v = FuncDefVisitor()
    v.visit(ast)
    return v.jsCode
