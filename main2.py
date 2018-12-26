from shader import Program, VertexShader, FragmentShader
from assets import models, textures
from entity import Entity, draw_entities, draw_lights, update_entities
from mathematics import create_transformation_matrix, create_perspective_matrix, sin, cos, pi
from pyglet.window import key, mouse, Window
from pyglet.gl import (
    glClear, glClearColor, glEnable, glCullFace,
    GL_DEPTH_BUFFER_BIT, GL_COLOR_BUFFER_BIT, GL_DEPTH_TEST, GL_CULL_FACE, GL_BACK
)

import pyglet
from glsl import *
from collections import OrderedDict


# All calls to OpenGL functions must happen after we've created the context!
window = Window(width=720, height=720)
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

glEnable(GL_DEPTH_TEST)
glEnable(GL_CULL_FACE)
glCullFace(GL_BACK)
glClearColor(0.1, 0.1, 0.12, 1.0)


object_shader = Program(
    vertex_shader=VertexShader(path='shaders/vertex_shader.txt'),
    fragment_shader=FragmentShader(path='shaders/fragment_shader.txt'),
    uniforms=OrderedDict(
        transform=Mat4(),
        view=Mat4(),
        projection=Mat4(*create_perspective_matrix(60, window.width / window.height, 1, 1000).flatten()),
    ),
    attributes=('location', 'normal', 'texture_coordinate')
)

entity = Entity(location=(0, 0, -20))
camera = Entity(location=(0, 0, 0))

time = 0
@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    with object_shader:
        draw_entities((entity, ), object_shader, models)


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global camera

    if modifiers & key.MOD_COMMAND:
        if buttons & mouse.LEFT or buttons & mouse.RIGHT:
            entity.rotation += -dy / 100, dx / 100, 0
        # elif buttons & mouse.RIGHT:
        #     world.rotate(entity_selected, 0, 0, dy / 100)
    elif modifiers & key.MOD_ALT:
        if buttons & mouse.LEFT or buttons & mouse.RIGHT:
            entity.location += 0, 0, -dy / 100
        # elif buttons & mouse.RIGHT:
        #     world.rotate(entity_selected, 0, 0, dy / 100)
    else:
        if buttons & mouse.LEFT or buttons & mouse.RIGHT:
            entity.location += dx / 100, dy / 100, 0
        # elif buttons & mouse.RIGHT:
        #     world.move(entity_selected, 0, 0, dy / 100)


@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    global zoom
    if zoom:
        camera.location -= 0, 0, scroll_y / 250
    else:
        camera.location += scroll_x / 250, scroll_y / 250, 0


if __name__ == '__main__':
    pyglet.app.run()
