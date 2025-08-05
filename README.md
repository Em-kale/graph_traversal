
## Usage

For some reason, I am unable to actually get a video to generate automatically

In the meantime, commands to run:

```manim -g filename.py SceneName```

To generate the images, then

```
ffmpeg -framerate 30 -i images/main/<SceneName>%04d.png -c:v libx264 -vf "fps=30,format=yuv420p" -movflags +faststart my_animation.mp4
```

might need to change the digit specification if there are too many image files for 4 values.
