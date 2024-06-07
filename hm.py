from __future__ import annotations
from dataclasses import dataclass

from antlr4 import InputStream, CommonTokenStream
from hmLexer import hmLexer
from hmParser import hmParser
from hmVisitor import hmVisitor

import streamlit as st
import pandas as pd

######################################################################################
################################ DEFINICION DEL ARBOL ################################
######################################################################################

@dataclass
class Node:
    id: int         # identificador unico del nodo
    symb: str       # simbolo que representa el nodo
    left: Tree
    right: Tree

class Void:
    pass
        
Tree = Node | Void

#-------------------------------- FUNCIONES DEL ARBOL --------------------------------

def fromTreeToDotGraph(tree: Tree) -> str:
    # recorre el arbol de la forma adecuada para crear el grafo
    def traverse(node: Tree, dot_lines: list):
        if isinstance(node, Void):
            return
        if isinstance(node, Node):
            # mediante el identificador unico, definimos el texto de los vertices
            dot_lines.append(f'    {node.id} [label="{node.symb}"];')
            
            # se crean las aristas en orden
            if isinstance(node.left, Node):
                dot_lines.append(f'    {node.id} -- {node.left.id};')
                traverse(node.left, dot_lines)
            if isinstance(node.right, Node):
                dot_lines.append(f'    {node.id} -- {node.right.id};')
                traverse(node.right, dot_lines)

    # se escribe la sintaxis en DOT para crear el grafo mediante el recorrido
    dot_lines = ["strict graph {"]
    traverse(tree, dot_lines)
    dot_lines.append("}")
    return "\n".join(dot_lines)


######################################################################################
############################## DEFINICION DEL VISITADOR ##############################
######################################################################################

class TreeVisitor(hmVisitor):
    def __init__(self, symbol_table):
        self.current_id = 0                 # identificador unico que se da a cada uno
        self.symbol_table = symbol_table    # tabla de simbolos hasta ahora

    # Retorna un identificador nuevo unico
    def next_id(self):
        self.current_id += 1
        return self.current_id

    # root : expr
    def visitRoot(self, ctx:hmParser.RootContext):
        return self.visit(ctx.expr())
	
    # typeDefinition : term '::' type
    def visitTypeDefinition(self, ctx: hmParser.TypeDefinitionContext):
        term = ctx.term().getText()
        type_expr = ctx.type_().getText()
        self.symbol_table[term] = type_expr
        return Void()
    
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

    # term: '(' expr ')'                # ParenExpr
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
         # El analizador de tipos HinNer
         #### Proyecto de lenguajes de programación - Q2 2023/24
         ***
         Códigos de prueba para tener a mano:  
         ```
         2  
         x  
         (+) 2  
         \\x -> (+) 2 x  
         (\\x -> (+) 2 x) 4  
         ((\\x -> (+) 2 x) ((\\y -> (+) 3 y) 6))  
         2 :: N  
         (+) :: N -> N -> N
         ```  
         """)

stInput = st.text_input("Entrada", 
                        value="Ejemplo",
                        help="Introduce la expresión y presiona *Enter* en tu teclado para compilarla"
                        )

input_stream = InputStream(stInput)
lexer = hmLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = hmParser(token_stream)
tree = parser.root()

# Para no perder la tabla de simbolos cada vez que haya rerun de streamlit se usa session_state
if 'symbol_table' not in st.session_state:
    st.session_state['symbol_table'] = {}

if parser.getNumberOfSyntaxErrors() != 0:
    st.error(f"{parser.getNumberOfSyntaxErrors()} error(s) de sintaxi.", icon="🚨")
else:
    visitor = TreeVisitor(st.session_state['symbol_table'])
    result_tree = visitor.visit(tree)
    
    st.session_state['symbol_table'] = visitor.symbol_table
    st.write("#### Contenido de la tabla de símbolos")
    symbol_table_data = [{"Símbolo": k, "Tipo": v} for k, v in st.session_state['symbol_table'].items()]
    symbol_table_df = pd.DataFrame(symbol_table_data)
    st.table(symbol_table_df)
    
    # En caso que haya sido una definicion de tipo (donde el visitador retorna Void()), no se imprime el arbol
    if isinstance(result_tree, Node):
        graphviz_code = fromTreeToDotGraph(result_tree)
        st.graphviz_chart(graphviz_code)


st.write(tree.toStringTree(recog=parser))