from manim import *

class MyScene(Scene):
    def construct(self):
        behold = MarkupText(
            f'Behold!', color=RED
        )

        square = MarkupText(
            f'A Square becoming a circle!', color=BLUE
        )

        self.play(Create(behold))
        self.play(FadeOut(behold))  # fade out animation
        self.wait(1)

        self.play(Create(square))
        self.play(FadeOut(square))  # fade out animation
        self.wait(1)

        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set color and transparency

        square = Square()  # create a square
        square.rotate(PI / 4)  # rotate a certain amount

        self.play(Create(square))  # animate the creation of the square
        self.play(Transform(square, circle))  # interpolate the square into the circle
        self.play(FadeOut(square))  # fade out animation
