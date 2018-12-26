from pyglet.gl import *
from pyglet.window import Window, mouse, key
from ctypes import cast, pointer, POINTER, sizeof, create_string_buffer, c_char, c_float, c_uint
from math import cos, sin, tan, pi
import numpy


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


window = Window(width=480, height=480)
glEnable(GL_DEPTH_TEST)


# Create shaders.
shaders_sources = [
    b"""
    #version 120
    uniform mat4 transformation;
    uniform mat4 perspective;
    attribute vec3 position;
    attribute vec2 texture_coordinate;
    varying vec2 out_texture_coordinate;
    void main()
    {
        gl_Position = perspective * transformation * vec4(position, 1.0);
        out_texture_coordinate = texture_coordinate;
    }
    """,
    b"""
    #version 120
    uniform sampler2D texture;
    varying vec2 out_texture_coordinate;
    void main()
    {  
       gl_FragColor = texture2D(texture, out_texture_coordinate);  
    }
    """
]
shader_handles = []
for i, source in enumerate(shaders_sources):
    handle = glCreateShader(GL_VERTEX_SHADER if i == 0 else GL_FRAGMENT_SHADER)
    glShaderSource(handle, 1, cast(pointer(pointer(create_string_buffer(source))), POINTER(POINTER(c_char))), None)
    glCompileShader(handle)
    shader_handles.append(handle)


# Create attributes.
position_name = create_string_buffer(b'position')
position_index = 0
texture_coordinate_name = create_string_buffer(b'texture_coordinate')  # NEW!
texture_coordinate_index = 1


# Create program.
program_handle = glCreateProgram()
glAttachShader(program_handle, shader_handles[0])
glAttachShader(program_handle, shader_handles[1])
glBindAttribLocation(program_handle, position_index, position_name)
glBindAttribLocation(program_handle, texture_coordinate_index, texture_coordinate_name)  # NEW!
glLinkProgram(program_handle)
glValidateProgram(program_handle)
glUseProgram(program_handle)


# Get uniform location.
transformation_name = create_string_buffer(b'transformation')
transformation_location = glGetUniformLocation(program_handle, cast(pointer(transformation_name), POINTER(c_char)))
perspective_name = create_string_buffer(b'perspective')
perspective_location = glGetUniformLocation(program_handle, cast(pointer(perspective_name), POINTER(c_char)))


# CHANGED
def create_cube():
    # Create and bind vbo.
    vertices = [
        -0.5,  0.5, -0.5, -0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5, -0.5,  # Top.
        -0.5, -0.5, -0.5,  0.5, -0.5, -0.5,  0.5, -0.5,  0.5, -0.5, -0.5,  0.5,  # Bottom.
        -0.5, -0.5, -0.5, -0.5, -0.5,  0.5, -0.5,  0.5,  0.5, -0.5,  0.5, -0.5,  # Left.
         0.5, -0.5,  0.5,  0.5, -0.5, -0.5,  0.5,  0.5, -0.5,  0.5,  0.5,  0.5,  # Right.
        -0.5, -0.5,  0.5,  0.5, -0.5,  0.5,  0.5,  0.5,  0.5, -0.5,  0.5,  0.5,  # Front.
         0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5,  0.5, -0.5,  0.5,  0.5, -0.5,  # Back.
    ]
    vbo = c_uint()
    glGenBuffers(1, vbo)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertices) * sizeof(c_float), (c_float * len(vertices))(*vertices), GL_STATIC_DRAW)

    # Associate vertex attribute 0 (position) with the bound vbo above.
    glEnableVertexAttribArray(position_index)
    glVertexAttribPointer(position_index, 3, GL_FLOAT, GL_FALSE, 0, 0)


    # Create and bind vbo. CHANGED (REMOVED color vbo and replaced it with texture)
    texture_coordinates = [
        0.0, 0.0,  0.0, 1.0,  1.0, 1.0,  1.0, 0.0,  # Top.
        0.0, 0.0,  0.0, 1.0,  1.0, 1.0,  1.0, 0.0,  # Bottom.
        0.0, 0.0,  0.0, 1.0,  1.0, 1.0,  1.0, 0.0,  # Left.
        0.0, 0.0,  0.0, 1.0,  1.0, 1.0,  1.0, 0.0,  # Right.
        0.0, 0.0,  0.0, 1.0,  1.0, 1.0,  1.0, 0.0,  # Front.
        0.0, 0.0,  0.0, 1.0,  1.0, 1.0,  1.0, 0.0,  # Back.
    ]
    texture_coordinates_vbo = c_uint()
    glGenBuffers(1, texture_coordinates_vbo)
    glBindBuffer(GL_ARRAY_BUFFER, texture_coordinates_vbo)
    glBufferData(GL_ARRAY_BUFFER, len(texture_coordinates) * sizeof(c_float), (c_float * len(texture_coordinates))(*texture_coordinates), GL_STATIC_DRAW)

    # Associate vertex attribute 2 with the bound vbo (our texture_coordinates vbo) above.
    glEnableVertexAttribArray(texture_coordinate_index)
    glVertexAttribPointer(texture_coordinate_index, 2, GL_FLOAT, GL_FALSE, 0, 0)  # CHANGED (to 2 instead of 3).


    # NEW Upload image to shader.
    texture = pyglet.image.load('../resources/textures/Leather.png').get_texture()  # DIMENSIONS MUST BE POWER OF 2.
    glBindTexture(GL_TEXTURE_2D, texture.id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glActiveTexture(GL_TEXTURE0)


    # Create and bind indexed vbo.
    indices = [
        0,  1,  3,  3,  1,  2,
        4,  5,  7,  7,  5,  6,
        8,  9,  11, 11, 9,  10,
        12, 13, 15, 15, 13, 14,
        16, 17, 19, 19, 17, 18,
        20, 21, 23, 23, 21, 22
    ]
    indexed_vbo = c_uint()
    glGenBuffers(1, indexed_vbo)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexed_vbo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * sizeof(c_uint), (c_uint * len(indices))(*indices), GL_STATIC_DRAW)

    # Need to return texture so it doesn't get garbage collected.
    return vbo, texture_coordinates_vbo, indexed_vbo, texture, len(indices)


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUniformMatrix4fv(perspective_location, 1, GL_TRUE, perspective_matrix.ctypes.data_as(POINTER(GLfloat)))  # ctypes.data_as must be here and not at initialization.


    # CHANGED
    for (vbo, texture_coordinates_vbo, indexed_vbo, texture, count), (location, rotation, scale) in zip(entities, entity_lrs):

        # glBindBuffer(GL_ARRAY_BUFFER, vbo)
        # glBindBuffer(GL_ARRAY_BUFFER, texture_coordinates_vbo)
        # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexed_vbo)
        #
        # glEnableVertexAttribArray(position_index)
        # glEnableVertexAttribArray(texture_coordinate_index)

        glUniformMatrix4fv(
            transformation_location, 1, GL_TRUE,
            create_transformation_matrix(*location, *rotation, *scale).ctypes.data_as(POINTER(GLfloat))
        )
        glDrawElements(GL_TRIANGLES, count, GL_UNSIGNED_INT, 0)

    # glDisableVertexAttribArray(position_index)
    # glDisableVertexAttribArray(texture_coordinate_index)


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    location, rotation, scale = entity_lrs[entity_selected]
    if buttons == mouse.LEFT:
        location[0] += dx / 250
        location[1] += dy / 250
    elif buttons == mouse.MIDDLE:  # Scroll button.
        scale[0] += dx / 250
        scale[1] += dy / 250
    elif buttons == mouse.RIGHT:
        rotation[1] += dx / 100
        rotation[0] -= dy / 100


@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    location, rotation, scale = entity_lrs[entity_selected]
    location[2] -= scroll_y / 10


# NEW
@window.event
def on_key_press(symbol, modifiers):
    global entity_selected
    if key.LEFT:
        entity_selected = (entity_selected - 1) % len(entities)
    elif key.RIGHT:
        entity_selected = (entity_selected + 1) % len(entities)


# NEW
entities = [create_cube() for x in range(10)]
entity_lrs = [
    [[numpy.random.randint(-6, 6), numpy.random.randint(-6, 6), -10], [0, 0, 0], [1, 1, 1]] for i in range(10)
]
entity_selected = 0
perspective_matrix = create_perspective_matrix(60, window.width / window.height, 0.1, 100)


pyglet.app.run()

