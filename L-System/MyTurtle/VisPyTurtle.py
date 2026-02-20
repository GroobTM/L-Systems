from vispy import use, app, scene
# Make VisPy use glfw
use(app="glfw")

from .MyTurtle import MyTurtle

class VisPyTurtle(MyTurtle):
    def __init__(self):
        super().__init__()

    def draw(self):
        canvas = scene.SceneCanvas(title="L-System", show=True, bgcolor="white")
        view = canvas.central_widget.add_view()

        view.camera = "panzoom"

        lines = self._MyTurtle__lines.reshape(-1, 2)

        scene.visuals.Line(pos=lines, parent=view.scene, width=2, connect="segments")
        
        view.camera.set_range()

        app.run()