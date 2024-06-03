import streamlit as st

from antlr4 import *
from hmLexer import hmLexer
from hmParser import hmParser
from hmVisitor import hmVisitor

class TreeVisitor(hmVisitor):

    def __init__(self):
        self.node_counter = 0
        self.edges = []
        self.nodes = []

    def get_new_node_id(self):
        self.node_counter += 1
        return f"node{self.node_counter}"

    def add_edge(self, from_node, to_node):
        self.edges.append((from_node, to_node))

    def visitTermino(self, ctx):
        node_id = self.get_new_node_id()
        self.nodes.append((node_id, "Term"))
        return node_id

    def visitApplication(self, ctx):
        node_id = self.get_new_node_id()
        self.nodes.append((node_id, "App"))
        for child in ctx.getChildren():
            child_id = self.visit(child)
            self.add_edge(node_id, child_id)
        return node_id

    def visitAbstraction(self, ctx):
        node_id = self.get_new_node_id()
        self.nodes.append((node_id, "Abs"))
        for child in ctx.getChildren():
            child_id = self.visit(child)
            self.add_edge(node_id, child_id)
        return node_id

    def visitHighPrioOperator(self, ctx):
        node_id = self.get_new_node_id()
        self.nodes.append((node_id, "HighPrioOp"))
        for child in ctx.getChildren():
            child_id = self.visit(child)
            self.add_edge(node_id, child_id)
        return node_id

    def visitLowPrioOperator(self, ctx):
        node_id = self.get_new_node_id()
        self.nodes.append((node_id, "LowPrioOp"))
        for child in ctx.getChildren():
            child_id = self.visit(child)
            self.add_edge(node_id, child_id)
        return node_id

    def visitNumber(self, ctx):
        node_id = self.get_new_node_id()
        self.nodes.append((node_id, ctx.getText()))
        return node_id

    def visitVariable(self, ctx):
        node_id = self.get_new_node_id()
        self.nodes.append((node_id, ctx.getText()))
        return node_id

    def generate_graphviz(self):
        result = ["strict graph {"]
        for node_id, label in self.nodes:
            result.append(f'    {node_id} [label="{label}"];')
        for from_node, to_node in self.edges:
            result.append(f'    {from_node} -- {to_node};')
        result.append("}")
        return "\n".join(result)

st.write("""
         # L'analitzador de tipus HinNer
         Projecte de llenguatjes de programació - Q2 2023-24
         ***
         Codigos de prueba para tener a mano:
         2  
         x  
         (+) 2  
         /x -> (+) 2 x  
         (/x -> (+) 2 x) 4  
         """)

stInput = st.text_input("Expressió", 
                        value=("Hola"),
                        help="Introdueix la teva expressió i prem *Enter* per a compilar-la"
                        )

input_stream = InputStream(stInput)
lexer = hmLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = hmParser(token_stream)
tree = parser.expr()

if parser.getNumberOfSyntaxErrors() != 0:
    st.write(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
else:
    visitor = TreeVisitor()
    visitor.visit(tree)
    graphviz_code = visitor.generate_graphviz()
    st.graphviz_chart(graphviz_code)

st.write(tree.toStringTree(recog=parser))