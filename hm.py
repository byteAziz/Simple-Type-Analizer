from __future__ import annotations
from dataclasses import dataclass

from antlr4 import *
from hmLexer import hmLexer
from hmParser import hmParser
from hmVisitor import hmVisitor

import streamlit as st

######################################################################################
################################ DEFINICIO DE L'ARBRE ################################
######################################################################################

@dataclass
class Node:
    id: int         # identificador unic del node
    symb: str
    left: Tree
    right: Tree

class Void:
    pass
        
Tree = Node | Void

# ---------------------------------- FUNCIONS D'ARBRE ----------------------------------

def fromTreeToDotGraph(tree: Tree) -> str:
    def node_id(node: Node) -> str:
        return f'"{node.id}_{node.symb}"'   # identificador unic d'un node en el graf

    def traverse(node: Tree, dot_lines: list):
        if isinstance(node, Void):
            return        
        if isinstance(node, Node):
            dot_lines.append(f'    {node_id(node)} [label="{node.symb}"];')
            if isinstance(node.left, Node):
                dot_lines.append(f'    {node_id(node)} -- {node_id(node.left)};')
                traverse(node.left, dot_lines)
            if isinstance(node.right, Node):
                dot_lines.append(f'    {node_id(node)} -- {node_id(node.right)};')
                traverse(node.right, dot_lines)

    dot_lines = ["strict graph {"]
    traverse(tree, dot_lines)
    dot_lines.append("}")
    return "\n".join(dot_lines)


######################################################################################
############################## DEFINICIO DEL VISITADOR ###############################
######################################################################################

class TreeVisitor(hmVisitor):
    def __init__(self):
        self.current_id = 0

    def next_id(self):
        self.current_id += 1
        return self.current_id

    def visitRoot(self, ctx:hmParser.RootContext):
        return self.visit(ctx.expr())

    def visitAbstraction(self, ctx:hmParser.AbstractionContext):
        variable = ctx.VARIABLE().getText()
        body = self.visit(ctx.expr())
        leftNode = Node(self.next_id(), variable, Void(), Void())
        return Node(self.next_id(), 'λ', leftNode, body)

    def visitApplicRecursive(self, ctx:hmParser.ApplicRecursiveContext):
        left = self.visit(ctx.application())
        right = self.visit(ctx.term())
        return Node(self.next_id(), '@', left, right)

    def visitApplicationBase(self, ctx:hmParser.ApplicationBaseContext):
        left = self.visit(ctx.term(0))
        right = self.visit(ctx.term(1))
        return Node(self.next_id(), '@', left, right)

    def visitParenExpr(self, ctx:hmParser.ParenExprContext):
        return self.visit(ctx.expr())

    def visitOperatorNP(self, ctx:hmParser.OperatorNPContext):
        operator = ctx.OPERATOR().getText()
        return Node(self.next_id(), operator, Void(), Void())

    def visitNumber(self, ctx:hmParser.NumberContext):
        number = ctx.NUMBER().getText()
        return Node(self.next_id(), number, Void(), Void())

    def visitVariable(self, ctx:hmParser.VariableContext):
        variable = ctx.VARIABLE().getText()
        return Node(self.next_id(), variable, Void(), Void())

   


######################################################################################
######################################## MAIN ########################################
######################################################################################



st.write("""
         # L'analitzador de tipus HinNer
         Projecte de llenguatjes de programació - Q2 2023-24
         ***
         Codigos de prueba para tener a mano:  
         2  
         x  
         (+) 2  
         \\x -> (+) 2 x  
         (\\x -> (+) 2 x) 4  
         (\\x -> (+) 2 x) ((\\y -> (+) 3 y) 6) 
         """)

stInput = st.text_input("Expressió", 
                        value=("Hola"),
                        help="Introdueix la teva expressió i prem *Enter* per a compilar-la"
                        )

input_stream = InputStream(stInput)
lexer = hmLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = hmParser(token_stream)
tree = parser.root()

if parser.getNumberOfSyntaxErrors() != 0:
    st.write(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
else:
    # sacar el arbol como grafo usando fromTreeToDotGraph y el visitador con la varibale 'tree'
    visitor = TreeVisitor()
    result_tree = visitor.visit(tree)
    
    graphviz_code = fromTreeToDotGraph(result_tree)
    st.graphviz_chart(graphviz_code)  


    # Estas lineas son de testeo, ignorar:
        # n6 = Node(3, "+", Void(), Void())
        # n7 = Node(3, "2", Void(), Void())
        # n4 = Node(2, "@", n6, n7)
        # n5 = Node(2, "x", Void(), Void())
        # n3 = Node(1, "@", n4, n5)
        # n2 = Node(1, "x", Void(), Void())
        # n1 = Node(0, "λ", n2, n3)
        # graphviz_code = fromTreeToDotGraph(n1)
        # st.graphviz_chart(graphviz_code)

st.write(tree.toStringTree(recog=parser))

# (root (expr (expr \ x -> (expr ( + ))) (expr x)))