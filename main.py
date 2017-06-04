from shader import Program, VertexShader, FragmentShader
from vbo import VBO, IndexedVBO, VAO, load_model
from entity import Entity
from mathematics import create_transformation_matrix, create_perspective_matrix
from pyglet.window import key, mouse, Window
from pyglet.clock import schedule_interval
from pyglet.gl import (
    glClear, glClearColor, glEnable, glCullFace,
    GL_DEPTH_BUFFER_BIT, GL_COLOR_BUFFER_BIT, GL_DEPTH_TEST, GL_CULL_FACE, GL_BACK
)


# All calls to glEnable must happen after we create the context!
window = Window(width=480, height=720)


glEnable(GL_DEPTH_TEST)
glEnable(GL_CULL_FACE)
glCullFace(GL_BACK)
glClearColor(0.8, 0.8, 0.8, 1.0)


shader_program = Program(
    vertex_shader=VertexShader.from_path('shaders/vertex_shader.txt'),
    fragment_shader=FragmentShader.from_path('shaders/fragment_shader.txt'),
    uniforms=['transformation', 'projection', 'light_position'],
    attributes=['position', 'normal']
)
shader_program2 = Program(
    vertex_shader=VertexShader.from_path('shaders/vertex_shader2.txt'),
    fragment_shader=FragmentShader.from_path('shaders/fragment_shader.txt'),
    uniforms=['transformation', 'projection', 'light_position'],
    attributes=['position', 'normal']
)

projection = create_perspective_matrix(60, window.width / window.height, 1, 1000)

# vao = VAO(indexed_vbo=IndexedVBO(indices), position=VBO(vertices))
suzanne = Entity(
    model=load_model('resources/models/suzanne.obj'), location=(0, 0, -5), rotation=(0, 0, 0), scale=(1, 1, 1)
)
light = Entity(
    model=load_model('resources/models/sphere.obj'), location=(0, 0, -3), rotation=(0, 0, 0), scale=(0.1, 0.1, 0.1)
)


shader_selection = 0
@window.event
def on_draw():
    update()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    shader = shader_program if shader_selection == 0 else shader_program2
    with shader:
        shader.load_uniform_matrix(projection, name='projection')

        shader.load_uniform_floats(*light.location, name='light_position')
        light.draw(shader)

        suzanne.draw(shader)


@window.event
def on_key_press(symbol, modifiers):
    global shader_selection, suzanne
    if symbol == key.A: suzanne.location[0] -= 0.1
    if symbol == key.D: suzanne.location[0] += 0.1
    if symbol == key.W: suzanne.location[1] += 0.1
    if symbol == key.S: suzanne.location[1] -= 0.1
    if symbol == key.Q: suzanne.location[2] += 1
    if symbol == key.E: suzanne.location[2] -= 1
    if symbol == key.SPACE: shader_selection = (shader_selection + 1) % 2



@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global suzanne, light
    if buttons & mouse.MIDDLE or buttons & mouse.LEFT and modifiers & key.MOD_COMMAND:
        suzanne.rotation[1] += dx / 100
        suzanne.rotation[0] -= dy / 100
    elif buttons & mouse.LEFT:
        suzanne.location[0] += dx / 250
        suzanne.location[1] += dy / 250
    elif buttons & mouse.RIGHT:
        if modifiers & key.MOD_CTRL or modifiers & key.MOD_COMMAND:
            light.location[2] -= dy / 100
        else:
            light.location[0] += dx / 100
            light.location[1] += dy / 100


@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    global suzanne, light
    suzanne.location[0] += scroll_x / 250
    suzanne.location[1] += scroll_y / 250
    light.location[0] += scroll_x / 250
    light.location[1] += scroll_y / 250


def update():
    global suzanne, light
    suzanne.update()
    light.update()


if __name__ == '__main__':
    import pyglet
    pyglet.app.run()
