import streamlit as st

from antlr4 import *
from hmLexer import hmLexer
from hmParser import hmParser
from hmVisitor import hmVisitor

class TreeVisitor(hmVisitor):
    def __init__(self):
        self.nivell = 0

    def visitTermino(self, ctx: hmParser.TerminoContext):
        return super().visitTermino(ctx)
        

    def visitApplication(self, ctx: hmParser.ApplicationContext):
        return super().visitApplication(ctx)
        

    def visitAbstraction(self, ctx: hmParser.AbstractionContext):
        return super().visitAbstraction(ctx)
        

    def visitHighPrioOperator(self, ctx: hmParser.HighPrioOperatorContext):
        return super().visitHighPrioOperator(ctx)
        

    def visitLowPrioOperator(self, ctx: hmParser.LowPrioOperatorContext):
        return super().visitLowPrioOperator(ctx)
        

    def visitNumber(self, ctx: hmParser.NumberContext):
        return super().visitNumber(ctx)
        

    def visitVariable(self, ctx: hmParser.VariableContext):
        return super().visitVariable(ctx)
        

    def generate_graphviz(self, treeRoot):
        self.visit(treeRoot)
        return '''
                strict graph {
                    a -- b
                }
                '''        

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
    visitor = TreeVisitor()
    visitor.visit(tree)
    graphviz_code = visitor.generate_graphviz(tree)
    st.graphviz_chart(graphviz_code)

st.write(tree.toStringTree(recog=parser))