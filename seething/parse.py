#!/usr/bin/python3

from pycparser import c_parser, c_ast, parse_file
from json import JSONEncoder
from pathlib import Path
import inspect
import subprocess
import re

class visitorJson(c_ast.NodeVisitor):

    tree = { 'children' : [] }
    branch = tree

    def json(self):
        return JSONEncoder().encode(self.tree)

    def getStrings(self, node, dout):
        for (v,k) in inspect.getmembers(node):
            if isinstance(k,str) and not v.startswith('__'):
                dout[v] = str(k)

    def generic_visit(self, node):
        parent = self.branch
        current = { 'type' : node.__class__.__name__ , 'children' : [] }
        self.getStrings(node, current)
        if hasattr(node, 'decl'):
            if isinstance(node.decl, c_ast.Decl):
                self.getStrings(node.decl, current)
        parent['children'].append(current)
        self.branch = current
        for c_name, c in node.children():
            self.visit(c)
        self.branch = parent

class FuncDefVisitor(c_ast.NodeVisitor):

    jsCode = ''

    def visit_FuncDef(self, node):
        self.jsCode += ('funcs.push( new funcDef(\'%s\', %d));\n' % (node.decl.name, len(node.body.block_items)))
        self.visit(node.body)
    def visit_FuncCall(self, node):
        self.jsCode += ('funcs[funcs.length - 1].calls.push(\'%s\');\n' % (node.name.name))

def objToJson(objfile):

    file = Path(objfile)

    if not file.exists():
        print('Cannot find %s.' % (file))
        return ''

    result = subprocess.run(['objdump','-d',file.as_posix()], stdout=subprocess.PIPE)

    fdef = re.compile('[0-9a-f]+ <[\w]+>:')
    fdefname= re.compile('(?<=<)[\w]+(?=>:)')
    fcall = re.compile('\s+[0-9a-z]+:\s+([0-9a-f]{2}\s+){5}callq\s+[0-9a-z]+\s+<\w+>')
    fcallname= re.compile('(?<=<)[\w]+')

    tree = { 'children' : [] }

    for l in result.stdout.decode().splitlines():
        if fdef.match(l):
            name = fdefname.search(l).group(0)
            if not name.startswith('_'):
                node = { 'type':'FuncDef', 'name' : name, 'children' : [] }
                tree['children'].append(node)
                nownode = node
        if fcall.match(l):
            name = fcallname.search(l).group(0)
            node = { 'type':'FuncCall', 'name' : name, 'children' : [] }
            nownode['children'].append(node)

    json = JSONEncoder().encode(tree)
    return json

def parseJson(infile, outfile):
    out = Path(outfile)
    with out.open('w') as f:
        ast = parse_file(infile)
        v = visitorJson()
        v.visit(ast)
        f.write(v.json())

def getJsFuncDefs(filename):
    ast = parse_file(filename)
    v = FuncDefVisitor()
    v.visit(ast)
    return v.jsCode
