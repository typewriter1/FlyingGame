# Flying Game
My [game](https://typewriter1.github.io).

![Screenshot](https://raw.githubusercontent.com/typewriter1/FlyingGame/master/screenshot7.png)

## Installing

To install, follow these steps:

- Download the zip from the green "Clone or Download" button at the top of the page.
- Install a development version of Panda3D from [here](http://www.panda3d.org/download.php?sdk&version=devel). Ensure you download a Python 3.5/3.6 version, as the game relies on newer features.
- Install RenderPipeline from [here](https://github.com/tobspr/RenderPipeline). Unzip it, and __update the path in gamebase.py__ to point at the installation.

If the game has a low frame-rate on your computer, you can change the `USE_RENDER_PIPELINE` variable to `False`, which make the graphics worse, but it should run quicker.

## How to Play

Use the arrow keys to control the plane.
