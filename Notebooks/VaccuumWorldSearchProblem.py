from copy import deepcopy
import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np

class State(object):
    """
    Define un objeto estado que contiene:
    
    world
        información sobre el mundo
    agent_location
        posición del agente en el mundo
    """
    def __init__(self):
        self.world = None
        self.agent_location = None
        
    def __str__(self):
        #return "World state: {} - Agent location: {}".format(self.world, self.agent_location)
        return "World: {}, Loc: {}".format(self.world, self.agent_location)        
        
def return_state_idx(state, states):    
    """
    Regresa el índice de un estado en el diccionario de estados.
    
    Argumentos
    ----------
    state : object
        el estado del cual se quiere obtener el índice
    """
    for i, new_state in states.items():
        if state.world == new_state.world and state.agent_location == new_state.agent_location:
            return i
            
class Transition(object):
    """
    Clase para obtener el modelo de transicion.
    """
    def __init__(self, cost_function = None):
        self.transitions = []
        self.cost_function = cost_function

    def get_transitions(self, states):
        """
        Genera el modelo de transición con los estados.
        Únicamente para el mundo de la aspiradora.

        Argumentos
        ----------
        states : dict
        Diccionario de estados del modelo de búsqueda
        """
        for i,prev_state in states.items():
            #Copia el estado para no modificarlo
            state = deepcopy(prev_state)
            #Guarda locación del agente
            location = state.agent_location
            #Guarda estado de la suciedad
            dirt = state.world[location]

            #Acción: si está sucio, limpia
            if dirt == 1:
                new_state = deepcopy(state)
                new_state.world[location] = 0
                clean_state = return_state_idx(new_state, states)
                self.transitions += [(i,'Clean',clean_state)]
            #Acción: Moverse de A a B
            if location == 'A':
                new_state = deepcopy(state)
                new_state.agent_location = 'B'
                right_state = return_state_idx(new_state, states)
                self.transitions += [(i,'Right',right_state)]
            #Acción: Moverse de B a A
            if location == 'B':
                new_state = deepcopy(state)
                new_state.agent_location = 'A'
                left_state = return_state_idx(new_state, states)
                self.transitions += [(i,'Left',left_state)]
                
    def backward_transitions(self, states):
        """
        Genera el modelo de transición de retroceso con los estados.
        Únicamente para el mundo de la aspiradora.

        Argumentos
        ----------
        states : dict
        Diccionario de estados del modelo de búsqueda
        """
        for i,prev_state in states.items():
            #Copia el estado para no modificarlo
            state = deepcopy(prev_state)
            #Guarda locación del agente
            location = state.agent_location
            #Guarda estado de la suciedad
            dirt = state.world[location]

            #Acción: si está sucio, limpia
            if dirt == 1:
                new_state = deepcopy(state)
                new_state.world[location] = 0
                clean_state = return_state_idx(new_state, states)
                self.transitions += [(clean_state,'Clean',i)]
            #Acción: Moverse de A a B
            if location == 'A':
                new_state = deepcopy(state)
                new_state.agent_location = 'B'
                right_state = return_state_idx(new_state, states)
                self.transitions += [(right_state,'Right',i)]
            #Acción: Moverse de B a A
            if location == 'B':
                new_state = deepcopy(state)
                new_state.agent_location = 'A'
                left_state = return_state_idx(new_state, states)
                self.transitions += [(left_state,'Left',i)]

    def transition(self, state_idx, action):
        """
        Función de transición.

        Argumentos
        ----------
        state_idx : int
            Estado actual en el que nos encontramos
        action : str
            Acción que se ejecuta en el estado

        Salida
        ------
        new_state : int
            Nuevo estado, resultado de la acción. 
            Si la acción no cambia el mundo, permanece en el mismo estado.
        """
        for (st,act,new_state) in self.transitions:
            if st == state_idx and act == action:
                return new_state
            else:
                pass
        
        return state_idx

    def cost(self, state, action, new_state):
        """
        Función de costo de la acción. En general cada acción 
        del mundo de la aspiradora cuesta 1.
        """
        if self.cost_function == None:
            return 1

    def plot_graph(self):
        """
        Función para visualizar la gráfica de las transiciones.
        """
        #Crea gráfica dirigida en networkx
        G = nx.DiGraph(directed=True)
        G = nx.from_edgelist([(e[0],e[2]) for e in self.transitions])
        
        #Funciones para plotear
        pos = nx.spring_layout(G)
        nx.draw(G, pos, labels=states, with_labels=True,node_size=1)
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='b')
        nx.draw_networkx_edge_labels(G, pos, edge_labels={(e[0],e[2]):e[1] for e in self.transitions},
                                     font_color='red')
        plt.show()
        
        
class SearchProblem(object):
    """
    Define el problema de búsquda.
    """
    def __init__(self, states, goal, actions, transition_model, initial=0):
        self.states = states
        self.initial = initial
        self.goal = goal
        self.actions = actions
        self.transition_model = transition_model
        
    def __str__(self):
        return "States: \n -{}\nInitial State:\n -{}\nFinal states:\n -{}\nActions:\n -{}\nTransition model:\n -{}".format(list(self.states.keys()),self.initial,self.goal,self.actions,self.transition_model.transitions)
    
    def act(self,state,action):
        #Regresa la transición de una acción
        return self.transition_model.transition(state,action)
