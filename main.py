import manim as m
from graph_initializer import GraphInitializer
import numpy as np

# TODO: have this class accept the type of algorithm by
# taking a parameter, then selecting the correct function to call
# also figure out what the name for that architecture is


class MyScene(m.Scene):
    def construct(self):
        initializer = GraphInitializer()

        # Get random graph layout, processed by force directed algo
        initialLayout = initializer.get_initial_layout()
        graphLayout = initializer.get_graph_layout()

        # get adjacencyMatrix
        graph = initializer.get_graph()

        self.nodes = [m.Circle] * len(graphLayout)
        self.nodes_initial = [m.Circle] * len(graphLayout)

        # create a circle for each node using graphLayout as positions
        i = 0
        while i < len(graphLayout):
            self.nodes[i] = m.Circle(
                color=m.WHITE, fill_color=m.BLUE, fill_opacity=1)\
                .move_to(graphLayout[i])
            i += 1

        j = 0
        while j < len(graphLayout):
            self.nodes_initial[j] = m.Circle(
                color=m.WHITE, fill_color=m.RED, fill_opacity=1)\
                .move_to(initialLayout[j])
            j += 1

        # Create array to hold the edges maybe this functionality can
        # be rolled up into the graph class
        initialEdges = []
        k = 0
        # Calculate edge start and end points for the initial graph
        while k < len(graphLayout):
            n = 0
            while n < len(graphLayout):
                if graph[k, n] == 0:
                    n += 1
                    continue
                else:
                    initialEdges.append([initialLayout[k], initialLayout[n]])
                n += 1
            k += 1

        edges = []
        x = 0
        # Calculate edge start and end points for the transformed graph
        while x < len(graphLayout):
            y = 0
            while y < len(graphLayout):
                if graph[x, y] == 0:
                    y += 1
                    continue
                else:
                    edges.append([graphLayout[x], graphLayout[y]])
                y += 1
            x += 1

        self.initialLines = []
        self.transformedLines = []

        # create a line object for each edge

        for initialEdge in initialEdges:
            self.initialLines.append(
                m.Line(initialEdge[0], initialEdge[1]).set_color(m.WHITE))

        for edge in edges:
            self.transformedLines.append(
                m.LabeledLine(label=m.Text(f"{int(np.linalg.norm(np.array([edge[0][0], edge[0][1]])-np.array([edge[1][0], edge[1][1]])))}"),
                              label_position=0.5,
                              label_config={
                    "font_size": 20
                },
                    start=edge[0], end=edge[1]))

        # Create group of entire initial graph
        # for some reason this doesn't accept a list, which seems insane
        # the asterisk unpacks the lists
        self.initialGraphGroup = m.VGroup(
            *self.nodes_initial, *self.initialLines)

        self.processedGraphGroup = m.VGroup(
            *self.nodes, *self.transformedLines)

        # select animate function to run
        # self.animate_graph_construction()
        self.animate_djikstra()

    # This animation displays the randomly generated graph
    # And then the redrawn graph post force-directed algorithm
    def animate_graph_construction(self):
        # Now animate them
        for initial_node in self.nodes_initial:
            self.play(m.Create(initial_node))
            self.wait(1)
        for initialLine in self.initialLines:
            self.add(initialLine)
            self.wait(1)

        # Now, shift the entire VGroup
        self.play(self.initialGraphGroup.animate.shift(m.LEFT * 16))
        self.wait(1)

        for node in self.nodes:
            self.play(m.Create(node))
            self.wait(1)

        for transformedLine in self.transformedLines:
            self.add(transformedLine)
            self.wait(1)

        self.play(m.FadeOut(self.initialGraphGroup))

        self.play(self.processedGraphGroup.animate.shift(m.LEFT * 6))

    def animate_djikstra(self):

        groupCenter = self.processedGraphGroup.get_center()
        width = self.processedGraphGroup.get_width()
        height = self.processedGraphGroup.get_height()
        if width > self.camera.frame_width or height > self.camera.frame_width:
            self.processedGraphGroup.scale(0.9)
            self.animate_djikstra()
            return

        translationVector = m.ORIGIN - groupCenter
        self.processedGraphGroup.shift(translationVector)
        self.wait(100)

        self.add(self.processedGraphGroup)
        self.wait(100)
