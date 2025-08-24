A project for applying a force directed algorithm for drawing a graph of arbitrary size neatly, 
with a manim visual animation. 

This functionality has been leveraged and extended (without the manim portion) within the graph traversal visualizer on my website. 

## Usage

For some reason, I am unable to actually get a video to generate automatically

In the meantime, commands to run:

```manim -g filename.py SceneName```

To generate the images, then

```
ffmpeg -framerate 30 -i images/main/<SceneName>%04d.png -c:v libx264 -vf "fps=30,format=yuv420p" -movflags +faststart my_animation.mp4
```

might need to change the digit specification if there are too many image files for 4 values.
