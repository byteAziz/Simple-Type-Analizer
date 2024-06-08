from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

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
    type: Optional[str] = None      # tipo que representan

class Void:
    pass
        
Tree = Node | Void

#-------------------------------- FUNCIONES DEL ARBOL --------------------------------

# dado una arbol, retorna el codigo para representar como un grafo usando DOT
def fromTreeToDotGraph(tree: Tree) -> str:
    # recorre el arbol de la forma adecuada para crear el grafo
    def traverse(node: Tree, dot_lines: list):
        if isinstance(node, Void):
            return
        if isinstance(node, Node):
            node_label = f'{node.symb}\n{node.type}'

            # mediante el identificador unico, definimos el texto de los vertices
            dot_lines.append(f'    {node.id} [label="{node_label}"];')
            
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

# dado un arbol y la tabla de simbolos prefefinida, retorna el arbol etiquetado
def labelTypes(tree: Tree, symbol_table: dict, temporal_types: dict = {}) -> None:
    # retorna la letra del abecedario correspondiente al numero
    def getLetterByNumber(number):
        return chr(ord('a') + number)

    if isinstance(tree, Node):
        if tree.symb in symbol_table:               # si esta en la tabla de tipos dada por el usuario
            tree.type = symbol_table[tree.symb]     

        elif tree.symb in temporal_types:           # si esta en la tabla de tipos unica del recorrido
            tree.type = temporal_types[tree.symb]      

        else:                                       # se asigna un nuevo tipo
            newType = getLetterByNumber(len(temporal_types))
            tree.type = newType
            if tree.symb in {'λ', '@'}:                             # si es una aplicacion o abstraccion, se guarda con
                temporal_types[f'{tree.symb}_{tree.id}'] = newType  # una llave unica para no repetir el tipo entre ellos
            else:                                       # si no lo es, se guarda el propio simbolo
                temporal_types[tree.symb] = newType     # para identificarlo en las proximas consultas

        labelTypes(tree.left, symbol_table, temporal_types)
        labelTypes(tree.right, symbol_table, temporal_types)

######################################################################################
############################## DEFINICION DEL VISITADOR ##############################
######################################################################################

class TreeVisitor(hmVisitor):
    def __init__(self, symbol_table):
        self.current_id = 0                 # identificador unico que se da a cada uno
        self.symbol_table = symbol_table    # tabla de simbolos hasta ahora, usado cuando se define un tipo

    # retorna un identificador nuevo unico
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
        return Node(self.next_id(), f"({operator})", Void(), Void())

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

#--------------------------- CONTROL DE INTERFAZ ESTATICA ----------------------------

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
                        help="Introduce la expresión y presiona *Enter* en tu teclado para enviarla"
                        )

#--------------------- CONTROL DE LA LOGICA E INTERFAZ DINAMICA ----------------------

input_stream = InputStream(stInput)
lexer = hmLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = hmParser(token_stream)
tree = parser.root()

# para no perder la tabla de simbolos cada vez que haya rerun de streamlit se usa session_state
if 'symbol_table' not in st.session_state:
    st.session_state['symbol_table'] = {}

if parser.getNumberOfSyntaxErrors() != 0:       # si hay errores de sintaxis se notifica
    st.error(f"{parser.getNumberOfSyntaxErrors()} error(s) de sintaxi.", icon="🚨")
else:                                           # en caso contrario se recorre el ast
    visitor = TreeVisitor(st.session_state['symbol_table'])
    result_tree = visitor.visit(tree)
    
    # se actualiza la tabla "recurrente" y se pinta con la funcion streamlit.table usando DataFrame de pandas
    st.session_state['symbol_table'] = visitor.symbol_table
    st.write("#### Contenido de la tabla de símbolos")
    symbol_table_data = [{"Símbolo": k, "Tipo": v} for k, v in st.session_state['symbol_table'].items()]
    symbol_table_df = pd.DataFrame(symbol_table_data)
    st.table(symbol_table_df)
    
    # en caso que haya sido una definicion de tipo (donde el visitador retorna Void()), no se imprime el arbol
    if isinstance(result_tree, Node):
        # en caso contrario, se etiquetan los nodos con sus tipos y se imprime con streamlit.graphviz_chart usando DOT
        labelTypes(result_tree, st.session_state['symbol_table'])
        graphviz_code = fromTreeToDotGraph(result_tree)
        st.graphviz_chart(graphviz_code)
