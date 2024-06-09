from __future__ import annotations
from dataclasses import dataclass

from antlr4 import InputStream, CommonTokenStream
from hmLexer import hmLexer
from hmParser import hmParser
from hmVisitor import hmVisitor

import streamlit as st
import pandas as pd


# ################################################################################## #
# ########################## DECLARACION DE  EXCEPCIONES ########################### #
# ################################################################################## #


class TipoNoDefinido(Exception):
    def __init__(self, simbolo: str):
        self.simbolo = simbolo
        self.message = f"El tipo del simbolo ```{simbolo}``` no ha sido definido."
        super().__init__(self.message)


class InconsistenciaDeTipos(Exception):
    def __init__(self, aplicacion_o_abstraccion: str, tipo1: str, tipo2: str):
        self.aplicacion_o_abstraccion = aplicacion_o_abstraccion
        self.tipo1 = tipo1
        self.tipo2 = tipo2
        self.message = f"Ha habido un error al inferir en una {aplicacion_o_abstraccion} con los siguientes tipos: ```{tipo1}``` vs ```{tipo2}```."
        super().__init__(self.message)


class AplicacionImposible(Exception):
    def __init__(self):
        self.message = "Se ha superado el maximo de tipos admitidos sobre una aplicación."
        super().__init__(self.message)


# ################################################################################## #
# ######################### CONVERSION DE FORMATO DE TIPOS ######################### #
# ################################################################################## #


# Durante el manejo del programa, los tipos se consideran str, y existen tres formatos diferentes:
# 1. inputFormat: El que se recibe del usuario dado por la gramatica: "A -> B -> C"
# 2. basicFormat: El que se usa para inferir los tipos para un manejo simple: "ABC"
# 3. outputFormat: El que se muestra al usuario: "(A -> (B -> C))"

# Pasa del formato de entrada al formato de salida: de "A -> B -> C" a "(A -> (B -> C))"
def fromInputToOutputFormat(type_expr: str) -> str:
    types = type_expr.split('->')
    if len(types) == 1:
        return f'{type_expr.strip()}'

    result = types[-1].strip()
    for part in reversed(types[:-1]):
        result = f'({part.strip()} -> {result})'
    return result


# Pasa del formato de salida al formato basico: de "(A -> (B -> C))" a "ABC"
def fromOutputToBasicFormat(type_expr: str) -> str:
    types = type_expr.split('->')
    for i in range(len(types)):
        types[i] = types[i].strip("() ")
    return "".join(types)


# Pasa del formato basico al formato de salida: de "ABC" a "(A -> (B -> C))"
def fromBasicToOutputFormat(type_expr: str) -> str:
    types = list(type_expr)
    if len(types) == 1:
        return f'{type_expr}'

    result = types[-1]
    for part in reversed(types[:-1]):
        result = f'({part} -> {result})'
    return result


# ################################################################################## #
# ############################## DEFINICION DEL ARBOL ############################## #
# ################################################################################## #


@dataclass
class Node:
    id: int         # identificador unico del nodo
    symb: str       # simbolo que representa el nodo
    left: Tree
    right: Tree
    type: str = ""              # tipo que representan
    hasDefType: bool = False    # indica si el tipo es definitivo, es decir, declarado por el usuario o inferido


class Void:
    pass


Tree = Node | Void


# ------------------------------- FUNCIONES DEL ARBOL ------------------------------ #

# dado una arbol, retorna el codigo para representar como un grafo usando DOT
def fromTreeToDotGraph(tree: Tree) -> str:
    # recorre el arbol de la forma adecuada para crear el grafo
    def traverse(node: Tree, dotLines: list):
        if isinstance(node, Node):
            node_label = f'{node.symb}\n{node.type}'

            # mediante el identificador unico, definimos el texto de los vertices
            dotLines.append(f'    {node.id} [label="{node_label}"];')

            # se crean las aristas en orden
            if isinstance(node.left, Node):
                dotLines.append(f'    {node.id} -- {node.left.id};')
                traverse(node.left, dotLines)
            if isinstance(node.right, Node):
                dotLines.append(f'    {node.id} -- {node.right.id};')
                traverse(node.right, dotLines)

    # se escribe la sintaxis en DOT para crear el grafo mediante el recorrido
    dotLines = ["strict graph {"]
    traverse(tree, dotLines)
    dotLines.append("}")
    return "\n".join(dotLines)


# dado un arbol y la tabla de simbolos prefefinida, retorna el arbol etiquetado y asigna nuevos tipos a los desconocidos
def labelTypes(tree: Tree, symbol_table: dict, temporal_types: dict = {}) -> None:
    # retorna la letra del abecedario correspondiente al numero
    def getLetterByNumber(number):
        return chr(ord('a') + number)

    if isinstance(tree, Node):
        if tree.symb in symbol_table:               # si esta en la tabla de tipos dada por el usuario
            tree.type = symbol_table[tree.symb]
            tree.hasDefType = True

        elif tree.symb in temporal_types:           # si esta en la tabla de tipos unica del recorrido
            tree.type = temporal_types[tree.symb]

        else:                                       # se asigna un nuevo tipo
            newType = getLetterByNumber(len(temporal_types))        # se asigna una letra del abecedario
            tree.type = newType
            if tree.symb in {'λ', '@'}:                             # si es una aplicacion o abstraccion, se guarda con
                temporal_types[f'{tree.symb}_{tree.id}'] = newType  # una llave unica para no repetir el tipo entre ellos
            else:                                       # si no lo es, se guarda el propio simbolo
                temporal_types[tree.symb] = newType     # para identificarlo en las proximas consultas

        labelTypes(tree.left, symbol_table, temporal_types)
        labelTypes(tree.right, symbol_table, temporal_types)


# dado un arbol, infiere los tipos de las aplicaciones y abstracciones
# en caso de error, lanza una excepcion correspondiente
def inferTypes(tree: Tree, tiposInferidos: dict) -> None:
    if isinstance(tree, Node):
        inferTypes(tree.left, tiposInferidos)
        inferTypes(tree.right, tiposInferidos)

        if not tree.hasDefType and isinstance(tree.left, Node) and isinstance(tree.right, Node):
            leftBasicType = fromOutputToBasicFormat(tree.left.type)
            rightBasicType = fromOutputToBasicFormat(tree.right.type)

            # ------ Inferencia de aplicaciones ------ #

            if tree.symb == '@':
                if not tree.left.hasDefType:                    # si el tipo de la izquierda no esta definido
                    raise TipoNoDefinido(tree.left.symb)

                if len(leftBasicType) == 1:                     # de la forma "(N)" por lo que no se puede aplicar
                    raise AplicacionImposible()

                if tree.right.hasDefType:                       # si el tipo de la derecha esta definido
                    if leftBasicType[0] != rightBasicType[0]:   # pero no coincide con el de la izquierda
                        raise InconsistenciaDeTipos("aplicación", leftBasicType[0], rightBasicType[0])

                else:                                   # si no esta definido, se asigna el primer tipo de la izquierda
                    tiposInferidos[tree.right.type] = f"{fromBasicToOutputFormat(leftBasicType[0])}"
                    tree.right.type = f"{fromBasicToOutputFormat(leftBasicType[0])}"
                    tree.right.hasDefType = True

                # a la aplicacion se le asigna el tipo de la derecha a partir del segundo tipo del de la izquierda
                tiposInferidos[tree.type] = f"{fromBasicToOutputFormat(leftBasicType[1:])}"
                tree.type = f"{fromBasicToOutputFormat(leftBasicType[1:])}"
                tree.hasDefType = True

            # ------ Inferencia de abstracciones ------ #

            if tree.symb == 'λ':
                if not tree.right.hasDefType:               # si el tipo de la derecha no esta definido
                    raise TipoNoDefinido(tree.right.symb)

                if not tree.left.hasDefType:                            # si el tipo de la izquierda no esta definido
                    if tree.left.type not in tiposInferidos:                # si no esta en la tabla de tipos inferidos
                        raise TipoNoDefinido(tree.left.symb)                # se lanza una excepcion
                    else:                                               # si esta en la tabla de tipos inferidos
                        tree.left.type = tiposInferidos[tree.left.type]     # se asigna el tipo inferido
                        tree.left.hasDefType = True
                        leftBasicType = fromOutputToBasicFormat(tree.left.type)

                # a la abstraccion se le asigna el tipo del de la izquierda con una flecha al tipo del de la derecha
                treeBasicType = leftBasicType + rightBasicType
                tiposInferidos[tree.type] = f"{fromBasicToOutputFormat(treeBasicType)}"
                tree.type = f"{fromBasicToOutputFormat(treeBasicType)}"
                tree.hasDefType = True


# ################################################################################## #
# ############################ DEFINICION DEL VISITADOR ############################ #
# ################################################################################## #


class TreeVisitor(hmVisitor):
    def __init__(self, symbol_table):
        self.current_id = 0                 # identificador unico que se da a cada uno
        self.symbol_table = symbol_table    # tabla de simbolos accareada en tota la sesion, usada cuando se define un tipo

    # retorna un identificador unico nuevo
    def next_id(self):
        self.current_id += 1
        return self.current_id

    # root : expr
    def visitRoot(self, ctx: hmParser.RootContext):
        return self.visit(ctx.expr())

    # typeDefinition : asignable '::' typeExpr
    def visitTypeDefinition(self, ctx: hmParser.TypeDefinitionContext):
        term = ctx.asignable().getText()
        inputType = ctx.typeExpr().getText()
        typeFormatted = fromInputToOutputFormat(inputType)
        self.symbol_table[term] = typeFormatted
        return Void()

    # abstraction : '\\' VARIABLE '->' expr;
    def visitAbstraction(self, ctx: hmParser.AbstractionContext):
        variable = ctx.VARIABLE().getText()
        left = Node(self.next_id(), variable, Void(), Void())
        right = self.visit(ctx.expr())
        return Node(self.next_id(), 'λ', left, right)

    # application : application term    # ApplicRecursive
    def visitApplicRecursive(self, ctx: hmParser.ApplicRecursiveContext):
        left = self.visit(ctx.application())
        right = self.visit(ctx.term())
        return Node(self.next_id(), '@', left, right)

    # application : term term           # ApplicationBase
    def visitApplicationBase(self, ctx: hmParser.ApplicationBaseContext):
        left = self.visit(ctx.term(0))
        right = self.visit(ctx.term(1))
        return Node(self.next_id(), '@', left, right)

    # term: '(' expr ')'                # ParenExpr
    def visitParenExpr(self, ctx: hmParser.ParenExprContext):
        return self.visit(ctx.expr())

    # term : '(' OPERATOR ')'           # OperatorNP
    def visitOperatorNP(self, ctx: hmParser.OperatorNPContext):
        operator = ctx.OPERATOR().getText()
        return Node(self.next_id(), f"({operator})", Void(), Void())

    # term : NUMBER                     # Number
    def visitNumber(self, ctx: hmParser.NumberContext):
        number = ctx.NUMBER().getText()
        return Node(self.next_id(), number, Void(), Void())

    # term : VARIABLE                   # Variable
    def visitVariable(self, ctx: hmParser.VariableContext):
        variable = ctx.VARIABLE().getText()
        return Node(self.next_id(), variable, Void(), Void())


# ################################################################################## #
# ###################################### MAIN ###################################### #
# ################################################################################## #


# -------------------------- CONTROL DE INTERFAZ ESTATICA -------------------------- #

st.write("""
         # El analizador de tipos HinNer
         #### Proyecto de lenguajes de programación - Q2 2023/24
         ###### Hecho por Tahir Muhammad Aziz
         ***
         """)

stInput = st.text_input("Entrada",
                        value="Ejemplo",
                        placeholder="\\ x -> (+) 2 x",
                        )


# -------------------- CONTROL DE LA LOGICA E INTERFAZ DINAMICA -------------------- #

input_stream = InputStream(stInput)
lexer = hmLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = hmParser(token_stream)
tree = parser.root()

# para no perder la tabla de simbolos cada vez que haya rerun de streamlit se usa session_state
if 'symbol_table' not in st.session_state:
    st.session_state['symbol_table'] = {}

if parser.getNumberOfSyntaxErrors() != 0:       # si hay errores de sintaxis se notifica
    st.error(f"{parser.getNumberOfSyntaxErrors()} error(es) de sintaxis.", icon="🚨")
else:                                           # en caso contrario se recorre el ast
    visitor = TreeVisitor(st.session_state['symbol_table'])
    result_tree = visitor.visit(tree)

    # se actualiza la tabla "recurrente" y se pinta con la funcion streamlit.table usando DataFrame de pandas
    st.session_state['symbol_table'] = visitor.symbol_table
    st.write("##### Contenido de la tabla de símbolos")
    symbol_table_data = [{"Símbolo": k, "Tipo": v} for k, v in st.session_state['symbol_table'].items()]
    symbol_table_df = pd.DataFrame(symbol_table_data)
    st.table(symbol_table_df)
    st.divider()

    # si se ha definido un tipo, no se muestra nada mas
    # en caso contrario, se muestra el arbol y se hace la inferencia
    if isinstance(result_tree, Node):
        # se etiquetan los nodos con sus tipos y se imprime con streamlit.graphviz_chart usando DOT
        st.write("##### Árbol de tipos")
        labelTypes(result_tree, st.session_state['symbol_table'])
        graphviz_code = fromTreeToDotGraph(result_tree)
        st.graphviz_chart(graphviz_code)

        # se crea un boton que al ser pulsado se hace la inferencia de tipos y se muestra en una tabla
        if st.button("Inferir tipos"):
            st.divider()
            st.write("##### Inferencia de tipos")
            try:
                tiposInferidos = {}
                inferTypes(result_tree, tiposInferidos)
            except (InconsistenciaDeTipos, AplicacionImposible, TipoNoDefinido) as it:
                st.error(f"ERROR: {it}", icon="🚨")
            else:
                graphviz_code = fromTreeToDotGraph(result_tree)
                st.graphviz_chart(graphviz_code)
                infered_types_data = [{"Tipo": k, "Inferido": v} for k, v in tiposInferidos.items()]
                infered_types_df = pd.DataFrame(infered_types_data)
                st.table(infered_types_df)
