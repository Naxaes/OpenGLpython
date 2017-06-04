from pyglet.gl import *
from pyglet.window import Window
from ctypes import cast, pointer, POINTER, sizeof, create_string_buffer, c_char, c_float, c_uint

window = Window(width=480, height=480)


# Create shaders.
shaders_sources = [
    b'#version 120\nattribute vec3 position;\nvoid main() {  gl_Position = vec4(position, 1.0);  }',
    b'#version 120\nvoid main() {  gl_FragColor = vec4(1.0, 0.0, 1.0, 1.0);  }'
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
position_location = 0


# Create program.
program_handle = glCreateProgram()
glAttachShader(program_handle, shader_handles[0])
glAttachShader(program_handle, shader_handles[1])
glBindAttribLocation(program_handle, position_location, position_name)
glLinkProgram(program_handle)
glValidateProgram(program_handle)
glUseProgram(program_handle)


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
    glDrawArrays(GL_TRIANGLES, 0, len(vertices) // 3)


pyglet.app.run()

