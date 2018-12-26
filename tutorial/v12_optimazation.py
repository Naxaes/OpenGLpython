import numpy
from numpy.random import randint
from pyglet.gl import *
from pyglet.window import Window, mouse, key
from ctypes import cast, pointer, POINTER, byref, sizeof, create_string_buffer, c_char, c_float, c_uint
from math import cos, sin, tan, pi

window = Window(width=480, height=480)
glEnable(GL_DEPTH_TEST)
glEnable(GL_CULL_FACE)   # NEW
glCullFace(GL_BACK)


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

    # NEW
    # Create attributes.
    attribute_mapping = []
    for attribute in attributes:
        attribute_mapping.append(create_string_buffer(attribute))

    # NEW
    try:
        # Create program.
        program_handle = glCreateProgram()
        glAttachShader(program_handle, shader_handles[0])
        glAttachShader(program_handle, shader_handles[1])
        for index, name in enumerate(attributes):  # CHANGED
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
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, 0)  # CHANGED (to 2 instead of 3).

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

    return vbo, texture_coordinates_vbo, normal_vbo, indexed_vbo, len(indices)


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


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    location, rotation, scale = camera
    if buttons == mouse.LEFT:
        location[0] += dx / 250
        location[1] += dy / 250
    elif buttons == mouse.MIDDLE:  # Scroll button.
        scale[0] += dx / 250
        scale[1] += dy / 250
    elif buttons == mouse.RIGHT:
        rotation[1] += dx / 250
        rotation[0] -= dy / 250


@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    location, rotation, scale = camera
    location[2] -= scroll_y / 10
    location[0] += scroll_x / 10


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


    # Light shader
    glUseProgram(light_program)

    glUniformMatrix4fv(light_uniform_mapping[b'perspective'], 1, GL_TRUE,
                       perspective_matrix.ctypes.data_as(POINTER(GLfloat)))
    glUniformMatrix4fv(light_uniform_mapping[b'view'], 1, GL_TRUE,
                       create_transformation_matrix(*camera[0], *camera[1], *camera[2]).ctypes.data_as(
                           POINTER(GLfloat)))

    for model_index, entity_list in lights.items():
        vbo, texture_coordinates_vbo, normal_vbo, indexed_vbo, count = models[model_index]

        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexed_vbo)

        for entity in entity_list:
            location, rotation, scale, color, attenuation = entity

            glUniformMatrix4fv(
                light_uniform_mapping[b'transformation'], 1, GL_TRUE,
                create_transformation_matrix(*location, *rotation, *scale).ctypes.data_as(POINTER(GLfloat))
            )
            glUniform3f(light_uniform_mapping[b'color'], *color)

            glDrawElements(GL_TRIANGLES, count, GL_UNSIGNED_INT, 0)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    glDisableVertexAttribArray(0)
    glDisableVertexAttribArray(1)
    glDisableVertexAttribArray(2)

    # Object shader
    glUseProgram(program)

    glUniformMatrix4fv(uniform_mapping[b'perspective'], 1, GL_TRUE, perspective_matrix.ctypes.data_as(
        POINTER(GLfloat)))  # ctypes.data_as must be here and not at initialization.
    glUniformMatrix4fv(uniform_mapping[b'view'], 1, GL_TRUE,
                       create_transformation_matrix(*camera[0], *camera[1], *camera[2]).ctypes.data_as(
                           POINTER(GLfloat)))

    for i, entity in enumerate(get_all_entities(lights)):
        glUniform3f(uniform_mapping[b'light[' + bytes(str(i), 'utf-8') + b'].position'], *entity[0])  # CHANGED
        glUniform3f(uniform_mapping[b'light[' + bytes(str(i), 'utf-8') + b'].color'],    *entity[3])  # CHANGED
        glUniform1f(uniform_mapping[b'light[' + bytes(str(i), 'utf-8') + b'].constant'],  entity[4][0])  # Should always be 1!
        glUniform1f(uniform_mapping[b'light[' + bytes(str(i), 'utf-8') + b'].linear'],    entity[4][1])  # Lower value, more light.
        glUniform1f(uniform_mapping[b'light[' + bytes(str(i), 'utf-8') + b'].quadratic'], entity[4][2])

    glActiveTexture(GL_TEXTURE0)

    for model_index, texture_mapping in entities.items():
        vbo, texture_coordinates_vbo, normal_vbo, indexed_vbo, count = models[model_index]

        # Make bindings for model.
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)

        glBindBuffer(GL_ARRAY_BUFFER, texture_coordinates_vbo)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, 0)

        glBindBuffer(GL_ARRAY_BUFFER, normal_vbo)
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, 0)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexed_vbo)

        for texture_index, entity_list in texture_mapping.items():

            # Make bindings for texture.
            texture = textures[texture_index]
            glBindTexture(GL_TEXTURE_2D, texture.id)

            for entity in entity_list:
                location, rotation, scale = entity

                # Prepare entities of specific model and texture, and draw.
                glUniformMatrix4fv(
                    uniform_mapping[b'transformation'], 1, GL_TRUE,
                    create_transformation_matrix(*location, *rotation, *scale).ctypes.data_as(POINTER(GLfloat))
                )

                glDrawElements(GL_TRIANGLES, count, GL_UNSIGNED_INT, 0)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    glDisableVertexAttribArray(0)
    glDisableVertexAttribArray(1)
    glDisableVertexAttribArray(2)



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
light_shaders = [
    b"""
    #version 120

    uniform mat4 transformation;
    uniform mat4 perspective;
    uniform mat4 view;
    uniform vec3 color;

    attribute vec3 position;

    void main()
    {    
        gl_Position =  perspective * view * transformation * vec4(position, 1.0);
    }

    """,
    b"""
    #version 120

    uniform mat4 transformation;
    uniform mat4 perspective;
    uniform mat4 view;
    uniform vec3 color;

    void main()
    {    
        gl_FragColor = vec4(color, 1.0);
    }

    """
]

temp = []
for i in range(4):
    for attribute in [b'].position', b'].color', b'].intensity', b'].constant', b'].linear', b'].quadratic']:
        temp.append(b'light[' + bytes(str(i), 'utf-8') + attribute)

attributes = [b'position', b'texture_coordinate', b'normal']
uniforms = [
    b'transformation', b'perspective', b'view', *temp
]
program, uniform_mapping = create_shader_program(object_shaders, attributes, uniforms)

light_attributes = [b'position']
light_uniforms = [b'transformation', b'perspective', b'view', b'color']
light_program, light_uniform_mapping = create_shader_program(light_shaders, light_attributes, light_uniforms)

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
        CONTAINER      : [[[randint(-6, 6), randint(-6, 6), randint(-8, -2)], [0, 0, 0], [1, 1, 1]] for i in range(5)],
        ALUMINIUM_PLATE: [[[randint(-6, 6), randint(-6, 6), randint(-8, -2)], [0, 0, 0], [1, 1, 1]] for i in range(5)]
    },
    SPHERE: {
        CONTAINER      : [[[randint(-6, 6), randint(-6, 6), randint(-8, -2)], [0, 0, 0], [1, 1, 1]] for i in range(5)],
        ALUMINIUM_PLATE: [[[randint(-6, 6), randint(-6, 6), randint(-8, -2)], [0, 0, 0], [1, 1, 1]] for i in range(5)]
    },
}

lights = {  # lights have no material but instead has two extra entity attributes: color and atenuation.
    CUBE  : [[[randint(-6, 6), randint(-6, 6), randint(-8, -2)], [0, 0, 0], [1, 1, 1], [0.5, 1.0, 1.0], [1.0, 0.009, 0.032]] for i in range(2)],
    SPHERE: [[[randint(-6, 6), randint(-6, 6), randint(-8, -2)], [0, 0, 0], [1, 1, 1], [0.5, 1.0, 1.0], [1.0, 0.009, 0.032]] for i in range(2)]
}

perspective_matrix = create_perspective_matrix(60, window.width / window.height, 0.1, 100)
camera = [[0, 0, -10], [0, 0, 0], [1, 1, 1]]

pyglet.app.run()
