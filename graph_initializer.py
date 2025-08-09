import numpy as np


# TODO: Restrict the positions to the same canvas size manim uses
# TODO: this class should take the frame height and width as a parameter to do this
class GraphInitializer():

    # Graph constants
    NUMBER_OF_NODES = 10

    # Force directed algorithm constants
    FORCE_THRESHOLD = 0.9
    MAX_ITERATIONS = 2000
    REPULSION_CONSTANT = 10.0
    MIN_DISTANCE = 0.5
    INITIAL_COOLING_FACTOR = 1
    COOLING_FACTOR_DECAY = 0.99

    # For total area of canvas
    HEIGHT = 30.0
    WIDTH = 30.0

    def __init__(self):
        # our graph
        # must by symmetrical
        adjacencyMatrix = np.random.randint(
            0, 10, (self.NUMBER_OF_NODES, self.NUMBER_OF_NODES))

        # can get a symmetrical matrix by averaging a matrix with its transpose
        # the potential issue is that this may lead to not very many 0s, and
        # therefore almost all nodes connected, so we might need to inject
        # some zeroes later
        symmetricalAdjacencyMatrix = (adjacencyMatrix + adjacencyMatrix.T) / 2
        self.adjacencyMatrix = symmetricalAdjacencyMatrix

        # set edges on diaganal to zero as that will be between node and itself
        np.fill_diagonal(adjacencyMatrix, 0)

        # initial coordinates for all nodes set to random values
        self.layout = np.random.uniform(0, 10, (self.NUMBER_OF_NODES, 3))

    # ------------------- PUBLIC METHODS -------------------------

    # public
    def get_graph_layout(self):
        return self.__calculate_positions(self.layout)

    # public
    def get_graph(self):
        return self.adjacencyMatrix

    # public
    def get_initial_layout(self):
        return self.layout
    # ------------------- PRIVATE METHODS -------------------------

    # use force directed algorithm to get new positions for all of our nodes
    # private
    def __calculate_positions(self, positionLayout):
        currentIteration = 0

        maxForce = self.FORCE_THRESHOLD + 1
        temp_positions = np.zeros((self.NUMBER_OF_NODES, 3))
        cooling_factor = self.INITIAL_COOLING_FACTOR
        # using Eade's force directed algorithm for simplicity
        while currentIteration < self.MAX_ITERATIONS:
            # and maxForce > self.FORCE_THRESHOLD:

            # let forces be an array holding an array for each node
            # AKA 2D array with NUMBER_OF_NODES arrays set to zero originally
            maxForce = 0.0

            forces = np.zeros((self.NUMBER_OF_NODES, 3))
            i = 0

            # need Frep(u, v) + Fatt(u,v) for each node
            # start with drilling down to the node level in our matrix
            # iterate through the rows
            while i < len(positionLayout):
                repulsive_force = self.__get_repulsive_sum(
                    positionLayout[i], positionLayout)

                # can technically derive all arguments from positionlayout
                # and the index,but whatever for now
                attractive_force = self.__get_attractive_sum(
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
            cooling_factor = cooling_factor * self.COOLING_FACTOR_DECAY
            currentIteration += 1

        return positionLayout

    # private
    def __get_attractive_sum(self, node, index, positionLayout):
        spring_force_sum = np.array([0.0, 0.0, 0.0])
        # shoule only sum for nodes that are connected of course

        # then if index is 1, we do the same for 1 etc.
        i = 0
        while i < len(positionLayout):
            # check index of i in adjacencyMatrix against index of node
            # in adjacencyMatrix, see if corresponding edge is 0
            edge = self.adjacencyMatrix[index, i]

            if edge == 0:
                i += 1
                continue

            euclidian_distance = np.linalg.norm(positionLayout[i]-node)

            if euclidian_distance < self.MIN_DISTANCE:
                euclidian_distance = self.MIN_DISTANCE

            vector_between_nodes = positionLayout[i] - node

            # calculate unit vector
            unit_vector = vector_between_nodes / euclidian_distance

            # calculate the ideal edge length
            # according to a variant of eade -> fruchterman-reingold algo
            # this should be the square root of area / number of nodes
            area = self.WIDTH * self.HEIGHT
            ideal_length = np.sqrt((area / self.NUMBER_OF_NODES))

            # Typical algorithms for this don't consider edge weight
            # here i multiply the edge weight by the ideal length
            # this applies when edge_weight represents the length of the edge,
            # and not the strength of the connection
            # otherwise, it would be the inverse
            spring_force = (np.log(euclidian_distance /
                            ideal_length)*unit_vector)

            spring_force_sum += spring_force
            i += 1

        # TODO: the lecture on this mentions something about subtracting
        # the repulsive force for these nodes. look into that
        # if you get a bad result
        return spring_force_sum

    # private
    def __get_repulsive_sum(self, node, positionLayout):
        sum_of_repulsive_forces = np.array([0.0, 0.0, 0.0])
        i = 0
        while i < len(positionLayout):
            if positionLayout[i] is node:
                i += 1
                continue
            # calculate euclidian distance between the points
            # this is just the magnitude of the difference as a scalar
            # enocdes no information about direction
            euclidian_distance = np.linalg.norm(positionLayout[i]-node)

            if euclidian_distance < self.MIN_DISTANCE:
                euclidian_distance = self.MIN_DISTANCE

            # calclate the unit vector between i and node , from i -> node
            vector_between_nodes = node - positionLayout[i]

            # calculate unit vector
            unit_vector = vector_between_nodes / euclidian_distance

            # calculate repulsive force sum
            sum_of_repulsive_forces += ((self.REPULSION_CONSTANT /
                                         (euclidian_distance ** 2))
                                        * unit_vector)
            i += 1

        return sum_of_repulsive_forces
