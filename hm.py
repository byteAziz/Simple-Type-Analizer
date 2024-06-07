from __future__ import annotations
from dataclasses import dataclass

from antlr4 import InputStream, CommonTokenStream
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
    symb: str       # simbol que representa el node
    left: Tree
    right: Tree

class Void:
    pass
        
Tree = Node | Void

# ---------------------------------- FUNCIONS D'ARBRE ----------------------------------

def fromTreeToDotGraph(tree: Tree) -> str:
    def traverse(node: Tree, dot_lines: list):
        if isinstance(node, Void):
            return        
        if isinstance(node, Node):
            dot_lines.append(f'    {node.id} [label="{node.symb}"];')
            if isinstance(node.left, Node):
                dot_lines.append(f'    {node.id} -- {node.left.id};')
                traverse(node.left, dot_lines)
            if isinstance(node.right, Node):
                dot_lines.append(f'    {node.id} -- {node.right.id};')
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

    # Retorna un identificador unic
    def next_id(self):
        self.current_id += 1
        return self.current_id

    # root : expr
    def visitRoot(self, ctx:hmParser.RootContext):
        return self.visit(ctx.expr())

    # abstraction : '\\' VARIABLE '->' expr;
    def visitAbstraction(self, ctx:hmParser.AbstractionContext):
        variable = ctx.VARIABLE().getText()
        left = Node(self.next_id(), variable, Void(), Void())
        right = self.visit(ctx.expr())
        return Node(self.next_id(), 'λ', left, right)

    # application : application term    # ApplicRecursive
    def visitApplicRecursive(self, ctx:hmParser.ApplicRecursiveContext):
        left = self.visit(ctx.application())
        right = self.visit(ctx.term())
        return Node(self.next_id(), '@', left, right)

    # application : term term           # ApplicationBase
    def visitApplicationBase(self, ctx:hmParser.ApplicationBaseContext):
        left = self.visit(ctx.term(0))
        right = self.visit(ctx.term(1))
        return Node(self.next_id(), '@', left, right)
    
    def visitParenExpr(self, ctx:hmParser.ParenExprContext):
        return self.visit(ctx.expr())

    # term : '(' OPERATOR ')'           # OperatorNP
    def visitOperatorNP(self, ctx:hmParser.OperatorNPContext):
        operator = ctx.OPERATOR().getText()
        return Node(self.next_id(), operator, Void(), Void())

    # term : NUMBER                     # Number
    def visitNumber(self, ctx:hmParser.NumberContext):
        number = ctx.NUMBER().getText()
        return Node(self.next_id(), number, Void(), Void())

    # term : VARIABLE                   # Variable
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
         ((\\x -> (+) 2 x) ((\\y -> (+) 3 y) 6))  
         2 :: N  
         (+) :: N -> N -> N  
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
    st.error(f"{parser.getNumberOfSyntaxErrors()} error(s) de sintaxi.", icon="🚨")
else:
    visitor = TreeVisitor()
    result_tree = visitor.visit(tree)
    
    graphviz_code = fromTreeToDotGraph(result_tree)
    st.graphviz_chart(graphviz_code)  

st.write(tree.toStringTree(recog=parser))
