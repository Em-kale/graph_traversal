from manim import *

class MyScene(Scene):
    def construct(self):
        self.title()

        node1_center=[0,0,0]
        node2_center=[5,0,0]
        node3_center=[5,5,0]

        node1 = Circle(color=BLUE).set_center(node1_center)  
        node2 = Circle(color=BLUE).move_to(node2_center)  
        node3 = Circle(color=BLUE).set_center(node3_center)  

        ##stationary dots
        dot1_position = node1.point_at_angle(2*PI) 
        dot3_position = node2.point_at_angle(PI / 2)
        
        d1 = Dot(point=dot1_position, color=BLUE)
        d3 = Dot(point=dot3_position, color=BLUE)

        ##moving dots
        dot2_starting_position = node1.point_at_angle(2*PI)
        dot2_ending_position = node2.point_at_angle(PI)
        dot4_starting_position = node2.point_at_angle(PI)
        dot4_ending_position = node3.point_at_angle(3*PI/2) 

        d2,d4=Dot(color=BLUE),Dot(color=BLUE)

        l1=Line(d1.get_center(),d2.get_center()).set_color(RED)

        ##for moving dots
        dot2_x=ValueTracker(node1.point_at_angle(2*PI)[0])

        d2.add_updater(lambda z: z.set_x(dot2_x.get_value()))
        l1.add_updater(lambda z: z.become(Line(d1.get_center(),d2.get_center())))

        self.play(Create(node1))

        self.add(d1,d2,l1)
        self.play(dot2_x.animate.set_value(dot2_ending_position[0]))

        self.wait(1)

        self.play(Create(node2))

        self.wait(1)

    def title(self): 
        title = MarkupText(
            f"Dijkstra's Algorithm!", color=BLUE
        )

        self.play(FadeIn(title))
        self.wait(1.5)
        self.play(FadeOut(title))
        self.wait(1)
