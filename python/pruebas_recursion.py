from arbol_expresiones_yo import ArbolExpresion

def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n - 1) #factorial(n) = n * factorial(n - 1) -> Ej: 5! = 5 * 4!

"""Lo que nos está rallando es el hecho de que nosotros no vemos una variable que esté acumulando el resultado.
   -> Se está acumulando en la <call stack>, el intérprete va línea a línea de lo que se 
      ejecuta en cada caso, de tal forma que *cuando se termina de evaluar la funcion*
      es cuando se empieza a calcular.
   -> ¿Cómo sabe el intérprete cuando para?
       Cuando ya no hay más recursión, es decir, en la línea 3 (return 1) no se llama a nada más, por tanto ese es
       el ultimo elemento de la <call stack> y desde ese momento se empieza a desapilar y calcular el resultado
    --> Hay que ponerse en situacion de lo que puede pasar en la siguiente iteración"""  
    
#--------- FACTORIAL ------------
n = 5
print(factorial(n))


#--------- EVALUAR() ------------
a = ArbolExpresion("3 4 + 2 *")
print(a.evaluar())

#--------- PREFIJA() ------------
a = ArbolExpresion("3 4 + 2 *")
print(a.prefija())

#--------- NUM_NODOS() ------------
a = ArbolExpresion("3 2 + 2 * 7 2 / *")
print(a.num_nodos())

#--------- ALTURA() ------------
a = ArbolExpresion("3 2 + 2 * 7 2 / *")
print(a.altura())

#--------- NUM_HOJAS() ------------
a = ArbolExpresion("3 4 + 2 *")
print(a.num_hojas())