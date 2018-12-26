from pyglet.gl import *
from pyglet.window import Window, mouse
from ctypes import cast, pointer, POINTER, sizeof, create_string_buffer, c_char, c_float, c_uint
from math import cos, sin, tan, pi
import numpy


def create_transformation_matrix(x, y, z, rx, ry, rz, sx, sy, sz):
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


def create_orthographic_matrix(left, right, bottom, top, near, far):  # NEW!
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


def create_perspective_matrix(fov, aspect_ratio, near, far):  # NEW!
    top = near * tan((pi / 180) * (fov / 2))
    bottom = -top
    right = top * aspect_ratio
    left = -right

    return create_orthographic_matrix(left, right, bottom, top, near, far)


window = Window(width=480, height=480)
glEnable(GL_DEPTH_TEST)


# Create shaders.
shaders_sources = [  # CHANGED!
    b"""
    #version 120
    uniform mat4 transformation;
    uniform mat4 perspective;
    attribute vec3 color;
    attribute vec3 position;
    varying vec4 out_color;
    void main()
    {
        gl_Position = perspective * transformation * vec4(position, 1.0);
        out_color = vec4(color, 1.0);
    }
    """,
    b"""
    #version 120
    varying vec4 out_color;
    void main()
    {  
       gl_FragColor = out_color;  
    }
    """
]
shader_handles = []
for i, source in enumerate(shaders_sources):
    handle = glCreateShader(GL_VERTEX_SHADER if i == 0 else GL_FRAGMENT_SHADER)
    string_buffer = create_string_buffer(source)
    glShaderSource(handle, 1, cast(pointer(pointer(string_buffer)), POINTER(POINTER(c_char))), None)
    glCompileShader(handle)
    shader_handles.append(handle)


# Create attributes.
position_name = create_string_buffer(b'position')
position_index = 0
color_name = create_string_buffer(b'color')
color_index = 1


# Create program.
program_handle = glCreateProgram()
glAttachShader(program_handle, shader_handles[0])
glAttachShader(program_handle, shader_handles[1])
glBindAttribLocation(program_handle, position_index, position_name)  # Have to be done before linking (unlike uniforms).
glBindAttribLocation(program_handle, color_index, color_name)
glLinkProgram(program_handle)
glValidateProgram(program_handle)
glUseProgram(program_handle)


# Get uniform location.
transformation_name = create_string_buffer(b'transformation')
transformation_location = glGetUniformLocation(program_handle, cast(pointer(transformation_name), POINTER(c_char)))
perspective_name = create_string_buffer(b'perspective')  # NEW
perspective_location = glGetUniformLocation(program_handle, cast(pointer(perspective_name), POINTER(c_char)))


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


# Associate vertex attribute 0 with the bound vbo above.
glEnableVertexAttribArray(position_index)
glVertexAttribPointer(position_index, 3, GL_FLOAT, GL_FALSE, 0, 0)


# Create and bind vbo.
colors = [
    0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0,
    0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0,
    0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0,
    1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0,
    0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0,
]
color_vbo = c_uint()
glGenBuffers(1, color_vbo)
glBindBuffer(GL_ARRAY_BUFFER, color_vbo)
glBufferData(GL_ARRAY_BUFFER, len(colors) * sizeof(c_float), (c_float * len(colors))(*colors), GL_STATIC_DRAW)


# Associate vertex attribute 1 with the bound (our color vbo) above.
glEnableVertexAttribArray(color_index)
glVertexAttribPointer(color_index, 3, GL_FLOAT, GL_FALSE, 0, 0)


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


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUniformMatrix4fv(
        perspective_location, 1, GL_TRUE,
        create_perspective_matrix(60, window.width / window.height, 0.1, 100).ctypes.data_as(POINTER(GLfloat))
    )
    glUniformMatrix4fv(
        transformation_location, 1, GL_TRUE,
        create_transformation_matrix(*location, *rotation, *scale).ctypes.data_as(POINTER(GLfloat))
    )
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, 0)


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global location
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
    global location
    location[2] -= scroll_y / 10


location = [0, 0, -3]  # CHANGED (so the cube is visible at the start).
rotation = [0, 0, 0]
scale = [1, 1, 1]

pyglet.app.run()

