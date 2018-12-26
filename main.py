from shader import Program, VertexShader, FragmentShader
from assets import models, textures
from entity import World
from mathematics import create_transformation_matrix, create_perspective_matrix, sin, cos, pi
from pyglet.window import key, mouse, Window
from pyglet.gl import (
    glClear, glClearColor, glEnable, glCullFace,
    GL_DEPTH_BUFFER_BIT, GL_COLOR_BUFFER_BIT, GL_DEPTH_TEST, GL_CULL_FACE, GL_BACK
)

import pyglet
from uniforms import TexturedMaterial, PointLight, SpotLight, SunLight, uniform_struct, uniform_struct_array
from numpy.random import random
from glsl import Vec4


# All calls to OpenGL functions must happen after we've created the context!
window = Window(width=1024, height=1024)


glEnable(GL_DEPTH_TEST)
glEnable(GL_CULL_FACE)
glCullFace(GL_BACK)
glClearColor(0.1, 0.1, 0.12, 1.0)


object_shader = Program(
    vertex_shader=VertexShader(path='shaders/lightning_shader.vs'),
    fragment_shader=FragmentShader(path='shaders/debug_lightning_shader_multiple_lights.fs'),
    uniforms=[
        'transform', 'view', 'projection', 'time', *uniform_struct('material', TexturedMaterial),
        *uniform_struct('spotlight', SpotLight), *uniform_struct_array('light', 4, PointLight),
        *uniform_struct('sunlight', SunLight)
    ],
    attributes=['position', 'normal', 'texture_coordinate']
)
lamp_shader = Program(
    vertex_shader=VertexShader(path='shaders/lamp_shader.vs'),
    fragment_shader=FragmentShader(path='shaders/lamp_shader.fs'),
    uniforms=['transform', 'view', 'projection', 'color'],
    attributes=['position']
)
terrain_shader = Program(
    vertex_shader=VertexShader(path='shaders/lamp_shader.vs'),
    fragment_shader=FragmentShader(path='shaders/lamp_shader.fs'),
    uniforms=['transform', 'view', 'projection', 'color'],
    attributes=['position']
)


world = World(200)
for i in range(10):
    location = random(size=3) * 10 + -random(size=3) * 10
    rotation = random(size=3) * 360
    world.create_object(mask=World.COMPONENT_SPRITE, model=0,
                        location=location, rotation=rotation, diffuse=2, specular=4, emission=3)
point_lights = [
    world.create_object(mask=World.COMPONENT_LIGHT, model=2, location=((-1)**x, 1, -x), scale=(0.1, 0.1, 0.1)) for x in range(2, 6)
]
point_light_structs = [
    PointLight(
        ambient=(0.2, 0.2, 0.2), diffuse=(0.5, 0.5, 0.5), specular=(1.0, 1.0, 1.0), position=world.location[x],
        constant=1.0, linear=0.09, quadratic=0.032
    ) for x in point_lights
]
spot_lights = [
    world.create_object(mask=World.COMPONENT_LIGHT, model=2, location=(0, 0, -1), scale=(0.2, 0.2, 0.2))
]
spot_light_structs = [
    SpotLight(
        ambient=(0.2, 0.2, 0.2), diffuse=(0.5, 0.5, 0.5), specular=(1.0, 1.0, 1.0), position=world.location[spot_lights[0]],
        constant=1.0, linear=0.09, quadratic=0.032, inner_angle=pi/8, outer_angle=pi/4, direction=(0, 0, -1)
    )
]
sun_lights = [
    world.create_object(mask=World.COMPONENT_LIGHT, model=2, location=(0, 0, -1), scale=(0.2, 0.2, 0.2))
]
sun_light_structs = [
    SunLight(
        ambient=(0.2, 0.2, 0.2), diffuse=(0.5, 0.5, 0.5), specular=(0.8, 0.8, 0.8), direction=(0, -1.0, 0)
    )
]

# floors = [
#     world.create_object(mask=World.COMPONENT_SPRITE, model=4, diffuse=1, specular=1, location=(x, 0, z))
#     for x in range(-40, 60, 20) for z in range(-40, 60, 20)
# ]
floor = world.create_object(mask=World.COMPONENT_SPRITE, model=4, diffuse=1, specular=1)


entity_selected = 0


zoom = False
camera_location = [0, 0, -20]
material_struct = TexturedMaterial(shininess=32)  # Values define the texture unit (i.e. GL_TEXTURE0, GL_TEXTURE1...).

time = 0
@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Load lights.
    for light_struct, light in zip(point_light_structs, point_lights):
        light_struct.position[:] = world.location[light]
    for light_struct, light in zip(spot_light_structs, spot_lights):
        light_struct.position[:] = world.location[light]
        # light_struct.direction[:] = cos(time), 0, -sin(time)
    for light_struct, light in zip(sun_light_structs, sun_lights):
        light_struct.direction = cos(pi / 2), -sin(pi / 2), 0


    with object_shader:
        # Upload uniforms.
        object_shader.load_uniform_matrix(create_transformation_matrix(*camera_location, 0, 0, 0, 1, 1, 1), name='view')
        for index, light_struct in enumerate(point_light_structs):
            object_shader.load_uniform_struct(light_struct, name='light[{}]'.format(index))
        for index, light_struct in enumerate(spot_light_structs):
            object_shader.load_uniform_struct(light_struct, name='spotlight')
        for index, light_struct in enumerate(sun_light_structs):
            object_shader.load_uniform_struct(light_struct, name='sunlight')

        object_shader.load_uniform_struct(material_struct, name='material')
        object_shader.load_uniform_floats(time, name='time')

        # Render.
        world.draw(object_shader, models, textures)

    with lamp_shader:  # Just renders the lamp object, does not handle different objects interaction with the lights.
        # Upload uniforms.
        lamp_shader.load_uniform_matrix(create_transformation_matrix(*camera_location, 0, 0, 0, 1, 1, 1), name='view')
        for light_struct in point_light_structs:
            lamp_shader.load_uniform_floats(*light_struct.diffuse, name='color')

        # Render.
        world.draw_light(lamp_shader, models)


@window.event
def on_key_press(symbol, modifiers):
    global entity_selected, zoom
    if symbol == key.T: world.diffuse[entity_selected] = (world.diffuse[entity_selected] + 1) % len(textures)
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


def draw(dt):
    global time
    time = time + dt
    on_draw()

if __name__ == '__main__':
    projection = create_perspective_matrix(60, window.width / window.height, 1, 1000)
    with object_shader:
        object_shader.load_uniform_matrix(projection, name='projection')
    with lamp_shader:
        lamp_shader.load_uniform_matrix(projection, name='projection')

    pyglet.clock.schedule_interval(draw, 1/60)
    pyglet.app.run()
