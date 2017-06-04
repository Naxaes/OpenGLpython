from shader import Program, VertexShader, FragmentShader
from assets import models, textures
from entity import World
from mathematics import create_transformation_matrix, create_perspective_matrix
from pyglet.window import key, mouse, Window
from pyglet.gl import (
    glClear, glClearColor, glEnable, glCullFace,
    GL_DEPTH_BUFFER_BIT, GL_COLOR_BUFFER_BIT, GL_DEPTH_TEST, GL_CULL_FACE, GL_BACK
)

import pyglet
from temp import TexturedMaterial, PointLight, uniform_struct


# All calls to OpenGL functions must happen after we've created the context!
window = Window(width=480, height=480)


glEnable(GL_DEPTH_TEST)
glEnable(GL_CULL_FACE)
glCullFace(GL_BACK)
glClearColor(0.1, 0.1, 0.12, 1.0)


object_shader = Program(
    vertex_shader=VertexShader.from_path('shaders/lightning_shader.vs'),
    fragment_shader=FragmentShader.from_path('shaders/lightning_shader.fs'),
    uniforms=['transform', 'view', 'projection', 'time', *uniform_struct('material', TexturedMaterial), *uniform_struct('light', PointLight)],
    attributes=['position', 'normal', 'texture_coordinate']
)
lamp_shader = Program(
    vertex_shader=VertexShader.from_path('shaders/lamp_shader.vs'),
    fragment_shader=FragmentShader.from_path('shaders/lamp_shader.fs'),
    uniforms=['transform', 'view', 'projection', 'color'],
    attributes=['position']
)


world = World(100)

entity = world.create_object(mask=World.COMPONENT_SPRITE, model=0, location=(0, 0, -5), diffuse=2, specular=4, emission=3)
light  = world.create_object(mask=World.COMPONENT_LIGHT, model=1, location=(0.8, 1, -2), scale=(0.1, 0.1, 0.1))

entity_selected = 0


zoom = False
camera_location = [0, 0, 0]
light_struct = PointLight(
    ambient=(0.2, 0.2, 0.2), diffuse=(0.5, 0.5, 0.5), specular=(1.0, 1.0, 1.0), position=world.location[light],
    constant=1.0, linear=0.09, quadratic=0.032
)
material_struct = TexturedMaterial(shininess=32)

time = 0
@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    light_struct.position = world.location[light]
    with object_shader:
        object_shader.load_uniform_matrix(
            create_transformation_matrix(*camera_location, 0, 0, 0, 1, 1, 1),
            name='view'
        )
        object_shader.load_uniform_struct(light_struct, name='light')
        object_shader.load_uniform_struct(material_struct, name='material')
        object_shader.load_uniform_floats(time, name='time')
        world.draw(object_shader, models, textures)
    with lamp_shader:
        lamp_shader.load_uniform_matrix(
            create_transformation_matrix(*camera_location, 0, 0, 0, 1, 1, 1),
            name='view'
        )
        lamp_shader.load_uniform_floats(*light_struct.diffuse, name='color')
        world.draw_light(lamp_shader, models)


@window.event
def on_key_press(symbol, modifiers):
    global entity_selected, zoom
    if symbol == key.T: world.texture[entity_selected] = (world.texture[entity_selected] + 1) % len(textures)
    if symbol == key.M: world.model[entity_selected] = (world.model[entity_selected] + 1) % len(models)
    if symbol == key.RIGHT:
        entity_selected = (entity_selected + 1) % world.max_entities
        if world.mask[entity_selected] == world.COMPONENT_VOID:
            entity_selected = 0
        print(entity_selected)
    if symbol == key.LEFT:
        entity_selected = (entity_selected - 1) % world.max_entities
        while world.mask[entity_selected] == world.COMPONENT_VOID:
            entity_selected -= 1
        print(entity_selected)
    if symbol == key.LCOMMAND: zoom = True

@window.event
def on_key_release(symbol, modifiers):
    global zoom
    if symbol == key.LCOMMAND: zoom = False


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global entity_selected


    if modifiers & key.MOD_COMMAND:
        if buttons & mouse.LEFT or buttons & mouse.RIGHT:
            world.rotate(entity_selected, -dy / 100, dx / 100, 0)
        # elif buttons & mouse.RIGHT:
        #     world.rotate(entity_selected, 0, 0, dy / 100)
    elif modifiers & key.MOD_ALT:
        if buttons & mouse.LEFT or buttons & mouse.RIGHT:
            world.move(entity_selected, 0, 0, -dy / 100)
        # elif buttons & mouse.RIGHT:
        #     world.rotate(entity_selected, 0, 0, dy / 100)
    else:
        if buttons & mouse.LEFT or buttons & mouse.RIGHT:
            world.move(entity_selected, dx / 100, dy / 100, 0)
        # elif buttons & mouse.RIGHT:
        #     world.move(entity_selected, 0, 0, dy / 100)


@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    global zoom
    if zoom:
        camera_location[2] -= scroll_y / 250
    else:
        camera_location[0] += scroll_x / 250
        camera_location[1] += scroll_y / 250


# import numpy
# def change_light(*ignore):
#     light_struct.ambient = numpy.random.random(size=3)
#     light_struct.diffuse = numpy.random.random(size=3)
#     light_struct.specular = numpy.random.random(size=3)
#
# def change_material(*ignore):
#     material_struct.ambient = numpy.random.random(size=3)
#     material_struct.diffuse = numpy.random.random(size=3)
#     material_struct.specular = numpy.random.random(size=3)
#     material_struct.shininess = numpy.random.randint(0, 128)
#
# pyglet.clock.schedule_interval(change_material, 2)
# pyglet.clock.schedule_interval(change_light, 3)

def draw(dt):
    global time
    # time = time + dt
    on_draw()

if __name__ == '__main__':
    projection = create_perspective_matrix(60, window.width / window.height, 1, 1000)
    with object_shader:
        object_shader.load_uniform_matrix(projection, name='projection')
    with lamp_shader:
        lamp_shader.load_uniform_matrix(projection, name='projection')

    pyglet.clock.schedule_interval(draw, 1/60)
    pyglet.app.run()
