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
        return self.infija()

    # --- Ejercicio 1: construir ---------------------------------------------
    def construir(self, postfija):
        # Coste: O(n)
        # Devuelve la RAIZ (un Nodo) del arbol de la expresion postfija.
        # Si esta mal formada (faltan o sobran operandos, token que no es un
        # numero ni un operador, cadena vacia): raise ValueError("...")
        # TODO: recorre postfija.split() con una pila (list) de NODOS.
        #--------------------------------------------------------------------#
        expresion_list = postfija.split()
        pila = []
        for c in expresion_list: 
            #creamos el nodo del elemento actual de la expresion postfija
            nodo_actual = Nodo(c)
            if c in OPERADORES:
                if len(pila) < 2:
                    raise ValueError("Faltan Operandos")
                
                nodo_actual.izquierdo = nodo_actual.derecho = None
                derecho = pila.pop()
                izquierdo = pila.pop()
                pila.append(Nodo(c, izquierdo, derecho))

            elif c.isdigit():   #no un else simplemente porque no nos podemos fiar de que el usuario puede que no ponga un digito.
                pila.append(nodo_actual)

            else:
                raise ValueError("Token no valido")
        #YA TENEMOS EL ARBOL! -> comprobamos que solo quede un elemento en la pila:
        if len(pila) != 1:
            raise ValueError("Expresion mal formada")    
        return pila[0]

        #Notese que usamos sacamosy metemos por la derecha porque una lisa es una pila con un array dinamico 
        # y de lo contrario tendriamos que redimiensionar todo el rato -> coste mayor!!!

    # --- Ejercicio 2: evaluar -----------------------------------------------
    def evaluar(self):
        # Coste: O(n)
        # "3 4 + 2 *" -> 14       "7 2 /" -> 3.5
        # Arbol vacio: raise ValueError("..."). La division por cero ya
        # lanza ZeroDivisionError por si sola.
        # TODO
        #--------------------------------------------------------------------#
        if self.raiz is None:
            raise IndexError("EL arbol esta vacio!")
        return self._evaluar(self.raiz)
        
    def _evaluar(self, nodo):
        "3 4 + 2"
        "(*(3, None, None), (4, None, None), (2, None, None))"
        if nodo.es_hoja():
            return int(nodo.valor)
        a = self._evaluar(nodo.izquierdo)
        b = self._evaluar(nodo.derecho)

        #TO COMPLETE



    # --- Ejercicio 3: las tres notaciones -----------------------------------
    # Tokens separados por un espacio. Arbol vacio -> ""
    def prefija(self):
        # Coste: O(n)      (3 + 4) * 2  ->  "* + 3 4 2"
        # TODO
        tokens = []
        self._preorder(self.raiz, tokens)

        # res = ""
        # for c in tokens:
        #     res += c
        # return res
        return "".join(tokens) #equivalente a lo de arriba

    def _preorder(self, nodo, tokens):
        if nodo is None: 
            return
        tokens.append(nodo.valor)
        self._preorder(nodo.izquierdo, tokens)
        self.preorder(nodo.derecho, tokens)

    def postfija(self):
        # Coste: O(?)      (3 + 4) * 2  ->  "3 4 + 2 *"
        # TODO
        raise NotImplementedError

    def infija(self):
        # Coste: O(?)      (3 + 4) * 2  ->  "((3 + 4) * 2)"
        # Cada operacion entre parentesis; una hoja sola, sin ellos: "7"
        # TODO
        raise NotImplementedError

    # --- Ejercicio 4: metricas ----------------------------------------------
    def num_nodos(self):
        # O(n). Hecho como ejemplo del patron: metodo publico que llama a un
        # auxiliar recursivo que recibe el nodo.
        return self._num_nodos(self.raiz)

    def _num_nodos(self, nodo):
        if nodo is None:
            return 0
        i = self._num_nodos(nodo.izquierdo)
        d = self._num_nodos(nodo.derecho)
        return 1 + i + d

    def altura(self):
        # Coste: O(?)      vacio -> -1, una hoja -> 0
        # TODO
        raise NotImplementedError

    def num_hojas(self):
        # Coste: O(?)
        # TODO
        raise NotImplementedError

    def num_internos(self):
        # Coste: O(?)
        # TODO
        raise NotImplementedError
    
    # --- Ampliacion (opcional) ----------------------------------------------
    def infija_minima(self):
        # Coste: O(?)      (3 + 4) * 2  ->  "(3 + 4) * 2"
        #                  3 + (4 * 2)  ->  "3 + 4 * 2"
        #                  8 - (4 - 1)  ->  "8 - (4 - 1)"
        # TODO
        raise NotImplementedError

    def por_niveles(self):
        # Coste: O(?)      (3 + 4) * 2  ->  "* + 2 3 4"   (nivel a nivel)
        # TODO: usa collections.deque como cola.
        raise NotImplementedError

    def construir_prefija(self, prefija):
        # Coste: O(?)      "* + 3 4 2"  ->  raiz del arbol de (3 + 4) * 2
        # Mal formada: raise ValueError("...")
        # TODO: sin pila, con recursion.
        raise NotImplementedError


if __name__ == "__main__":
    from utilidades import dibujar
    a = ArbolExpresion("3 4 + 2 *")
    print(dibujar(a))
    print("prefija :", a.prefija())
    print("infija  :", a.infija())
    print("postfija:", a.postfija())
    print("valor   :", a.evaluar())
