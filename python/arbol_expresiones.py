# arbol_expresiones.py
# Practica - Arboles de expresiones.
#
# Objetivo: construir el arbol de una expresion aritmetica a partir de su
# notacion postfija, evaluarlo y escribirlo en las tres notaciones.
#
# Expresiones: numeros enteros no negativos y los operadores + - * /
# Ejemplo: "3 4 + 2 *" es (3 + 4) * 2
#
#         *
#        / \
#       +   2
#      / \
#     3   4
#
# Hay que completar los metodos marcados con TODO (cada uno lanza ahora
# NotImplementedError) y sustituir cada "O(?)" por el coste que consigue tu
# implementacion. Lo que ya esta escrito no se toca: los tests dependen de los
# nombres (raiz, valor, izquierdo, derecho).
#
# Orden de trabajo y tests de cada paso:
#   1. construir                     -> test_arbol_expresiones.PruebasConstruccion
#   2. evaluar                       -> test_arbol_expresiones.PruebasEvaluacion
#   3. prefija, infija, postfija     -> test_arbol_expresiones.PruebasNotaciones
#   4. altura, num_hojas             -> test_arbol_expresiones.PruebasMetricas
# Ampliacion (opcional): infija_minima, por_niveles, construir_prefija
#   -> PruebasAmpliacion (se saltan mientras no los hagas).
#
# Ejecutar los tests:
#   python3 -m unittest -v test_arbol_expresiones
#
# Para ver tu arbol (utilidades.py ya esta hecho):
#   from utilidades import dibujar, infija_a_postfija
#   print(dibujar(ArbolExpresion(infija_a_postfija("(3 + 4) * 2"))))

OPERADORES = ("+", "-", "*", "/")


class Nodo:
    # __slots__: cada nodo solo tiene hueco para estos tres campos.
    __slots__ = ("valor", "izquierdo", "derecho")

    def __init__(self, valor, izquierdo=None, derecho=None):
        self.valor = valor          # str: un numero ("3") o un operador ("+")
        self.izquierdo = izquierdo
        self.derecho = derecho

    def es_hoja(self):
        return self.izquierdo is None and self.derecho is None


class ArbolExpresion:

    def __init__(self, postfija=None):
        # ArbolExpresion()             -> arbol vacio
        # ArbolExpresion("3 4 + 2 *")  -> arbol de la expresion
        self.raiz = None
        if postfija is not None:
            self.raiz = self.construir(postfija)

    def __str__(self):
