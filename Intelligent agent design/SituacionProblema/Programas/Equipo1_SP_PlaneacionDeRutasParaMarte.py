#------------------------------------------------------------------------------------------------------------------
#   Imports
#------------------------------------------------------------------------------------------------------------------
import math
import numpy as np

from simpleai.search import SearchProblem, depth_first, breadth_first, astar, iterative_limited_depth_first, limited_depth_first, uniform_cost, greedy
from simpleai.search.viewers import BaseViewer, ConsoleViewer, WebViewer


#------------------------------------------------------------------------------------------------------------------
#   Variables globales
#------------------------------------------------------------------------------------------------------------------

escala = 10.0174
mars_map = np.load('mars_map.npy')
nr, nc = mars_map.shape
x = np.round(escala*np.arange(mars_map.shape[1]))
y = np.round(escala*np.arange(mars_map.shape[0]))
paso = 10

#---------------------------------------------------------------------------------------------------------------
#   Definición del problema
#---------------------------------------------------------------------------------------------------------------

class RutaParaMarte(SearchProblem):
    """ 
        Clase que es usada para definir la ruta para explorar Marte.
        El estado se representará con una coordenada (x,y, z) que representará la posición del agente.
    """
    def __init__(self, posicion_i, posicion_f, altura):
        """ Constructor de la clase.
        """
        self.posicion_i = (posicion_i[0], posicion_i[1], z(posicion_i[0], posicion_i[1]))
        self.altura = altura
        self.escala = escala

        initial_state = self.posicion_i   # Estado inicial
                
        # Llama al constructor de su superclase SearchProblem (se le especifica el estado inicial).
        SearchProblem.__init__(self, initial_state)
        
        self.goal = (posicion_f[0], posicion_f[1], z(posicion_f[0], posicion_f[1]))
    
    def actions(self, state):
        """ 
            Este método regresa una lista con las acciones posibles que pueden ser ejecutadas de 
            acuerdo con el estado especificado.
            
            state: El estado a ser evaluado.
        """
        actions = []
        altura = z(state[0], state[1])
        if state[0]>x[0]:
            if z(state[0]-paso, state[1])!=-1 and abs(z(state[0]-paso, state[1])-altura)<=self.altura:
                actions.append('left')
        if state[0]<x[-1]:
            if z(state[0]+paso, state[1])!=-1 and abs(z(state[0]+paso, state[1])-altura)<=self.altura:
                actions.append('right')
        if state[1]>y[0]:
            if z(state[0], state[1]-paso)!=-1 and abs(z(state[0], state[1]-paso)-altura)<=self.altura:
                actions.append('down')
        if state[1]<y[-1]:
            if z(state[0], state[1]+paso)!=-1 and abs(z(state[0], state[1]+paso)-altura)<=self.altura:
                actions.append('up')
                
        return actions
    
    def result(self, state, action):
        """ 
            Este método regresa el nuevo estado obtenido despues de ejecutar la acción.

            state: El estado a ser modificado.
            action: La acción a ser ejecutada sobre el estado.
        """
        new_state = state
        
        if action=='left':
            new_state = (round(state[0]-paso), state[1], z(state[0]-paso, state[1]))
        elif action=='right':
            new_state = (round(state[0]+paso), state[1], z(state[0]+paso, state[1]))
        elif action=='up':
            new_state = (state[0], round(state[1]+paso), z(state[0], state[1]+paso))
        elif action=='down':
            new_state = (state[0], round(state[1]-paso), z(state[0], state[1]-paso))
        
        return new_state
        
    def is_goal(self, state):
        """ 
            This method evaluates whether the specified state is the goal state.

            state: The state to be tested.
        """
        return state == self.goal
    
    def cost(self, state, action, state2):
        """ 
            Este método recibe dos estados y una acción, y regresa el costo de 
            aplicar la acción del primer estado al segundo.

            state: El primer estado.
            action: La acción usada para generar el segundo estado.
            state2: El segundo estado obtenido después de aplicar la acción.
        """
        return math.sqrt(pow((state2[0]-state[0]), 2)+pow((state2[1]-state[1]), 2)+pow((state[1]-state2[1]), 2))
    
    def heuristic(self, state):
        """ 
            Este método regresa un estimado de la distancia desde el estado a la meta.

            state: El estado a ser evaluado.
        """

        return math.sqrt(pow((self.goal[0]-state[0]), 2)+pow((self.goal[1]-state[1]), 2)+pow((self.goal[2]-state[2]), 2))
    

# Despliega los resultados
def display(result):
    if result is not None:
        for i, (action, state) in enumerate(result.path()):
            if action == None:
                print('Configuración inicial')
            elif i == len(result.path()) - 1:
                print(i,'- Después de', action)
                print('¡Meta lograda con costo =', result.cost,'!')
            else:
                print(i,'- Después de', action)

            print('  ', state)
    else:
        print('Imposible llegar a ese punto. Probar con otra altura')
        
#------------------------------------------------------------------------------------------------------------------
#   Funciones auxiliares
#------------------------------------------------------------------------------------------------------------------

def z(x, y):
    r = round(nr-(x//escala))  
    c = round((y//escala))
    return (mars_map[r][c])

#------------------------------------------------------------------------------------------------------------------
#   Valores iniciales
#------------------------------------------------------------------------------------------------------------------

xi = 2850
yi = 6400
posicion_i = (xi, yi)


"""
#Problema entre dos puntos que no están a más de 500 metros.
xf = 2950
yf = 6600
"""

"""
#Problema entre dos puntos que están entre 1000 y 5000 metros.
xf = 1900
yf = 6000
"""



xf = 3150
yf = 6800

posicion_f = (xf, yf)

altura = 1.285


#------------------------------------------------------------------------------------------------------------------
#   Crear un PSA
#------------------------------------------------------------------------------------------------------------------

my_viewer = None
#my_viewer = ConsoleViewer()    # Texto en la consola


ruta = RutaParaMarte(posicion_i, posicion_f, altura)


print('\n ---------------------------------------------- \n>> Búsqueda Primero en Anchura <<')
result = breadth_first(ruta, graph_search=True, viewer=my_viewer)
display(result)


print('\n ---------------------------------------------- \n>> Búsqueda Primero en Profundidad <<')
result = depth_first(ruta, graph_search=True)
display(result)


print('\n ---------------------------------------------- \n>> Búsqueda Limitada en Profundidad <<')
result = limited_depth_first(ruta, 10,  graph_search=True)
display(result)


print('\n ---------------------------------------------- \n>> Búsqueda Iterativa Limitada en Profundidad <<')
result = iterative_limited_depth_first(ruta, graph_search=True)
display(result)


print('\n ---------------------------------------------- \n>> Búsqueda Codiciosa <<')
result = greedy(ruta, graph_search=True)
display(result)


print('\n ---------------------------------------------- \n>> Búsqueda A* <<')
result = astar(ruta, graph_search=True, viewer=my_viewer)
display(result)


#---------------------------------------------------------------------------------------------------------------
#   Fin del archivo
#---------------------------------------------------------------------------------------------------------------




