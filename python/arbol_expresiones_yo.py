# arbol_expresiones_practica.py
# Practica - Arboles de expresiones (version para practicar, sin soluciones).
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
        
        #--------------------------------------------------------------------#
        pila = [] #pila = [*]
        for c in postfija.split():  #[3, 4, +, 2, *]
            if c in OPERADORES:
                if len(pila) < 2:
                    raise ValueError("La expresion esta mal formada -> faltan operandos")
                token = Nodo(c)
                hijo_derecho = pila.pop()
                hijo_izquierdo = pila.pop()
                #-> todo en orden, hay dos operandos en la cima de la pila -> asignamos hijos (operandos) al padre
                # (operador):
                token.izquierdo = hijo_izquierdo
                token.derecho = hijo_derecho
                pila.append(token)
            
            else:
                #comprobamos que el token sea un numero:
                if not c.isdigit(): raise ValueError("La empresion esta mal formada -> hay elementos que no son numeros u operadores!")
                #ES UN NUMERO -> OK!
                pila.append(Nodo(c))
        if len(pila) != 1:
            raise ValueError("La expresion esta mal formada -> no queda la raiz en la pila")
        return pila[0]
                   
    # --- Ejercicio 2: evaluar -----------------------------------------------
    def evaluar(self):
        """Cambia el nodo actual y apila"""
        # Coste: O(n)
        # "3 4 + 2 *" -> 14       "7 2 /" -> 3.5
        # Arbol vacio: raise ValueError("..."). La division por cero ya
        # lanza ZeroDivisionError por si sola.
        #---------------------------------------------------------------------#
        # Solo se ejecuta una vez, comprobamos exepción y llamamos a _evaluar #
        #---------------------------------------------------------------------#
        if self.raiz is None: 
            raise ValueError("El arbol esta vacio -> No se puede calcular nada")
         

        return self._evaluar(self.raiz)   #evaluar la raiz = evaluar el arbol entero. El resultado se acumulará en la <call stack>
        
        
    def _evaluar(self, nodo): 
        """Calcula el valor de res con cada nodo
           Devuelve el resultado de la operacion"""
        #-------------------------------------------------------------------------------------------------------#
        # ESTRATEGIA: Llamar a _evaluar una vez por cada nodo -> O(n) -> _evaluar(izq), _evaluar(der).          #
        #             Los 'returns' se ejecutan cuando ya se ha recorrido el arbol entero y se esta desapilando #
        #-------------------------------------------------------------------------------------------------------#
        if nodo.es_hoja():
            return int(nodo.valor)  #apilamos el valor de la hoja
            
        #Es un operador y tiene 2 hijos; a y b son hojas:
        #Aquí apilamos en la <call stack>:
        a = self._evaluar(nodo.izquierdo)   #a = int(a.valor) -> Nota: Por eso ya no hace falta poner abajo en los return "int()"
        b = self._evaluar(nodo.derecho)     #b = int(b.valor)
        
        if nodo.valor == "+":                   
            return a + b
        elif nodo.valor == "-":
            return a - b
        elif nodo.valor == "*":
            return a * b
        elif nodo.valor == "/":
            return a / b
        else: #se supone que nunca deberíamos entrar aquí pero en informática hay que ser desconfiado ;)
            raise ValueError("Hay un operando no definido")
            
   

    # --- Ejercicio 3: las tres notaciones -----------------------------------
    # Tokens separados por un espacio. Arbol vacio -> ""
    def prefija(self):
        # Coste: O(?)      (3 + 4) * 2  ->  "* + 3 4 2"
        #---------------------------------------------------------------------#
        tokens = []
        self._preorder(self.raiz, tokens)
        return " ".join(tokens)
    
    def _preorder(self, nodo, tokens):
        if nodo is None: return 
        tokens.append(nodo.valor)
        self._preorder(nodo.izquierdo, tokens)
        self._preorder(nodo.derecho, tokens)

    def postfija(self):
        # Coste: O(n)      (3 + 4) * 2  ->  "3 4 + 2 *"
        #------------------------------------------------------------------#
        tokens = []
        self._postorder(self.raiz, tokens)
        return " ".join(tokens)
    
    def _postorder(self, nodo, tokens):
        if nodo.valor is None: return 
        self._postorder(nodo.izquierdo, tokens)
        self._postorder(nodo.derecho, tokens)
        tokens.append(nodo.valor)

    def infija(self):
        # Coste: O(n)      (3 + 4) * 2  ->  "((3 + 4) * 2)"
        # Cada operacion entre parentesis; una hoja sola, sin ellos: "7"
        #------------------------------------------------------------------#
        #Casos especiales: No hay arbol o solo una hoja (solo esta la raiz)
        if self.raiz is None: return ""
        return self._inorder(self.raiz)
        
    def _inorder(self, nodo): 
        if nodo.es_hoja(): return nodo.valor
        izq = self._inorder(nodo.izquierda)
        der = self._inorder(nodo.derecha)
        #Si se ejecuta esto, la rama que se esta analizando ha acabado:
        return f"({izq} {nodo.valor} {der})"


    # --- Ejercicio 4: metricas ----------------------------------------------
    def num_nodos(self):
        # O(n). Hecho como ejemplo del patron: metodo publico que llama a un
        # auxiliar recursivo que recibe el nodo.
        if self.raiz is None: return 0
        return self._num_nodos(self.raiz)

    def _num_nodos(self, nodo):
        if nodo.es_hoja():
            return 1
        izq = self._num_nodos(nodo.izquierdo)
        der = self._num_nodos(nodo.derecho)
        #numero de nodos de una rama entera sin contar la raiz del arbol: desde la raiz hasta el final.
        return izq + der + 1

    def altura(self):
        # Coste: O(n)      vacio -> -1, una hoja -> 0
        if self.raiz is None: return -1
        return self._altura(self.raiz)
    
    def _altura(self, nodo):
        if nodo.es_hoja():
            return 0
        
        izq = 1 + self._altura(nodo.izquierdo) 
        der = 1 + self._altura(nodo.derecho) 
        return max(izq, der)
        
    def num_hojas(self):
        # Coste: O(n)
        if self.raiz is None: return 0
        return self._num_hojas(self.raiz)
    
    def _num_hojas(self, nodo):
        if nodo.es_hoja():
            return 1
        izq = self._num_hojas(nodo.izquierdo)
        der = self._num_hojas(nodo.derecho)

        return izq + der
        

    def num_internos(self):
        # Coste: O(n)
        return self.num_nodos() - self.num_hojas()

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

