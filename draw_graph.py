
import numpy as np

# Graph constants
UPPER_BOUND = 10
NUMBER_OF_NODES = 4

# Force directed algorithm constants
FORCE_THRESHOLD = 1
MAX_ITERATIONS = 1
REPULSION_CONSTANT = 2.0
MIN_DISTANCE = 0.05
INITIAL_COOLING_FACTOR = 1
COOLING_FACTOR_DECAY = 0.99

# For total area of canvas
HEIGHT = 20
WIDTH = 20

# our graph
# TODO: MUST BE SYMMETRICAL
adjacencyMatrix = np.random.randint(0, 10, (NUMBER_OF_NODES, NUMBER_OF_NODES))

# initial coordinates for all nodes set to random values
layout = np.zeros((NUMBER_OF_NODES, 3))

# number of rows / columns == number of nodes
# use force directed algorithm to determine new positions for all of our nodes


def calculate_positions(positionLayout):
    currentIteration = 0

    maxForce = FORCE_THRESHOLD + 1
    temp_positions = np.zeros((NUMBER_OF_NODES, 3))
    cooling_factor = INITIAL_COOLING_FACTOR
    # using Eade's force directed algorithm for simplicity
    while currentIteration < MAX_ITERATIONS and maxForce > FORCE_THRESHOLD:
        # need Frep(u, v) + Fatt(u,v) for each node
        # lets start with drilling down to the node level in our matrix
        # iterate through the rows

        # let forces be an array holding an array for each node
        # AKA 2D array with NUMBER_OF_NODES arrays set to zero originally
        maxForce = 0.0

        forces = np.zeros((NUMBER_OF_NODES, 3))
        i = 0
        while i < len(positionLayout):
            repulsive_force = get_repulsive_sum(
                positionLayout[i], positionLayout)

            # can technically derive all arguments from positionlayout and the index,
            # but whatever for now

            attractive_force = get_attractive_sum(
                positionLayout[i], i, positionLayout)

            total_force = repulsive_force + attractive_force

            forces[i] = total_force

            temp_positions[i] = positionLayout[i] + \
                cooling_factor * total_force

            # calculate magnitude of total_force
            total_force_magnitude = np.linalg.norm(total_force)
            # check if max_force
            if total_force_magnitude > maxForce:
                maxForce = total_force_magnitude

            i += 1

        positionLayout = temp_positions
        cooling_factor = cooling_factor * COOLING_FACTOR_DECAY
        currentIteration += 1

    return positionLayout


def get_attractive_sum(node, index, positionLayout):
    spring_force_sum = np.array([0, 0, 0])
    print("calculating attractive force...")
    # shoule only sum for nodes that are connected of course

    # then if index is 1, we do the same for 1 etc.
    i = 0
    while i < len(positionLayout):
        # check index of i in adjacencyMatrix against index of node
        # in adjacencyMatrix, see if corresponding edge is 0
        edge = adjacencyMatrix[index, i]
        if edge == 0:
            continue

        euclidian_distance = np.linalg.norm(positionLayout[i]-node)

        if euclidian_distance < MIN_DISTANCE:
            euclidian_distance = MIN_DISTANCE
        # calclate the unit vector between i and node , from i -> node
        vector_between_nodes = positionLayout[i] - node

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
        i += 1

    # TODO: the lecture on this mentions something about subtracting
    # the repulsive force for these nodes. look into that
    # if you get a bad result
    return spring_force_sum


def get_repulsive_sum(node, positionLayout):
    sum_of_repulsive_forces = np.array([0, 0, 0])
    print("calculating repulsive force...")
    for i in positionLayout:
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


def set_graph_edge_values(matrix):
    i = 0
    while i < NUMBER_OF_NODES:
        matrix[i][i] = 0
        i += 1


set_graph_edge_values(adjacencyMatrix)
print(calculate_positions(layout))
