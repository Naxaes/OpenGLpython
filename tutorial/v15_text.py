import numpy
import os  # NEW
from numpy.random import randint
from pyglet.gl import *
from pyglet.window import Window, mouse, key
from ctypes import cast, pointer, POINTER, byref, sizeof, create_string_buffer, c_char, c_float, c_uint
from math import cos, sin, tan, pi


# We want a stencil buffer with 8-bit values. Don't know why we have to specify double_buffer,
# but it don't work otherwise. The other default values are good.
config = pyglet.gl.Config(stencil_size=8, double_buffer=True)
window = Window(width=480, height=480, config=config)


# NEW
class Font:

    def __init__(self, path):
        self.characters = {}
        texture_path = None

        for line in open(path):
            if line.startswith('page '):
                for statement in line.split(' '):
                    if statement.startswith('file'):
                        texture_path = statement.split('=')[-1].replace('"', '', 2).replace('\n', '')
            elif line.startswith('common '):
                pass
            elif line.startswith('char '):
                character_attributes = {}
                for statement in line.split(' '):
                    if '=' in statement:
                        attribute, value = statement.split('=')
                        character_attributes[attribute] = int(value)

                        if 'id=' in statement:
                            self.characters[int(value)] = character_attributes

        assert texture_path, 'Could not find the texture!'
        folder_path = os.path.split(path)[0]
        self.texture = load_texture(os.path.join(folder_path, texture_path))

    def create_text_quad(self, text, anchor_center=False):

        positions = []
        texture_coordinates = []
        indices = []

        cursor_x, cursor_y = 0, 0
        index = 0

        height = self.texture.height

        for character in text:
            info = self.characters[ord(character)]
            tx, ty = info['x'], info['y']
            tw, th = info['width'], info['height']
            x, y = cursor_x + info['xoffset'], cursor_y - info['yoffset']

            v = [
                x     , y,        # topleft
                x     , y - th,   # bottomleft
                x + tw, y - th,   # bottomright
                x + tw, y,        # topright
            ]
            t = [
                tx     , height - ty,        # topleft
                tx     , height - (ty + th), # bottomleft
                tx + tw, height - (ty + th), # bottomright
                tx + tw, height - ty         # topright
            ]
            i = [index, index + 1, index + 3, index + 3, index + 1, index + 2]

            positions.extend(v)
            texture_coordinates.extend(t)
            indices.extend(i)

            index += 4

            cursor_x += info['xadvance']

        # Normalize
        max_value = max((self.texture.height, self.texture.width))

        if anchor_center:
            width = cursor_x
            offset = (width / 2) / max_value
            positions = [i / max_value - offset for i in positions]
        else:
            positions = [i / max_value for i in positions]

        texture_coordinates = [i / max_value for i in texture_coordinates]

        return positions, texture_coordinates, indices


class Shader:

    bound = None  # This is okay if we assume we're only going to need one OpenGL context.

    def __init__(self, sources, attributes, uniforms):
        self.id, self.uniform = create_shader_program(sources, attributes, uniforms)

    def enable(self):
        glUseProgram(self.id)
        Shader.bound = self  # Just for safety.

    def disable(self):
        glUseProgram(0)
        Shader.bound = None

    def load_uniform_matrix(self, **uniforms):
        assert Shader.bound is self, "Must bind this shader before being able to load uniform."
        for name, data in uniforms.items():
            glUniformMatrix4fv(self.uniform[bytes(name, 'utf-8')], 1, GL_TRUE, data.ctypes.data_as(POINTER(GLfloat)))

    def load_uniform_floats(self, **uniforms):
        assert Shader.bound is self, "Must bind this shader before being able to load uniform."
        for name, data in uniforms.items():
            if isinstance(data, (float, int)):
                glUniform1f(self.uniform[bytes(name, 'utf-8')], data)
            else:
                functions = glUniform2f, glUniform3f, glUniform4f
                functions[len(data)-2](self.uniform[bytes(name, 'utf-8')], *data)

class VBO:

    def __init__(self, id_, dimension):
        self.id = id_
        self.dimension = dimension
        self.type = GL_FLOAT

    def enable(self, index):
        glBindBuffer(GL_ARRAY_BUFFER, self.id)
        glEnableVertexAttribArray(index)
        glVertexAttribPointer(index, self.dimension, self.type, GL_FALSE, 0, 0)


class Model:

    bound = None  # This is okay if we assume we're only going to need one OpenGL context.

    def __init__(self, vbos, indexed_vbo, count):
        self.vbos = vbos
        self.index_vbo = indexed_vbo
        self.count = count

    def enable(self):
        for index, vbo in enumerate(self.vbos):
            vbo.enable(index=index)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.index_vbo)
        Model.bound = self  # Safety.

    def disable(self):
        for index in range(len(self.vbos)):
            glDisableVertexAttribArray(index)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        Model.bound = None

    def render(self):
        assert Model.bound is self, "Model isn't bound."
        glDrawElements(GL_TRIANGLES, self.count, GL_UNSIGNED_INT, 0)


class Transform:

    def __init__(self, location, rotation, scale):
        self.location = list(location)  # Should really be a vector instead.
        self.rotation = list(rotation)
        self.scale = list(scale)

    def matrix(self):
        return create_transformation_matrix(
            *self.location, *self.rotation, *self.scale
        )


def create_transformation_matrix(x, y, z, rx, ry, rz, sx, sy, sz):
    # TODO optimize by creating the transformation matrix directly.
    translation = numpy.array(
        ((1, 0, 0, x),
         (0, 1, 0, y),
         (0, 0, 1, z),
         (0, 0, 0, 1)), dtype=GLfloat
    )

    rotation_x = numpy.array(
        ((1, 0, 0, 0),
         (0, cos(rx), -sin(rx), 0),
         (0, sin(rx), cos(rx), 0),
         (0, 0, 0, 1)), dtype=GLfloat
    )

    rotation_y = numpy.array(
        ((cos(ry), 0, sin(ry), 0),
         (0, 1, 0, 0),
         (-sin(ry), 0, cos(ry), 0),
         (0, 0, 0, 1)), dtype=GLfloat
    )

    rotation_z = numpy.array(
        ((cos(rz), -sin(rz), 0, 0),
         (sin(rz), cos(rz), 0, 0),
         (0, 0, 1, 0),
         (0, 0, 0, 1)), dtype=GLfloat
    )

    scale = numpy.array(
        ((sx, 0, 0, 0),
         (0, sy, 0, 0),
         (0, 0, sz, 0),
         (0, 0, 0, 1)), dtype=GLfloat
    )

    return translation @ rotation_x @ rotation_y @ rotation_z @ scale


def create_orthographic_matrix(left, right, bottom, top, near, far):
    a = 2 * near
    b = right - left
    c = top - bottom
    d = far - near

    return numpy.array(
        (
            (a / b, 0, (right + left) / b, 0),
            (0, a / c, (top + bottom) / c, 0),
            (0, 0, -(far + near) / d, -(2 * d) / d),
            (0, 0, -1, 0)
        ), dtype=GLfloat
    )


def create_perspective_matrix(fov, aspect_ratio, near, far):
    # TODO optimize by creating the transformation matrix directly.
    top = near * tan((pi / 180) * (fov / 2))
    bottom = -top
    right = top * aspect_ratio
    left = -right

    return create_orthographic_matrix(left, right, bottom, top, near, far)


def create_shader_program(sources, attributes, uniforms):
    shader_handles = []
    for i, source in enumerate(sources):
        handle = glCreateShader(GL_VERTEX_SHADER if i == 0 else GL_FRAGMENT_SHADER)
        glShaderSource(handle, 1, cast(pointer(pointer(create_string_buffer(source))), POINTER(POINTER(c_char))), None)
        glCompileShader(handle)
        shader_handles.append(handle)

    # Create attributes.
    attribute_mapping = []
    for attribute in attributes:
        attribute_mapping.append(create_string_buffer(attribute))

    try:
        # Create program.
        program_handle = glCreateProgram()
        glAttachShader(program_handle, shader_handles[0])
        glAttachShader(program_handle, shader_handles[1])
        for index, name in enumerate(attributes):
            glBindAttribLocation(program_handle, index, name)
        glLinkProgram(program_handle)
        glValidateProgram(program_handle)
        glUseProgram(program_handle)
    except pyglet.gl.GLException:
        # Print errors.
        status = GLint()
        glGetShaderiv(shader_handles[0], GL_INFO_LOG_LENGTH, byref(status))
        output = create_string_buffer(status.value)
        glGetShaderInfoLog(shader_handles[0], status, None, output)
        print(output.value.decode('utf-8'))
        status = GLint()
        glGetShaderiv(shader_handles[1], GL_INFO_LOG_LENGTH, byref(status))
        output = create_string_buffer(status.value)
        glGetShaderInfoLog(shader_handles[1], status, None, output)
        print(output.value.decode('utf-8'))
        status = GLint()
        glGetProgramiv(program_handle, GL_INFO_LOG_LENGTH,
                       byref(status))  # Getting the number of char in info log to 'status'
        output = create_string_buffer(status.value)  # status.value)
        glGetProgramInfoLog(program_handle, status, None, output)
        print(output.value.decode('utf-8'))

    # Get uniform location.
    uniform_mapping = {}
    for uniform in uniforms:
        name = create_string_buffer(uniform)
        location = glGetUniformLocation(program_handle, cast(pointer(name), POINTER(c_char)))
        uniform_mapping[uniform] = location

    return program_handle, uniform_mapping


def create_object(vertices, texture_coordinates, normals, indices):
    # Create and bind vbo.
    vbo = c_uint()
    glGenBuffers(1, vbo)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertices) * sizeof(c_float), (c_float * len(vertices))(*vertices), GL_STATIC_DRAW)

    # Associate vertex attribute 0 (position) with the bound vbo above.
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)

    glBindBuffer(GL_ARRAY_BUFFER, 0)

    # Create and bind vbo. CHANGED (REMOVED color vbo and replaced it with texture)
    texture_coordinates_vbo = c_uint()
    glGenBuffers(1, texture_coordinates_vbo)
    glBindBuffer(GL_ARRAY_BUFFER, texture_coordinates_vbo)
    glBufferData(GL_ARRAY_BUFFER, len(texture_coordinates) * sizeof(c_float),
                 (c_float * len(texture_coordinates))(*texture_coordinates), GL_STATIC_DRAW)

    # Associate vertex attribute 2 with the bound vbo (our texture_coordinates vbo) above.
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, 0)

    glBindBuffer(GL_ARRAY_BUFFER, 0)

    # Create and bind vbo.
    normal_vbo = c_uint()
    glGenBuffers(1, normal_vbo)
    glBindBuffer(GL_ARRAY_BUFFER, normal_vbo)
    glBufferData(GL_ARRAY_BUFFER, len(normals) * sizeof(c_float), (c_float * len(vertices))(*vertices), GL_STATIC_DRAW)

    # Associate vertex attribute 0 (position) with the bound vbo above.
    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, 0)

    glBindBuffer(GL_ARRAY_BUFFER, 0)

    # Create and bind indexed vbo.
    indexed_vbo = c_uint()
    glGenBuffers(1, indexed_vbo)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexed_vbo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * sizeof(c_uint), (c_uint * len(indices))(*indices),
                 GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    vbos = VBO(vbo, 3), VBO(texture_coordinates_vbo, 2), VBO(normal_vbo, 3)
    return Model(vbos=vbos, indexed_vbo=indexed_vbo, count=len(indices))

    # return vbo, texture_coordinates_vbo, normal_vbo, indexed_vbo, len(indices)


# NEW
def create_2D_object(vertices, texture_coordinates, indices):
    # Create and bind vbo.
    vbo = c_uint()
    glGenBuffers(1, vbo)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertices) * sizeof(c_float), (c_float * len(vertices))(*vertices), GL_STATIC_DRAW)

    # Associate vertex attribute 0 (position) with the bound vbo above.
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, 0)

    glBindBuffer(GL_ARRAY_BUFFER, 0)

    # Create and bind vbo.
    texture_coordinates_vbo = c_uint()
    glGenBuffers(1, texture_coordinates_vbo)
    glBindBuffer(GL_ARRAY_BUFFER, texture_coordinates_vbo)
    glBufferData(GL_ARRAY_BUFFER, len(texture_coordinates) * sizeof(c_float),
                 (c_float * len(texture_coordinates))(*texture_coordinates), GL_STATIC_DRAW)

    # Associate vertex attribute 2 with the bound vbo (our texture_coordinates vbo) above.
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, 0)

    glBindBuffer(GL_ARRAY_BUFFER, 0)

    # Create and bind indexed vbo.
    indexed_vbo = c_uint()
    glGenBuffers(1, indexed_vbo)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexed_vbo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * sizeof(c_uint), (c_uint * len(indices))(*indices),
                 GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    vbos = VBO(vbo, 2), VBO(texture_coordinates_vbo, 2)
    return Model(vbos=vbos, indexed_vbo=indexed_vbo, count=len(indices))


def create_cube():
    vertices = [
        -0.5, 0.5, -0.5, -0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, -0.5,  # Top.
        -0.5, -0.5, -0.5, 0.5, -0.5, -0.5, 0.5, -0.5, 0.5, -0.5, -0.5, 0.5,  # Bottom.
        -0.5, -0.5, -0.5, -0.5, -0.5, 0.5, -0.5, 0.5, 0.5, -0.5, 0.5, -0.5,  # Left.
        0.5, -0.5, 0.5, 0.5, -0.5, -0.5, 0.5, 0.5, -0.5, 0.5, 0.5, 0.5,  # Right.
        -0.5, -0.5, 0.5, 0.5, -0.5, 0.5, 0.5, 0.5, 0.5, -0.5, 0.5, 0.5,  # Front.
        0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5, -0.5, 0.5, 0.5, -0.5,  # Back.
    ]

    texture_coordinates = [
        0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0,  # Top.
        0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0,  # Bottom.
        0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0,  # Left.
        0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0,  # Right.
        0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0,  # Front.
        0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0,  # Back.
    ]

    normals = [
        0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,  # Top.
        0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0,  # Bottom.
        -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0,  # Left.
        1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0,  # Right.
        0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,  # Front.
        0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0,  # Back.
    ]

    indices = [
        0, 1, 3, 3, 1, 2,
        4, 5, 7, 7, 5, 6,
        8, 9, 11, 11, 9, 10,
        12, 13, 15, 15, 13, 14,
        16, 17, 19, 19, 17, 18,
        20, 21, 23, 23, 21, 22
    ]

    return create_object(vertices, texture_coordinates, normals, indices)


def load_model(path):
    vertices = []
    normals = []
    texture_coordinates = []

    with open(path) as text_file:  # TODO Is it streamed? Does it matter?

        line = text_file.readline()

        while True:

            if line.startswith('v '):
                _, x, y, z = line.split()
                vertices.append((float(x), float(y), float(z)))
            elif line.startswith('vt '):
                _, u, t = line.split()
                texture_coordinates.append((float(u), float(t)))
            elif line.startswith('vn '):
                _, x, y, z = line.split()
                normals.append((float(x), float(y), float(z)))
            elif line.startswith('f ') or line == '':
                break

            line = text_file.readline()

        indices = []
        unique_data = []
        sorted_vertices = []
        sorted_normals = []
        sorted_texture_coordinates = []
        index = 0

        while line != '':
            if not line.startswith('f'):
                line = text_file.readline()
                continue

            _, *faces = line.split(' ')

            for face in faces:
                vertex = face.split('/')
                if vertex not in unique_data:
                    unique_data.append(vertex)
                    indices.append(index)
                    vertex_index, texture_index, normal_index = vertex
                    vertex_index, texture_index, normal_index = int(vertex_index), int(texture_index), int(normal_index)
                    sorted_vertices.extend(vertices[vertex_index - 1])
                    sorted_normals.extend(normals[normal_index - 1])
                    sorted_texture_coordinates.extend(texture_coordinates[texture_index - 1])
                    index += 1
                else:
                    indices.append(unique_data.index(vertex))

            line = text_file.readline()

    return create_object(sorted_vertices, sorted_texture_coordinates, sorted_normals, indices)


def load_texture(path, min_filter=GL_LINEAR, max_filter=GL_LINEAR, wrap_s=GL_CLAMP_TO_EDGE, wrap_t=GL_CLAMP_TO_EDGE):
    texture = pyglet.image.load(path).get_texture()  # DIMENSIONS MUST BE POWER OF 2.
    glBindTexture(GL_TEXTURE_2D, texture.id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, min_filter)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, max_filter)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap_s)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap_t)
    glBindTexture(GL_TEXTURE_2D, 0)
    return texture


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
    glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)  # Keep if depth test fails, keep if stencil test fails, replace if both succeed.

    glStencilFunc(GL_ALWAYS, 1, 0xFF)          # Always fill the stencil buffer.
    glStencilMask(0xFF)                        # 0xFF turns on writes the stencil mask. 0x00 disables writes.

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
        program.load_uniform_floats(**{'light[' + str(i) + '].position':  entity[0].location})
        program.load_uniform_floats(**{'light[' + str(i) + '].color':     entity[1]})
        program.load_uniform_floats(**{'light[' + str(i) + '].constant':  entity[2][0]})
        program.load_uniform_floats(**{'light[' + str(i) + '].linear':    entity[2][1]})
        program.load_uniform_floats(**{'light[' + str(i) + '].quadratic': entity[2][2]})

    glActiveTexture(GL_TEXTURE0)

    for model_index, texture_mapping in entities.items():
        model = models[model_index]
        model.enable()

        for texture_index, entity_list in texture_mapping.items():

            # Make bindings for texture.
            texture = textures[texture_index]
            glBindTexture(GL_TEXTURE_2D, texture.id)

            for entity in entity_list:
                transform = entity

                # Prepare entities of specific model and texture, and draw.
                program.load_uniform_matrix(transformation=transform.matrix())
                model.render()

    # Stencil shader
    glDisable(GL_DEPTH_TEST)             # Disable depth tests.
    glStencilFunc(GL_NOTEQUAL, 1, 0xFF)  # Only draw where the stencil buffer isn't 1.
    glStencilMask(0x00)                  # Disable writes.

    transform  = get_selected_entity_transform()
    sx, sy, sz = transform.scale
    # Make the transform slightly bigger so it's visible.
    transform   = create_transformation_matrix(*transform.location, *transform.rotation, sx*1.1, sy*1.1, sz*1.1)
    model_index = get_entity_model_index(all_entities[entity_selected])
    if model_index is not None:  # CHANGED
        model = models[model_index]

        simple_program.enable()
        simple_program.load_uniform_matrix(perspective=perspective_matrix, view=camera.matrix(), transformation=transform)
        simple_program.load_uniform_floats(color=[255, 0, 255])

        model.enable()
        model.render()


    # NEW - Render text
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)

    text_positions, text_texture_coordinates, text_indices = font_arial.create_text_quad("Hello", anchor_center=True)
    text = create_2D_object(text_positions, text_texture_coordinates, text_indices)

    simple_2D_program.enable()
    simple_2D_program.load_uniform_matrix(perspective=perspective_matrix, view=camera.matrix(), transformation=text_transform.matrix())
    simple_2D_program.load_uniform_floats(color=[255, 255, 255])

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, font_arial.texture.id)

    text.enable()
    text.render()



# Create shaders.
object_shaders = [
    b"""
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
    b"""
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

    const int NUM_LIGHTS = 4;

    uniform sampler2D texture;
    uniform Light light[NUM_LIGHTS];
    uniform mat4  view;

    varying vec3 out_position;
    varying vec3 out_normal;
    varying vec2 out_texture_coordinate;

    void main()
    {
        vec3 camera_position = -view[3].xyz;
        vec4 light_color = vec4(0.0, 0.0, 0.0, 0.0);
        float attenuation = 0.0;

        for (int i = 0; i < NUM_LIGHTS; i++) {
            vec3 vector_to_light = light[i].position - out_position;

            vec3  direction_to_light = normalize(vector_to_light);
            float distance_to_light  = length(vector_to_light);

            float angle_normal_and_light = dot(out_normal, direction_to_light);
            float diffuse_factor = clamp(angle_normal_and_light, 0.0, 1.0);        // or max(angle_normal_and_light, 1.0)
            attenuation += 1.0 / (
                light[i].constant + light[i].linear * distance_to_light + light[i].quadratic * distance_to_light * distance_to_light
                );

            light_color += vec4(light[i].color * diffuse_factor, 1.0);
        }

        vec4 color = texture2D(texture, out_texture_coordinate);

        vec4 ambient = color * 0.2;
        vec4 diffuse = color * light_color * attenuation;

        gl_FragColor = ambient + diffuse;
    }

    """
]
simple_shaders = [  # Using this shader to render single color.
    b"""
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
    b"""
    #version 120

    uniform vec3 color;

    void main()
    {    
        gl_FragColor = vec4(color, 1.0);
    }

    """
]

simple_2D_shaders = [  # NEW - Render 2D-model with a single color.
    b"""
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
    b"""
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

font_arial = Font('../resources/fonts/arial.fnt')  # NEW
text_transform = Transform(location=(0, 0, 0), rotation=(0, 0, 0), scale=(10, 10, 10))  # NEW

temp = []
for i in range(4):
    for attribute in [b'].position', b'].color', b'].intensity', b'].constant', b'].linear', b'].quadratic']:
        temp.append(b'light[' + bytes(str(i), 'utf-8') + attribute)

attributes = [b'position', b'texture_coordinate', b'normal']
uniforms = [
    b'transformation', b'perspective', b'view', *temp
]
program = Shader(object_shaders, attributes, uniforms)

simple_attributes = [b'position']
simple_uniforms = [b'transformation', b'perspective', b'view', b'color']
simple_program = Shader(simple_shaders, simple_attributes, simple_uniforms)

simple_2D_attributes = [b'position']
simple_2D_uniforms = [b'transformation', b'perspective', b'view', b'color']
simple_2D_program = Shader(simple_2D_shaders, simple_2D_attributes, simple_2D_uniforms)

CUBE = 0
SPHERE = 1
models = [create_cube(), load_model('../resources/models/sphere.obj')]

CONTAINER = 0
ALUMINIUM_PLATE = 1
textures = [
    load_texture('../resources/textures/Container.png'), load_texture('../resources/textures/AluminiumPlate.png')
]

entities = {
    CUBE  : {
        CONTAINER      : [Transform(location=[randint(-6, 6), randint(-6, 6), randint(-8, -2)], rotation=[0, 0, 0], scale=[1, 1, 1]) for i in range(5)],
        ALUMINIUM_PLATE: [Transform(location=[randint(-6, 6), randint(-6, 6), randint(-8, -2)], rotation=[0, 0, 0], scale=[1, 1, 1]) for i in range(5)]
    },
    SPHERE: {
        CONTAINER      : [Transform(location=[randint(-6, 6), randint(-6, 6), randint(-8, -2)], rotation=[0, 0, 0], scale=[1, 1, 1]) for i in range(5)],
        ALUMINIUM_PLATE: [Transform(location=[randint(-6, 6), randint(-6, 6), randint(-8, -2)], rotation=[0, 0, 0], scale=[1, 1, 1]) for i in range(5)]
    },
}

lights = {  # lights have no material but instead has two extra entity attributes: color and attenuation.
    CUBE  : [[Transform(location=[randint(-6, 6), randint(-6, 6), randint(-8, -2)], rotation=[0, 0, 0], scale=[1, 1, 1]), [0.5, 1.0, 1.0], [1.0, 0.009, 0.032]] for i in range(2)],
    SPHERE: [[Transform(location=[randint(-6, 6), randint(-6, 6), randint(-8, -2)], rotation=[0, 0, 0], scale=[1, 1, 1]), [0.5, 1.0, 1.0], [1.0, 0.009, 0.032]] for i in range(2)]
}

perspective_matrix = create_perspective_matrix(60, window.width / window.height, 0.1, 100)
camera = Transform(location=[0, 0, -10], rotation=[0, 0, 0], scale=[1, 1, 1])


entity_selected = 0
all_entities = get_all_entities(entities) + get_all_entities(lights) + [camera, text_transform]  # CHANGED

pyglet.app.run()
