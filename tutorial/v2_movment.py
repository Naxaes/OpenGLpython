from pyglet.gl import *
from pyglet.window import Window
from ctypes import cast, pointer, POINTER, sizeof, create_string_buffer, c_char, c_float, c_uint
from math import cos, sin
import numpy


# NEW
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
shaders_sources = [
    # CHANGED
    b'#version 120\nattribute vec3 position;\nuniform mat4 transformation;\nvoid main() {  gl_Position = transformation * vec4(position, 1.0);  }',
    b'#version 120\nvoid main() {  gl_FragColor = vec4(1.0, 0.0, 1.0, 1.0);  }'
]
shader_handles = []
for i, source in enumerate(shaders_sources):
    handle = glCreateShader(GL_VERTEX_SHADER if i == 0 else GL_FRAGMENT_SHADER)
    transformation_name = create_string_buffer(source)
    glShaderSource(handle, 1, cast(pointer(pointer(transformation_name)), POINTER(POINTER(c_char))), None)
    glCompileShader(handle)
    shader_handles.append(handle)


# Create attributes.
position_name = create_string_buffer(b'position')
position_location = 0


# Create program.
program_handle = glCreateProgram()
glAttachShader(program_handle, shader_handles[0])
glAttachShader(program_handle, shader_handles[1])
glBindAttribLocation(program_handle, position_location, position_name)
glLinkProgram(program_handle)
glValidateProgram(program_handle)
glUseProgram(program_handle)


# Get uniform location.
transformation_name = create_string_buffer(b'transformation')  # NEW
transformation_location = glGetUniformLocation(program_handle, cast(pointer(transformation_name), POINTER(c_char)))  # NEW


# Create and bind vbo.
vertices = [
    -0.5,  0.5, 0.0,  # Left top.
    -0.5, -0.5, 0.0,  # Left bottom.
     0.5,  0.5, 0.0,  # Right top.

     0.5,  0.5, 0.0,  # Right top.
    -0.5, -0.5, 0.0,  # Left bottom.
     0.5, -0.5, 0.0,  # Right bottom.
]
vbo = c_uint()
glGenBuffers(1, vbo)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, len(vertices) * sizeof(c_float), (c_float * len(vertices))(*vertices), GL_STATIC_DRAW)


# Associate vertex attribute 0 (position) with the bound vbo above.
glEnableVertexAttribArray(position_location)
glVertexAttribPointer(position_location, 3, GL_FLOAT, GL_FALSE, 0, 0)


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glUniformMatrix4fv(
        transformation_location, 1, GL_TRUE,
        create_transformation_matrix(*location, *rotation, *scale).ctypes.data_as(POINTER(GLfloat))
    )  # NEW
    glDrawArrays(GL_TRIANGLES, 0, len(vertices) // 3)


# NEW
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
        rotation[0] += dy / 100


# NEW
location = [0, 0, 0]
rotation = [0, 0, 0]
scale    = [1, 1, 1]

pyglet.app.run()
