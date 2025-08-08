
import numpy as np

# Graph constants
UPPER_BOUND = 10
NUMBER_OF_NODES = 4

# Force directed algorithm constants
FORCE_THRESHOLD = 1
MAX_ITERATIONS = 1
REPULSION_CONSTANT = 2.0
MIN_DISTANCE = 0.05

# For total area of canvas
HEIGHT = 20
WIDTH = 20

# our graph
adjacencyMatrix = np.empty((NUMBER_OF_NODES, NUMBER_OF_NODES))

# initial coordinates for all nodes set to random values
layout = np.empty((NUMBER_OF_NODES, 3))

# number of rows / columns == number of nodes
# use force directed algorithm to determine new positions for all of our nodes


def calculate_positions():
    currentIteration = 0
    maxForce = 20  # placeholder

    # using Eade's force directed algorithm for simplicity
    while currentIteration < MAX_ITERATIONS and maxForce > FORCE_THRESHOLD:
        # need Frep(u, v) + Fatt(u,v) for each node
        # lets start with drilling down to the node level in our matrix
        # iterate through the rows
        for i in layout:
            repulsive_force = get_repulsive_sum(i)
            attractive_force = get_attractive_sum(i)
            print(i)

        currentIteration += 1


def get_attractive_sum(node):
    spring_force_sum = np.array([0, 0, 0])
    print("calculating attractive force...")
    # shoule only sum for nodes that are connected of course
    # TODO: add that

    # we figure out the index of the node we are currently on
    # nodes = [[0,1,2,3],[4,5,6,7],[8,9,1,0],[1,2,3,4]]
    # adjacencyMatrix = [[],[],[],[],[],[],[],[],[],[]....etc
    # call index 0
    # then we need to check against row 1, 2....n where n is number of nodes all at index 0
    # if the value is 0, we skip, if the value is not 0, we don't skip

    # then if index is 1, we do the same for 1 etc.

    # TODO: reinstate the deleted populateGraph function, it initialized the edge values lol

    for i in layout:
        if i is node:
            continue

        euclidian_distance = np.linalg.norm(i-node)

        if euclidian_distance < MIN_DISTANCE:
            euclidian_distance = MIN_DISTANCE
        # calclate the unit vector between i and node , from i -> node
        vector_between_nodes = node - i

        # calculate unit vector (same direction as vector
        # between nodes but length 1)
        unit_vector = vector_between_nodes / euclidian_distance

        # calculate the ideal edge length
        # according to a variant of eade, the fruchterman-reingold algorithm
        # this should be the square root of area / number of nodes
        area = WIDTH * HEIGHT
        ideal_length = np.sqrt((area / NUMBER_OF_NODES))

        spring_force = np.log(euclidian_distance / ideal_length)*unit_vector
        spring_force_sum += spring_force

    # TODO: the lecture on this mentions something about subtracting
    # the repulsive force for these nodes. look into that
    # if you get a bad result
    return spring_force_sum


def get_repulsive_sum(node):
    sum_of_repulsive_forces = np.array([0, 0, 0])
    print("calculating repulsive force...")
    for i in layout:
        if i is node:
            continue
        # calculate euclidian distance between the points
        # this is just the magnitude of the difference as a scalar, and encodes
        # no information about direction
        euclidian_distance = np.linalg.norm(i-node)
        if euclidian_distance < MIN_DISTANCE:
            euclidian_distance = MIN_DISTANCE
        # calclate the unit vector between i and node , from i -> node
        vector_between_nodes = node - i

        # calculate unit vector (same direction as vector
        # between nodes but length 1)
        unit_vector = vector_between_nodes / euclidian_distance

        # calculate repulsive force
        sum_of_repulsive_forces += ((REPULSION_CONSTANT /
                                    (euclidian_distance ** 2)) * unit_vector)
    return sum_of_repulsive_forces


def set_graph_edge_values():
    adjacencyMatrix = np.random.randint(
        0, 10, (NUMBER_OF_NODES, NUMBER_OF_NODES))

    i = 0
    while i < NUMBER_OF_NODES:
        adjacencyMatrix[i][i] = 0
        i += 1

    print(adjacencyMatrix)


set_graph_edge_values()
# calculate_positions()
