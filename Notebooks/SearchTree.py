import numpy as np

def BestFirstSearch(problem):
    """
    Algoritmo Best-First Search para generar el camino más apto
    en el árbol de búsqueda de un problema.
    
    Argumentos
    ----------
    problem : objeto
        Problema de búsquda.
        
    Salida
    ------
    nodes : list
        Lista de los nodos que llevan a la solución.
    """
    #Almacenamiento de nodos
    nodes = []
    #Nodo inicial
    node = Node()
    node.state = problem.initial
    #Frontera con cola de prioridad
    frontier = PriorityQueue()
    frontier.push(node)
    #Nodos alcanzados
    reached = {problem.initial:node}

    #Mientras la frontera no esté vacía
    while frontier.isEmpty() == False:
        #Pop en frontera
        node = frontier.pop()
        #Guarda el nodo en la lista
        nodes.append(node)

        #Si llega a un nodo final se detiene 
        #y regresa el camino de nodos
        if node.state in problem.goal:
            return nodes

        #Expande el nodo actual
        expantion = expand(problem, node)
        for child in expantion:
            #Guarda estado de los hijos
            state = child.state
            #Guarda los hijos no alcanzados o que tengan menor costo
            if state not in reached.keys() or child.cost < reached[state].cost:
                reached[state] = child
                frontier.push(child)

    #Si no logra llegar a un nodo final
    #El algoritmo regresa mensaje de error
    return "No se ha logrado llegar a un estado final."
    
class PriorityQueue(object):
    """
    Clase de una cola de prioridad en los problemas de búsqueda.
    """
    def __init__(self):
        self.queue = []
  
    def __str__(self):
        return ' '.join([str(q) for q in self.queue])
  
    def isEmpty(self):
        """
        Returns
        -------
        empty : bool
            Devuelve el valor True si el queue está vacío
        """
        return self.queue == []
  
    def push(self, element):
        """
        Arguments
        ---------
        element : 
            El elemento que se va agregar al queue
        """
        self.queue.append(element)
  
    def pop(self):
        """
        Elimina el elemento con más valor según un peso f
        y regresa el elemento correspondiente a este valor.
        """
        #Encuentra el elemento máximo en base al costo
        max_element = np.argmax([element.cost for element in self.queue])
        #Guarda el elemento máximo
        item = self.queue[max_element]
        #Borra este elemento de la cola
        del self.queue[max_element]
    
        return item
    
    def top(self):
        """
        Devuelve el elemento con la función de costo más alta.
        A diferencia de pop, no elimina el elemento de la pila.
        """
        #Encuentra el elemento máximo en base al costo
        max_element = np.argmax([element.cost for element in self.queue])
        #Guarda el elemento máximo
        item = self.queue[max_element]
        
        return item

class FIFOQueue(object):
    """
    Clase de una cola FIFO en los problemas de búsqueda.
    """
    def __init__(self):
        self.queue = []
  
    def __str__(self):
        return ' '.join([str(q) for q in self.queue])
  
    def isEmpty(self):
        """
        Returns
        -------
        empty : bool
            Devuelve el valor True si el queue está vacío
        """
        return self.queue == []
  
    def push(self, element):
        """
        Arguments
        ---------
        element : 
            El elemento que se va agregar al queue
        """
        self.queue.append(element)
  
    def pop(self):
        """
        Elimina el elemento con más valor según un peso f
        y regresa el elemento correspondiente a este valor.
        """
        #Regresa el primer elemento que llegó
        first_element = self.queue[0]
        #Borra este elemento de la cola
        del self.queue[0]
    
        return first_element
    
    def top(self):
        """
        Devuelve el elemento con la función de costo más alta.
        A diferencia de pop, no elimina el elemento de la pila.
        """
        #Encuentra el elemento máximo en base al costo
        max_element = np.argmax([element.cost for element in self.queue])
        #Guarda el elemento máximo
        item = self.queue[max_element]
        
        return item
        
class Node(object):
    """
    Clase para crear nodos con sus atributos.
    """
    def __init__(self):
        self.state = 0
        self.parent = None 
        self.action = None
        self.cost = 0
        
    def __str__(self):
        if self.parent == None:
            return "State: {}, Cost: {}".format(self.state,self.cost)
        else:
            return "State: {}, Action: {}, Parent: {}, Cost: {}".format(self.state,self.action,self.parent.state,self.cost)
            
            
def expand(problem, node):
    """
    Función para expandir los nodos dado el problema.
    
    Argumentos
    ---------
    problem : objeto
        Problema de búsqueda.
    node : objeto
        Nodo que se va a expandir.
        
    Salida
    ------
    childs :generator
        Generador con los hijos del nodo.
    """
    #Nodo en el que se inicia
    s = node.state 

    for action in problem.actions:
        #Ejecuta la acción
        new_s = problem.act(s, action)
        #Guarda el costo de la acción
        cost = node.cost + problem.transition_model.cost(s,action,new_s)
        
        #Genera un nuevo nodo
        new_node = Node()
        new_node.state = new_s
        new_node.parent = node 
        new_node.action = action 
        new_node.cost = cost

        yield new_node
