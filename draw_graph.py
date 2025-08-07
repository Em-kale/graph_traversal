
import numpy as np

UPPER_BOUND = 10
NUMBER_OF_NODES = 4

FORCE_THRESHOLD = 1
MAX_ITERATIONS = 1
REPULSION_CONSTANT = 2.0
MIN_DISTANCE = 0.05
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
    print("calculating attractive force...")
    # calculate attractive force


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

        # calculate unit vector (same direction as vector between nodes but length 1)
        unit_vector = vector_between_nodes / euclidian_distance

        # calculate repulsive force
        sum_of_repulsive_forces += ((REPULSION_CONSTANT /
                                    (euclidian_distance ** 2)) * unit_vector)
    return sum_of_repulsive_forces


calculate_positions()
