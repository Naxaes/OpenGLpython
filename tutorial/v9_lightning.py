import numpy
from pyglet.gl import *
from pyglet.window import Window, mouse, key
from ctypes import cast, pointer, POINTER, byref, sizeof, create_string_buffer, c_char, c_float, c_uint
from math import cos, sin, tan, pi


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
shader_handles = []
shaders_sources = [
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

    uniform sampler2D texture;
    uniform Light light;
    uniform mat4  view;

    varying vec3 out_position;
    varying vec3 out_normal;
    varying vec2 out_texture_coordinate;

    void main()
    {
        vec3 camera_position = -view[3].xyz;
        vec3 vector_to_light = light.position - out_position;

        vec3  direction_to_light = normalize(vector_to_light);
        float distance_to_light  = length(vector_to_light);

        float angle_normal_and_light = dot(out_normal, direction_to_light);
        float diffuse_factor = clamp(angle_normal_and_light, 0.0, 1.0);        // or max(angle_normal_and_light, 1.0)
        float attenuation = 1.0 / (
            light.constant + light.linear * distance_to_light + light.quadratic * distance_to_light * distance_to_light
            );

        vec4 light_color = vec4(light.color * diffuse_factor, 1.0);
        vec4 color = texture2D(texture, out_texture_coordinate);

        vec4 ambient = color * 0.2;
        vec4 diffuse = color * light_color * attenuation;

        gl_FragColor = ambient + diffuse;
    }

    """
]
for i, source in enumerate(shaders_sources):
    handle = glCreateShader(GL_VERTEX_SHADER if i == 0 else GL_FRAGMENT_SHADER)
    glShaderSource(handle, 1, cast(pointer(pointer(create_string_buffer(source))), POINTER(POINTER(c_char))), None)
    glCompileShader(handle)
    shader_handles.append(handle)

# Create attributes.
position_name = create_string_buffer(b'position')
position_index = 0
texture_coordinate_name = create_string_buffer(b'texture_coordinate')
texture_coordinate_index = 1
normal_name = create_string_buffer(b'normal')
normal_index = 2

# NEW
try:
    # Create program.
    program_handle = glCreateProgram()
    glAttachShader(program_handle, shader_handles[0])
    glAttachShader(program_handle, shader_handles[1])
    glBindAttribLocation(program_handle, position_index, position_name)
    glBindAttribLocation(program_handle, texture_coordinate_index, texture_coordinate_name)
    glBindAttribLocation(program_handle, normal_index, normal_name)
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
    glGetProgramiv(program_handle, GL_INFO_LOG_LENGTH, byref(status))  # Getting the number of char in info log to 'status'
    output = create_string_buffer(status.value)  # status.value)
    glGetProgramInfoLog(program_handle, status, None, output)
    print(output.value.decode('utf-8'))


# Get uniform location.
transformation_name = create_string_buffer(b'transformation')
transformation_location = glGetUniformLocation(program_handle, cast(pointer(transformation_name), POINTER(c_char)))
perspective_name = create_string_buffer(b'perspective')
perspective_location = glGetUniformLocation(program_handle, cast(pointer(perspective_name), POINTER(c_char)))
view_name = create_string_buffer(b'view')
view_location = glGetUniformLocation(program_handle, cast(pointer(view_name), POINTER(c_char)))
light_position_name = create_string_buffer(b'light.position')
light_position_location = glGetUniformLocation(program_handle, cast(pointer(light_position_name), POINTER(c_char)))
light_color_name = create_string_buffer(b'light.color')
light_color_location = glGetUniformLocation(program_handle, cast(pointer(light_color_name), POINTER(c_char)))
light_intensity_name = create_string_buffer(b'light.intensity')
light_intensity_location = glGetUniformLocation(program_handle, cast(pointer(light_intensity_name), POINTER(c_char)))
light_constant_name = create_string_buffer(b'light.constant')
light_constant_location = glGetUniformLocation(program_handle, cast(pointer(light_constant_name), POINTER(c_char)))
light_linear_name = create_string_buffer(b'light.linear')
light_linear_location = glGetUniformLocation(program_handle, cast(pointer(light_linear_name), POINTER(c_char)))
light_quadratic_name = create_string_buffer(b'light.quadratic')
light_quadratic_location = glGetUniformLocation(program_handle, cast(pointer(light_quadratic_name), POINTER(c_char)))


# CHANGED
def create_cube():
    # Create and bind vbo.
    vertices = [
        -0.5, 0.5, -0.5, -0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, -0.5,  # Top.
        -0.5, -0.5, -0.5, 0.5, -0.5, -0.5, 0.5, -0.5, 0.5, -0.5, -0.5, 0.5,  # Bottom.
        -0.5, -0.5, -0.5, -0.5, -0.5, 0.5, -0.5, 0.5, 0.5, -0.5, 0.5, -0.5,  # Left.
        0.5, -0.5, 0.5, 0.5, -0.5, -0.5, 0.5, 0.5, -0.5, 0.5, 0.5, 0.5,  # Right.
        -0.5, -0.5, 0.5, 0.5, -0.5, 0.5, 0.5, 0.5, 0.5, -0.5, 0.5, 0.5,  # Front.
        0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5, -0.5, 0.5, 0.5, -0.5,  # Back.
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
        0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0,  # Top.
        0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0,  # Bottom.
        0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0,  # Left.
        0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0,  # Right.
        0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0,  # Front.
        0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0,  # Back.
    ]
    texture_coordinates_vbo = c_uint()
    glGenBuffers(1, texture_coordinates_vbo)
    glBindBuffer(GL_ARRAY_BUFFER, texture_coordinates_vbo)
    glBufferData(GL_ARRAY_BUFFER, len(texture_coordinates) * sizeof(c_float),
                 (c_float * len(texture_coordinates))(*texture_coordinates), GL_STATIC_DRAW)

    # Associate vertex attribute 2 with the bound vbo (our texture_coordinates vbo) above.
    glEnableVertexAttribArray(texture_coordinate_index)
    glVertexAttribPointer(texture_coordinate_index, 2, GL_FLOAT, GL_FALSE, 0, 0)  # CHANGED (to 2 instead of 3).

    # Create and bind vbo.
    normals = [
        0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,  # Top.
        0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0,  # Bottom.
        -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0,  # Left.
        1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0,  # Right.
        0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,  # Front.
        0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0,  # Back.
    ]
    normal_vbo = c_uint()
    glGenBuffers(1, normal_vbo)
    glBindBuffer(GL_ARRAY_BUFFER, normal_vbo)
    glBufferData(GL_ARRAY_BUFFER, len(normals) * sizeof(c_float), (c_float * len(vertices))(*vertices), GL_STATIC_DRAW)

    # Associate vertex attribute 0 (position) with the bound vbo above.
    glEnableVertexAttribArray(normal_index)
    glVertexAttribPointer(normal_index, 3, GL_FLOAT, GL_FALSE, 0, 0)

    # NEW Upload image to shader.
    texture = pyglet.image.load('../resources/textures/Container.png').get_texture()  # DIMENSIONS MUST BE POWER OF 2.
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
        0, 1, 3, 3, 1, 2,
        4, 5, 7, 7, 5, 6,
        8, 9, 11, 11, 9, 10,
        12, 13, 15, 15, 13, 14,
        16, 17, 19, 19, 17, 18,
        20, 21, 23, 23, 21, 22
    ]
    indexed_vbo = c_uint()
    glGenBuffers(1, indexed_vbo)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexed_vbo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * sizeof(c_uint), (c_uint * len(indices))(*indices),
                 GL_STATIC_DRAW)

    # Need to return texture so it doesn't get garbage collected.
    return vbo, texture_coordinates_vbo, normal_vbo, indexed_vbo, texture, len(indices)


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glUniformMatrix4fv(perspective_location, 1, GL_TRUE, perspective_matrix.ctypes.data_as(
        POINTER(GLfloat)))  # ctypes.data_as must be here and not at initialization.
    glUniformMatrix4fv(view_location, 1, GL_TRUE, camera.ctypes.data_as(POINTER(GLfloat)))  # NEW

    glUniform3f(light_position_location, 0.0, -1.0, 1.0)
    glUniform3f(light_color_location, 0.5, 1.0, 1.0)
    glUniform1f(light_constant_location, 1.0)  # Should always be 1!
    glUniform1f(light_linear_location, 0.009)  # Lower value, more light.
    glUniform1f(light_quadratic_location, 0.032)

    for (vbo, texture_coordinates_vbo, normal_vbo, indexed_vbo, texture, count), (location, rotation, scale) in zip(
            entities, entity_lrs):
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBindBuffer(GL_ARRAY_BUFFER, texture_coordinates_vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexed_vbo)

        glEnableVertexAttribArray(position_index)
        glEnableVertexAttribArray(texture_coordinate_index)

        glUniformMatrix4fv(
            transformation_location, 1, GL_TRUE,
            create_transformation_matrix(*location, *rotation, *scale).ctypes.data_as(POINTER(GLfloat))
        )
        glDrawElements(GL_TRIANGLES, count, GL_UNSIGNED_INT, 0)

        glDisableVertexAttribArray(position_index)
        glDisableVertexAttribArray(texture_coordinate_index)


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


@window.event
def on_key_press(symbol, modifiers):
    global entity_selected
    if key.LEFT == symbol:
        entity_selected = (entity_selected - 1) % len(entities)
    elif key.RIGHT == symbol:
        entity_selected = (entity_selected + 1) % len(entities)


entities = [create_cube() for x in range(10)]
entity_lrs = [
    [[numpy.random.randint(-6, 6), numpy.random.randint(-6, 6), -6], [0, 0, 0], [1, 1, 1]] for i in range(10)
]
entity_selected = 0
perspective_matrix = create_perspective_matrix(60, window.width / window.height, 0.1, 100)

# NEW
camera = create_transformation_matrix(0, 0, -10, 0, 0, 0, 1, 1, 1)
light = create_transformation_matrix(0, 2, -4, 0, 0, 0, 1, 1, 1)

pyglet.app.run()

