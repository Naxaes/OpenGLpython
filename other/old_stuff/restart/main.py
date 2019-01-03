from numpy.random import randint, random
from pyglet.gl import *
from pyglet.window import Window, mouse, key
from restart.entity import Entity, Light, StaticModel, Quad2D
from restart.mathematics import create_transformation_matrix, create_perspective_matrix
from restart.shader import LightShader, ObjectShader, SelectShader, FontShader
from restart.texture import Texture

from other.old_stuff.restart.font import Font

config = pyglet.gl.Config(double_buffer=True, depth_size=24, stencil_size=8, alpha_size=8)

window = Window(width=480, height=480, config=config)

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

glEnable(GL_CULL_FACE)
glCullFace(GL_BACK)


def get_all_entities(mapping):
    entities = []
    if isinstance(mapping, list):
        return mapping
    elif isinstance(mapping, dict):
        for x in mapping.values():
            entities.extend(get_all_entities(x))
        return entities
    else:
        assert False


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if selected_entity is None:
        return
    if buttons == mouse.LEFT:
        selected_entity.location[0] += dx / 250
        selected_entity.location[1] += dy / 250
    elif buttons == mouse.MIDDLE:  # Scroll button.
        selected_entity.scale[0] += dx / 250
        selected_entity.scale[1] += dy / 250
    elif buttons == mouse.RIGHT:
        selected_entity.rotation[1] += dx / 250
        selected_entity.rotation[0] -= dy / 250


@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    if selected_entity is None:
        return
    selected_entity.location[2] -= scroll_y / 10
    selected_entity.location[0] += scroll_x / 10


@window.event
def on_key_press(symbol, modifiers):
    global selected_entity_index, selected_entity

    if symbol == key.LEFT:
        selected_entity_index -= 1
    elif symbol == key.RIGHT:
        selected_entity_index += 1
    elif symbol == key.SPACE:
        selected_entity = camera
        return
    else:
        return


    for entity in get_all_entities(entities):
        if entity.value == selected_entity_index:
            selected_entity = entity
            return
    else:
        if selected_entity_index == -1:
            selected_entity = text

    print(selected_entity_index)

    selected_entity_index = 0



@window.event
def on_draw():
    # Clearing the stencil buffer must take scissor test and mask into account. Always enable writing to the stencil
    # buffer before clearing!
    glEnable(GL_DEPTH_TEST)

    glStencilMask(0xFF)
    glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)

    glEnable(GL_STENCIL_TEST)
    glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)  # Action if: stencil fails, stencil pass & depth fails, both passes
    glStencilFunc(GL_ALWAYS, 1, 0xFF)  # Update with 1's where the objects are rendered.
    glStencilMask(0x00)  # Value that AND's the value written to buffer. 0xFF basically enable's writing to stencil.

    uniforms = {
        b'perspective': perspective_matrix,
        b'view'       : create_transformation_matrix(*camera.location, *camera.rotation, *camera.scale)
    }

    # light_program.draw(uniforms, lights, models)
    object_program.draw(uniforms, entities, models, textures, get_all_entities(lights))
    #
    # if selected_entity is not None and selected_entity is not camera and selected_entity is not text:
    #     select_program.draw(uniforms, selected_entity, models, color=selected_color)
    #
    # font_program.draw(uniforms, text, quad, font.texture)


object_program = ObjectShader()
light_program = LightShader()
select_program = SelectShader()
font_program = FontShader()


CUBE = 0
SPHERE = 1
models = [StaticModel.as_cube(), StaticModel.from_obj_file('../resources/models/sphere.obj')]

NO_TEXTURE = 0
CONTAINER = 0
CONTAINER_SPECULAR = 1
ALUMINIUM_PLATE = 2
textures = [
    Texture('../resources/textures/Container.png'),
    Texture('../resources/textures/ContainerSpecular.png'),
    Texture('../resources/textures/AluminiumPlate.png')
]

entities = {
    CUBE  : {
        # CONTAINER      : [Entity(location=randint(-6, 6, size=3), model=CUBE, textures=CONTAINER) for i in range(5)],
        # ALUMINIUM_PLATE: [Entity(location=randint(-6, 6, size=3), model=CUBE, textures=ALUMINIUM_PLATE) for i in
        #                   range(5)],
        (CONTAINER, CONTAINER_SPECULAR): [Entity(location=randint(-6, 6, size=3), model=CUBE, textures=(CONTAINER, CONTAINER_SPECULAR)) for i in range(2)]
    },
    # SPHERE: {
    #     CONTAINER      : [Entity(location=randint(-6, 6, size=3), model=SPHERE, textures=CONTAINER) for i in range(5)],
    #     ALUMINIUM_PLATE: [Entity(location=randint(-6, 6, size=3), model=SPHERE, textures=ALUMINIUM_PLATE) for i in
    #                       range(5)]
    # },
}

lights = {  # lights have no material but instead has two extra entity attributes: color and attenuation.
    CUBE  : [Light(location=randint(-6, 6, size=3), color=random(size=3)) for i in range(2)],
    SPHERE: [Light(location=randint(-6, 6, size=3), color=random(size=3)) for i in range(2)]
}

object_program.add_entities([Entity(location=randint(-6, 6, size=3), model=CUBE, textures=(CONTAINER, CONTAINER_SPECULAR)) for i in range(2)])

print(object_program.entities)
print(entities)

perspective_matrix = create_perspective_matrix(60, window.width / window.height, 0.1, 100)
camera = Entity((0, 0, 0), (0, 0, 0), (1, 1, 1))

selected_entity_index = 0
selected_entity = camera
selected_color = (1.0, 0.8, 1.0)


font = Font('../resources/fonts/arial.fnt')
text = Entity((0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1))
quad = Quad2D(*font.create_text_quad('Welcome to OpenGL!', anchor_center=True))

pyglet.app.run()
