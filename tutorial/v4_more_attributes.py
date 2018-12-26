from pyglet.gl import *
from pyglet.window import Window
from ctypes import cast, pointer, POINTER, sizeof, create_string_buffer, c_char, c_float, c_uint
from math import cos, sin
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


window = Window(width=480, height=480)


# Create shaders.
shaders_sources = [  # CHANGED
    b"""
    #version 120
    uniform mat4 transformation;
    attribute vec3 color;
    attribute vec3 position;
    varying vec4 out_color;
    void main()
    {
        gl_Position = transformation * vec4(position, 1.0);
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
color_name = create_string_buffer(b'color')  # NEW
color_index = 1


# Create program.
program_handle = glCreateProgram()
glAttachShader(program_handle, shader_handles[0])
glAttachShader(program_handle, shader_handles[1])
glBindAttribLocation(program_handle, position_index, position_name)
glBindAttribLocation(program_handle, color_index, color_name)  # NEW
glLinkProgram(program_handle)
glValidateProgram(program_handle)
glUseProgram(program_handle)


# Get uniform location.
transformation_name = create_string_buffer(b'transformation')
transformation_location = glGetUniformLocation(program_handle, cast(pointer(transformation_name), POINTER(c_char)))


# Create and bind vbo.
vertices = [
    -0.5,  0.5, 0.0,  # Left top.
    -0.5, -0.5, 0.0,  # Left bottom.
     0.5, -0.5, 0.0,  # Right bottom.
     0.5,  0.5, 0.0,  # Right top.
]
vbo = c_uint()
glGenBuffers(1, vbo)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, len(vertices) * sizeof(c_float), (c_float * len(vertices))(*vertices), GL_STATIC_DRAW)


# Associate vertex attribute 0 ('position' in our shader) with the bound vbo above.
glEnableVertexAttribArray(position_index)
glVertexAttribPointer(position_index, 3, GL_FLOAT, GL_FALSE, 0, 0)


# NEW Create and bind vbo.
colors = [
    1.0, 0.0, 0.0,  # Left top.
    0.0, 1.0, 0.0,  # Left bottom.
    0.0, 0.0, 1.0,  # Right bottom.
    1.0, 0.0, 1.0,  # Right top.
]
color_vbo = c_uint()
glGenBuffers(1, color_vbo)
glBindBuffer(GL_ARRAY_BUFFER, color_vbo)
glBufferData(GL_ARRAY_BUFFER, len(colors) * sizeof(c_float), (c_float * len(colors))(*colors), GL_STATIC_DRAW)


# NEW Associate vertex attribute 1 ('color' in our shader) with the bound (our color vbo) above.
glEnableVertexAttribArray(color_index)
glVertexAttribPointer(color_index, 3, GL_FLOAT, GL_FALSE, 0, 0)


# Create and bind indexed vbo.
indices = [
    0, 1, 3,
    3, 1, 2,
]
indexed_vbo = c_uint()
glGenBuffers(1, indexed_vbo)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexed_vbo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * sizeof(c_uint), (c_uint * len(indices))(*indices), GL_STATIC_DRAW)


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glUniformMatrix4fv(
        transformation_location, 1, GL_TRUE,
        create_transformation_matrix(*location, *rotation, *scale).ctypes.data_as(POINTER(GLfloat))
    )
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, 0)


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global location
    if buttons == 1:  # Right mouse button.
        location[0] += dx / 250
        location[1] += dy / 250
    elif buttons == 2:  # Scroll button.
        scale[0] += dx / 250
        scale[1] += dy / 250
    elif buttons == 4:  # Left mouse button.
        rotation[1] += dx / 100
        rotation[0] -= dy / 100


location = [0, 0, 0]
rotation = [0, 0, 0]
scale = [1, 1, 1]

pyglet.app.run()

