import numpy
import os
from numpy.random import randint
from pyglet.gl import *
from pyglet.window import Window, mouse, key
from ctypes import cast, pointer, POINTER, byref, sizeof, create_string_buffer, c_char, c_float, c_uint
from math import cos, sin, tan, pi


from source.model   import load_model, create_cube
from source.texture import load_texture
from source.text    import Font
from source.shader  import Shader
from source.linear_algebra import Vector2, Vector3, transformation_matrix, perspective_matrix as create_perspective_matrix

# We want a stencil buffer with 8-bit values. Don't know why we have to specify double_buffer,
# but it don't work otherwise. The other default values are good.
config = pyglet.gl.Config(stencil_size=8, double_buffer=True)
window = Window(width=480, height=480, config=config)


class Transform:
    def __init__(self, location, rotation, scale):
        self.location = Vector3(*location)
        self.rotation = Vector3(*rotation)
        self.scale    = Vector3(*scale)

    def matrix(self):
        return transformation_matrix(*self.location, *self.rotation, *self.scale)


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


def get_selected_entity_transform():
    entity = all_entities[entity_selected]
    if isinstance(entity, list):
        transform = entity[0]
    else:
        transform = entity
    return transform


# Hack until we make better data structure for entities.
def get_entity_model_index(entity):
    for model_index, texture_mapping in entities.items():
        for texture_index, entity_list in texture_mapping.items():
            for candidate in entity_list:
                if candidate == entity:
                    return model_index
    for model_index, entity_list in lights.items():
        for candidate in entity_list:
            if candidate == entity:
                return model_index
    return None


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    transform = get_selected_entity_transform()
    if buttons == mouse.LEFT:
        transform.location[0] += dx / 250
        transform.location[1] += dy / 250
    elif buttons == mouse.MIDDLE:  # Scroll button.
        transform.scale[0] += dx / 250
        transform.scale[1] += dy / 250
    elif buttons == mouse.RIGHT:
        transform.rotation[1] += dx / 250
        transform.rotation[0] -= dy / 250


@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    transform = get_selected_entity_transform()
    transform.location[2] -= scroll_y / 10
    transform.location[0] += scroll_x / 10


@window.event
def on_key_press(symbol, modifiers):
    global entity_selected
    if key.LEFT == symbol:
        entity_selected = (entity_selected - 1) % len(all_entities)
    elif key.RIGHT == symbol:
        entity_selected = (entity_selected + 1) % len(all_entities)


@window.event
def on_draw():
    # Must be set here because we turn those of when rendering using stencil buffer.
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glEnable(GL_STENCIL_TEST)
    glStencilOp(GL_KEEP, GL_KEEP,
                GL_REPLACE)  # Keep if depth test fails, keep if stencil test fails, replace if both succeed.

    glStencilFunc(GL_ALWAYS, 1, 0xFF)  # Always fill the stencil buffer.
    glStencilMask(0xFF)  # 0xFF turns on writes the stencil mask. 0x00 disables writes.

    # Apparently, if we've haven't enabled writes for the stencil mask before this line, the stencil mask won't be cleared.
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)

    # Light shader
    simple_program.enable()
    simple_program.load_uniform_matrix(perspective=perspective_matrix, view=camera.matrix())

    for model_index, entity_list in lights.items():
        model = models[model_index]
        model.enable()

        for entity in entity_list:
            transform, color, attenuation = entity

            simple_program.load_uniform_matrix(transformation=transform.matrix())
            simple_program.load_uniform_floats(color=color)

            model.render()

    # Object shader
    program.enable()
    program.load_uniform_matrix(perspective=perspective_matrix, view=camera.matrix())

    for i, entity in enumerate(get_all_entities(lights)):
        program.load_uniform_floats(**{'light[' + str(i) + '].position': entity[0].location})
        program.load_uniform_floats(**{'light[' + str(i) + '].color': entity[1]})
        program.load_uniform_floats(**{'light[' + str(i) + '].constant': entity[2][0]})
        program.load_uniform_floats(**{'light[' + str(i) + '].linear': entity[2][1]})
        program.load_uniform_floats(**{'light[' + str(i) + '].quadratic': entity[2][2]})

    for model_index, texture_mapping in entities.items():
        model = models[model_index]
        model.enable()

        for texture_indices, entity_list in texture_mapping.items():

            # Make bindings for texture.
            for index, texture_index in enumerate(texture_indices):
                glActiveTexture(GL_TEXTURE0 + index)
                texture = textures[texture_index]
                glBindTexture(GL_TEXTURE_2D, texture.id)
            texture_names = {'material.diffuse': 0, 'material.specular': 1, 'material.emission': 2}
            program.load_uniform_sampler(**texture_names)
            program.load_uniform_floats(**{'material.shininess': 32})

            for entity in entity_list:
                transform = entity

                # Prepare entities of specific model and texture, and draw.
                program.load_uniform_matrix(transformation=transform.matrix())
                model.render()

    # Stencil shader
    glDisable(GL_DEPTH_TEST)  # Disable depth tests.
    glStencilFunc(GL_NOTEQUAL, 1, 0xFF)  # Only draw where the stencil buffer isn't 1.
    glStencilMask(0x00)  # Disable writes.

    transform = get_selected_entity_transform()
    sx, sy, sz = transform.scale
    # Make the transform slightly bigger so it's visible.
    transform = transformation_matrix(*transform.location, *transform.rotation, sx * 1.1, sy * 1.1, sz * 1.1)
    model_index = get_entity_model_index(all_entities[entity_selected])
    if model_index is not None:
        model = models[model_index]

        simple_program.enable()
        simple_program.load_uniform_matrix(perspective=perspective_matrix, view=camera.matrix(),
                                           transformation=transform)
        simple_program.load_uniform_floats(color=[255, 0, 255])

        model.enable()
        model.render()

    # Render text
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)

    text = font_arial.text_model("Hello", anchor_center=True)

    simple_2D_program.enable()
    simple_2D_program.load_uniform_matrix(perspective=perspective_matrix, view=camera.matrix(),
                                          transformation=text_transform.matrix())
    simple_2D_program.load_uniform_floats(color=[255, 255, 255])

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, font_arial.texture.id)

    text.enable()
    text.render()


# Create shaders.
object_shaders    = [
    """
    #version 120

    uniform mat4 transformation;
    uniform mat4 perspective;
    uniform mat4 view;

    attribute vec3 position;
    attribute vec3 normal;
    attribute vec2 texture_coordinate;

    varying vec3 out_position;
    varying vec3 out_normal;
    varying vec2 out_texture_coordinate;

    void main()
    {
        // Vector should have 1.0 as w-component so the transformation matrix affects it properly, while directions
        // should have 0.0 as w-component so the transformation matrix doesn't affect it's location.
        // Since position is a vector, it should have 1.0 as w-component.
        // Since normal is a direction, it should have 0.0 as w-component.

        vec4 full_position = vec4(position, 1.0);
        vec4 full_normal   = vec4(normal, 0.0);

        vec4 world_position = transformation * full_position;
        vec4 world_normal   = transformation * full_normal;

        out_position = vec3(world_position);
        out_normal   = normalize(vec3(world_normal));
        out_texture_coordinate = texture_coordinate;

        gl_Position =  perspective * view * world_position;
    }

    """,
    """
    #version 120

    /* 
    Naming conventions:
        * vector    - A vector that might not be normalized.
        * direction - A vector that must be normalized.

        All vectors/directions are in relation to the object vertex if nothing else is specified. 
        For example: 
            'normal' is the normal of the vertex.
            'vector_to_light' is a non-normalized vector pointing from the vertex to the light.
            'direction_camera_to_light' is a normalized vector pointing from the camera to the light.
    */

    struct Light {
        vec3  position;
        vec3  color;

        float constant;
        float linear;
        float quadratic;
    };

    struct Material {
        sampler2D diffuse;
        sampler2D specular;
        sampler2D emission;
        float shininess;
    };

    const int NUM_LIGHTS = 4;

    uniform sampler2D texture;
    uniform Light light[NUM_LIGHTS];
    uniform mat4  view;
    uniform Material material;

    varying vec3 out_position;
    varying vec3 out_normal;
    varying vec2 out_texture_coordinate;


    vec3 calculate_pointlight(Light light, Material material, vec3 position, vec3 normal, vec2 texture_coordinate)
    {

        vec3  light_direction = normalize(light.position - position);
        vec3  camera_position = -view[3].xyz;

        // Attenuation
        float distance = length(light.position - position);
        float attenuation = 1.0 / (light.constant + light.linear * distance + light.quadratic * distance * distance);

        // Ambient
        vec3 ambient = light.color * 0.2 * vec3(texture2D(material.diffuse, texture_coordinate));

        // Diffuse
        float diffuse_factor = max(dot(normal, light_direction), 0.0);
        vec3  diffuse = light.color * 0.5 * diffuse_factor * vec3(texture2D(material.diffuse, texture_coordinate));

        // Specular
        vec3  camera_direction = normalize(camera_position - position);
        vec3  reflection_direction = reflect(-light_direction, normal);
        float specular_factor = pow(max(dot(camera_direction, reflection_direction), 0.0), material.shininess);
        vec3  specular = light.color * specular_factor * vec3(texture2D(material.specular, texture_coordinate));

        return (ambient + diffuse + specular) * attenuation;
    }



    void main()
    {
        vec3 ambient  = vec3(0.0);
        vec3 diffuse  = vec3(0.0);
        vec3 specular = vec3(0.0);
        vec3 total_light = vec3(0.0);

        vec3 normal = normalize(out_normal);


        // Light calculations.
        for (int i = 0; i < NUM_LIGHTS; i++)
        {
            total_light += calculate_pointlight(light[i], material, out_position, normal, out_texture_coordinate);
        }

        gl_FragColor =  vec4(total_light, 1.0);
    }

    """
]
simple_shaders    = [  # Using this shader to render single color.
    """
    #version 120

    uniform mat4 transformation;
    uniform mat4 perspective;
    uniform mat4 view;

    attribute vec3 position;

    void main()
    {    
        gl_Position =  perspective * view * transformation * vec4(position, 1.0);
    }

    """,
    """
    #version 120

    uniform vec3 color;

    void main()
    {    
        gl_FragColor = vec4(color, 1.0);
    }

    """
]
simple_2D_shaders = [
    """
    #version 120

    uniform mat4 transformation;
    uniform mat4 perspective;
    uniform mat4 view;

    attribute vec2 position;
    attribute vec2 texture_coordinate;

    varying vec2 out_texture_coordinate;

    void main()
    {    
        gl_Position =  perspective * view * transformation * vec4(position, 0.0, 1.0);
        out_texture_coordinate = texture_coordinate;
    }

    """,
    """
    #version 120

    varying vec2 out_texture_coordinate;

    uniform vec3 color;
    uniform sampler2D font_texture;

    void main()
    {    
        gl_FragColor = texture2D(font_texture, out_texture_coordinate).a * vec4(color, 1.0);
    }

    """
]

font_arial = Font('../resources/fonts/arial.fnt')
text_transform = Transform(location=(0, 0, 0), rotation=(0, 0, 0), scale=(10, 10, 10))

light_uniforms    = ['light[' + str(i) + attribute for attribute in ('].position', '].color', '].intensity', '].constant', '].linear', '].quadratic') for i in range(4)]
material_uniforms = ['material.' + x for x in ('diffuse', 'specular', 'emission', 'shininess')]

attributes = ['position', 'texture_coordinate', 'normal']
uniforms   = ['transformation', 'perspective', 'view', *light_uniforms, *material_uniforms]
program    = Shader.create(*object_shaders, attributes, uniforms)

simple_attributes = ['position']
simple_uniforms   = ['transformation', 'perspective', 'view', 'color']
simple_program    = Shader.create(*simple_shaders, simple_attributes, simple_uniforms)

simple_2D_attributes = ['position']
simple_2D_uniforms   = ['transformation', 'perspective', 'view', 'color']
simple_2D_program    = Shader.create(*simple_2D_shaders, simple_2D_attributes, simple_2D_uniforms)

CUBE = 0
SPHERE = 1
models = [create_cube(), load_model('../resources/models/sphere.obj')]

CONTAINER_DIFFUSE = 0
CONTAINER_SPECULAR = 1
CONTAINER_EMISSION = 2
ALUMINIUM_PLATE = 3
textures = [
    load_texture('../resources/textures/Container.png'),
    load_texture('../resources/textures/ContainerSpecular.png'),
    load_texture('../resources/textures/ContainerEmission.png'),
    load_texture('../resources/textures/AluminiumPlate.png')
]

entities = {
    CUBE  : {
        (CONTAINER_DIFFUSE, CONTAINER_SPECULAR, CONTAINER_EMISSION): [
            Transform(location=[randint(-6, 6), randint(-6, 6), randint(-8, -2)], rotation=[0, 0, 0], scale=[1, 1, 1])
            for i in range(5)],
        (ALUMINIUM_PLATE,)                                         : [
            Transform(location=[randint(-6, 6), randint(-6, 6), randint(-8, -2)], rotation=[0, 0, 0], scale=[1, 1, 1])
            for i in range(5)]
    },
    SPHERE: {
        (CONTAINER_DIFFUSE, CONTAINER_SPECULAR, CONTAINER_EMISSION): [
            Transform(location=[randint(-6, 6), randint(-6, 6), randint(-8, -2)], rotation=[0, 0, 0], scale=[1, 1, 1])
            for i in range(5)],
        (ALUMINIUM_PLATE,)                                         : [
            Transform(location=[randint(-6, 6), randint(-6, 6), randint(-8, -2)], rotation=[0, 0, 0], scale=[1, 1, 1])
            for i in range(5)]
    },
}

lights = {  # lights have no material but instead has two extra entity attributes: color and attenuation.
    CUBE  : [
        [Transform(location=[randint(-6, 6), randint(-6, 6), randint(-8, -2)], rotation=[0, 0, 0], scale=[1, 1, 1]),
         [0.5, 1.0, 1.0], [1.0, 0.009, 0.032]] for i in range(2)],
    SPHERE: [
        [Transform(location=[randint(-6, 6), randint(-6, 6), randint(-8, -2)], rotation=[0, 0, 0], scale=[1, 1, 1]),
         [0.5, 1.0, 1.0], [1.0, 0.009, 0.032]] for i in range(2)]
}

perspective_matrix = create_perspective_matrix(60, window.width / window.height, 0.1, 100)
camera = Transform(location=[0, 0, -10], rotation=[0, 0, 0], scale=[1, 1, 1])

entity_selected = 0
all_entities = get_all_entities(entities) + get_all_entities(lights) + [camera, text_transform]

pyglet.app.run()
