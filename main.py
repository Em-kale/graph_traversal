import manim as m
from graph_initializer import GraphInitializer


class MyScene(m.Scene):
    def construct(self):
        initializer = GraphInitializer()

        # Get random graph layout, processed by force directed algo
        initialLayout = initializer.get_initial_layout()
        graphLayout = initializer.get_graph_layout()
        nodes = [m.Circle] * len(graphLayout)
        nodes_initial = [m.Circle] * len(graphLayout)

        # create a circle for each node using graphLayout as positions
        i = 0
        while i < len(graphLayout):
            nodes[i] = m.Circle(
                color=m.BLUE, fill_opacity=1).move_to(graphLayout[i])
            i += 1

        j = 0
        while j < len(graphLayout):
            nodes_initial[j] = m.Circle(
                color=m.RED, fill_color=1).move_to(initialLayout[j])
            j += 1

        for node in nodes:
            self.play(m.Create(node))
            self.wait(1)

        for initial_node in nodes_initial:
            self.play(m.Create(initial_node))
            self.wait(1)

        # draw lines between them

        #
        #        l1 = Line(d1.get_center(), d2.get_center())
        #        l2 = Line(d3.get_center(), d4.get_center())
