
#------------------------------------------------------------------------------------------------------------------
#   Imports
#------------------------------------------------------------------------------------------------------------------
import time
import random
import math
import numpy as np

#------------------------------------------------------------------------------------------------------------------
#   Variables globales
#------------------------------------------------------------------------------------------------------------------

escala = 10.045
mars_map = np.load('mars_crater.npy')
nr, nc = mars_map.shape
x = np.round(escala*np.arange(mars_map.shape[1]))
y = np.round(escala*np.arange(mars_map.shape[0]))
paso = 10


#------------------------------------------------------------------------------------------------------------------
#   Funciones auxiliares
#------------------------------------------------------------------------------------------------------------------

def z(x, y):
    r = round(nr-(x//escala))  
    c = round((y//escala))
    return (mars_map[r][c])


#------------------------------------------------------------------------------------------------------------------
#   Class definitions
#------------------------------------------------------------------------------------------------------------------

class Ruta(object):
    """ 
        Class that represents n-queens placed on a chess board. The board is represented by an array
        of n rows and two columns. Each row corresponds to one queen, and the columns represent
        the coordinates.
    """
    
    def __init__(self, posicion_i, altura):        
        """ 
            This constructor initializes the board with n queens. 

            n: The number of rows and columns of the chess.
            randomize: True indicates that the initial queen positions are choosen randomly.
                       False indicates that the queens are placed on the first row.
        """
        self.posicion_i = (posicion_i[0], posicion_i[1], z(posicion_i[0], posicion_i[1]))
        self.altura = altura
        
    
    def cost(self):
        """ This method calculates the cost of this solution (the number of queens that are not safe). """
        return self.posicion_i[2]

    def neighbor(self):
        """ This method returns a board instance like this one but with one random move made. """        
        new_state = Ruta(self.posicion_i, self.altura)
        acceptable = False
        a = 0
        while not(acceptable):
            i = random.randint(0,4)
            
            if i==0 and self.posicion_i[0]>x[0]:
                a = z(self.posicion_i[0]-paso, self.posicion_i[1])
                new_state.posicion_i = (self.posicion_i[0]-paso, self.posicion_i[1], a)
            
            elif i==1 and self.posicion_i[0]<x[-1]:
                a = z(self.posicion_i[0]+paso, self.posicion_i[1])
                new_state.posicion_i = (self.posicion_i[0]+paso, self.posicion_i[1], a)
                
            elif i==2 and self.posicion_i[1]<y[0]:
                a = z(self.posicion_i[0], self.posicion_i[1]-paso)
                new_state.posicion_i = (self.posicion_i[0], self.posicion_i[1]-paso, a)
                
            elif i==3 and self.posicion_i[1]>y[-1]:
                a = z(self.posicion_i[0], self.posicion_i[1]+paso)
                new_state.posicion_i = (self.posicion_i[0], self.posicion_i[1]+paso, a)
            
            if abs(self.posicion_i[2]-a)<=altura:
                acceptable = True

        return new_state
    
                                       
#------------------------------------------------------------------------------------------------------------------
#   Program
#------------------------------------------------------------------------------------------------------------------
# random.seed(time.time()*1000)

xi = 3350
yi = 5800
posicion_i = (xi, yi)
altura = 2
ruta = Ruta(posicion_i, altura)      # Initialize board

cost = ruta.cost()         # Initial cost    
step = 0                    # Step count

alpha = 0.9995              # Coefficient of the exponential temperature schedule        
t0 = 1                      # Initial temperature
t = t0    

while t > 0.005 and cost > 0:

    # Calculate temperature
    t = t0 * math.pow(alpha, step)
    step += 1
        
    # Get random neighbor
    neighbor = ruta.neighbor()
    new_cost = neighbor.cost()

    # Test neighbor
    if new_cost < cost:
        ruta = neighbor
        cost = new_cost
    else:
        # Calculate probability of accepting the neighbor
        p = math.exp(-(new_cost - cost)/t)
        if p >= random.random():
            ruta = neighbor
            cost = new_cost

    print("Iteration: ", step, "    Cost: ", cost, "    Temperature: ", t)





#------------------------------------------------------------------------------------------------------------------
#   End of file
#------------------------------------------------------------------------------------------------------------------
