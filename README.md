# Analizador de tipos HinNer
##### Hecho por Tahir Muhammad Aziz

## Descripción
Este proyecto es un analizador de tipos basado en la gramática de Hindley-Milner. El propósito es permitir la definición de tipos, así como la inferencia de tipos en expresiones lambda y aplicaciones de funciones.

## Funcionalidades
- **Definición de Tipos:** Define tipos usando una sintaxis similar y simplificada a Haskell.
- **Definición de expresiones:** Define expresiones para ver su comportamiento.
- **Visualización de Árboles:** Representación gráfica del árbol de tipos usando Graphviz.
- **Inferencia de Tipos:** Infere tipos no definidos en expresiones lambda y aplicaciones.
- **Interfaz de Usuario:** Interfaz web interactiva implementada con Streamlit.

## Requisitos
- Python 3.x
- Antlr4
- Streamlit

## Compilación y ejecución
1. Dirigete a la carpeta de los archivos y genera los necesarios:
    ```bash
    antlr4 -Dlanguage=Python3 -no-listener -visitor hm.g4
    ```
1. Ejecuta la aplicación con streamlit:
    ```bash
    streamlit run hm.py
    ```

## Uso
1. **Definición de Tipos:** Introduce definiciones de tipos en la interfaz de usuario. 
    Por ejemplo, para definir el tipo de `(+)`, se puede escribir `(+) :: N -> N -> N`. Las definiciones
    se mantienen en una tabla de tipos, puedes actualizar el tipo de un operador en notacion prefija o numero
    volviendo a introducirlo. Para limpiarla, basta con recargar la pagina.

2. **Definición de Expresiones:** Introduce expresiones lambda y aplicaciones de funciones. 
    Por ejemplo, `(\x -> (+) 2 x) 3`.

3. **Visualización de Árboles:** Al introducir una expresión, se genera automáticamente el árbol de tipos, 
    el cual se visualiza gráficamente debajo de la tabla de tipos.

4. **Inferencia de Tipos:** Después de definir una expresión, presiona el botón "Inferir tipos" 
    para que el sistema realice la inferencia de los tipos no definidos y actualice la visualización del árbol.
    En caso de haber un comportamiento inesperado, se notifica mediante la interfaz el error causante como se ve a continuación.

## Manejo de Errores
- `TipoNoDefinido`: Se lanza cuando el tipo de un símbolo no ha sido definido.
- `InconsistenciaDeTipos`: Se lanza cuando hay un error de inconsistencia de tipos en una aplicación o abstracción.
- `DemasiadasAplicaciones`: Se lanza cuando se supera el máximo de tipos admitidos en una aplicación.
