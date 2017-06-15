from pyglet.gl import (
    GLboolean, GLuint, GLint, GLfloat, GLdouble, GLsizei, GLenum, GLchar, GLException,

    glCreateShader, glShaderSource, glCompileShader, glGetShaderiv, glCreateProgram, glAttachShader,
    glBindAttribLocation, glLinkProgram, glValidateProgram, glGetUniformLocation, glGetAttribLocation, glGetProgramiv,
    glGetShaderInfoLog, glGetProgramInfoLog, glUseProgram, glGetActiveUniform, glGetActiveAttrib, glGetError,

    glUniform1f, glUniform2f, glUniform3f, glUniform4f, glUniform1i, glUniform2i, glUniform3i, glUniform4i,
    glUniform1ui, glUniform2ui, glUniform3ui, glUniform4ui,
    glUniform1fv, glUniform2fv, glUniform3fv, glUniform4fv, glUniform1iv, glUniform2iv, glUniform3iv, glUniform4iv,
    glUniform1uiv, glUniform2uiv, glUniform3uiv, glUniform4uiv,

    glUniformMatrix2fv, glUniformMatrix2x3fv, glUniformMatrix2x4fv,
    glUniformMatrix3x2fv, glUniformMatrix3fv, glUniformMatrix3x4fv,
    glUniformMatrix4x2fv, glUniformMatrix4x3fv, glUniformMatrix4fv,

    GL_FALSE, GL_TRUE, GL_COMPILE_STATUS, GL_LINK_STATUS, GL_VALIDATE_STATUS, GL_ATTACHED_SHADERS, GL_ACTIVE_ATTRIBUTES,
    GL_ACTIVE_UNIFORMS, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, GL_INFO_LOG_LENGTH, GL_NO_ERROR,
)
from c_bindings import c_string, c_string_array, c_array, byref, create_string_buffer, pointer, cast, POINTER
from temporary import table, temp
import sys
import numpy

"""
There are 5 data types that can be uploaded to the shader in 5 different structures:

    Data types are float, double, int, uint and bool.
    Data structures are scalar, vector, matrix, array, struct, and others which are uploaded just with scalars.

    * Scalars can be all 5 data types.
    * Vectors can be all 5 data types and size 2, 3, 4.
    * Matrices can only be float (in GLSL 2.1) and have rows/cols of size 2, 3, 4.

    * Arrays can contain all data types and data structures of any size, but only one per array.
    * Structs can contain all data types and data structures of any size, there's no limit per struct.

    Scalars, vectors, array of scalars or array of vectors can be uploaded with glUniform{1, 2, 3, 4}{f, d, i, ui, b}v.

    Matrices needs to be uploaded using glUniformMatrix{n, nxm}. Arrays of matrices can be iterated over.

    Every field in a struct must be uploaded separately. That means we have to identify the fields and send them to the
    right function. Arrays of structs should be able to be iterated over.



"""

# from pyglet.gl.lib import link_GL, link_WGL # WGLFunctionProxy
# except for bools which use i and opaques which use 1i

CHECK_ERROR = True
CHECK_WARNING = True
CRASH_ON_ERROR = True
CRASH_ON_WARNING = False

GLSL_SCALARS = {
    'bool', 'int', 'uint', 'float', 'double'
}
GLSL_VECTORS = {
    'bvec2', 'ivec2', 'uvec2', 'vec2', 'dvec2',
    'bvec3', 'ivec3', 'uvec3', 'vec3', 'dvec3',
    'bvec4', 'ivec4', 'uvec4', 'vec4', 'dvec4'
}
GLSL_MATRICES = {
    'mat2x2', 'mat2x3', 'mat2x4',
    'mat3x2', 'mat3x3', 'mat3x4',
    'mat4x2', 'mat4x3', 'mat4x4',
    'mat2', 'mat3', 'mat4'
}
GLSL_SAMPLERS = {
    'sampler1D', 'isampler1D', 'usampler1D',
    'sampler2D', 'isampler2D', 'usampler2D',
    'sampler3D', 'isampler3D', 'usampler3D',

    'samplerCube', 'isamplerCube', 'usamplerCube',
    'sampler2DRect', 'isampler2DRect', 'usampler2DRect',
    'sampler1DArray', 'isampler1DArray', 'usampler1DArray',
    'sampler2DArray', 'isampler2DArray', 'usampler2DArray',
    'samplerCubeArray', 'isamplerCubeArray', 'usamplerCubeArray',
    'samplerBuffer', 'isamplerBuffer', 'usamplerBuffer',
    'sampler2DMS', 'isampler2DMS', 'usampler2DMS',
    'sampler2DMSArray', 'isampler2DMSArray', 'usampler2DMSArray'
}
GLSL_IMAGES = {
    'image1D', 'iimage1D', 'uimage1D',
    'image2D', 'iimage2D', 'uimage2D',
    'image3D', 'iimage3D', 'uimage3D',

    'imageCube', 'iimageCube', 'uimageCube',
    'image2DRect', 'iimage2DRect', 'uimage2DRect',
    'image1DArray', 'iimage1DArray', 'uimage1DArray',
    'image2DArray', 'iimage2DArray', 'uimage2DArray',
    'imageCubeArray', 'iimageCubeArray', 'uimageCubeArray',
    'imageBuffer', 'iimageBuffer', 'uimageBuffer',
    'image2DMS', 'iimage2DMS', 'uimage2DMS',
    'image2DMSArray', 'iimage2DMSArray', 'uimage2DMSArray'
}
GLSL_DATA_TYPES = {  # Missing atomic uniforms.
    *GLSL_SCALARS,
    *GLSL_VECTORS,
    *GLSL_MATRICES,

    # The following uniforms all have three prefixes: None == float, i == integer and u == unsigned integer,
    *GLSL_SAMPLERS,
    *GLSL_IMAGES
}


# -------------------------------------- Shader -------------------------------------------------

class Shader(GLuint):
    """
    Shader is a static object. Once created it cannot be changed. Instead you need to delete it and create a new.
    """

    def __init__(self, shader_type, source=None, path=None):
        """
        Creates a shader object from either a source string or a text file at path.

        Args:
            shader_type: GL_VERTEX_SHADER or GL_FRAGMENT_SHADER.
            source: String of the code to use for the shader.
            path: Path to a text file containing the code for the shader.
        """
        if path:
            source = open(path).read()

        handle = -1
        try:
            handle = glCreateShader(shader_type)
            glShaderSource(handle, 1, c_string_array(source, count=1), None)
            glCompileShader(handle)
        except GLException:
            debug_shader(handle)

        super(Shader, self).__init__(handle)
        self.shader_type = shader_type
        self.source = source
        self.path = path

        if CHECK_ERROR:
            debug_shader(self)

    def __repr__(self):
        return 'Shader(ID=%s, path=%s)' % (self.value, self.path)


class VertexShader(Shader):
    def __init__(self, source=None, path=None):
        super(VertexShader, self).__init__(shader_type=GL_VERTEX_SHADER, source=source, path=path)


class FragmentShader(Shader):
    def __init__(self, source=None, path=None):
        super(FragmentShader, self).__init__(shader_type=GL_FRAGMENT_SHADER, source=source, path=path)


def shader_status(shader: GLuint, status_type: int) -> GLint:
    """
    Returns the status of the 'shader' for any given 'status_type'.

    Errors:
        GL_INVALID_VALUE:      if shader is not a value generated by OpenGL.
        GL_INVALID_OPERATION:  if shader does not refer to a shader object.
        GL_INVALID_ENUM:       if status_type is not an accepted value.

    Args:
        shader:       The handle to the shader.
        status_type:  GL_SHADER_TYPE, GL_DELETE_STATUS, GL_COMPILE_STATUS, GL_INFO_LOG_LENGTH, GL_SHADER_SOURCE_LENGTH.

    Returns:

    """
    status = GLint()
    glGetShaderiv(shader, status_type, byref(status))
    return status.value


def debug_shader(shader: Shader):
    """

    Args:
        shader: Handle to the shader.

    Returns:

    """
    error = False

    def print_error(message):
        nonlocal error
        error = True

        status = GLint()
        glGetShaderiv(shader, GL_INFO_LOG_LENGTH, byref(status))

        output = create_string_buffer(status.value)
        glGetShaderInfoLog(shader, status, None, output)

        shader_source = '\n'.join(
            ['{:<3} | '.format(row) + line for row, line in enumerate(shader.source.splitlines(), start=1)]
        )

        print(message, output.value.decode('utf-8'), 'Shader source:', shader_source, file=sys.stderr, sep='\n')

    if shader == -1:
        print_error('Could not create shader!')
    if shader_status(shader, GL_COMPILE_STATUS) == GL_FALSE:
        print_error('Could not compile %s!' % shader)

    if error and CRASH_ON_ERROR:
        sys.exit(-1)


# -------------------------------------- PROGRAM -------------------------------------------------


class Program(GLuint):

    def __init__(self, vertex_shader: Shader, fragment_shader: Shader, attributes=(), uniforms=()):
        """
        The process of creating a shader can be divided into 6 steps:

            1. Create an ID.
            2. Attach shaders.
            3. Bind attributes.
            4. Link program.
            5. Validate program.
            6. Bind uniforms.

        Args:
            vertex_shader: 
            fragment_shader: 
            attributes: 
            uniforms: 
        """

        handle = -1
        attribute_location = {}
        uniform_location = {}

        try:
            handle = glCreateProgram()
            glAttachShader(handle, vertex_shader)
            glAttachShader(handle, fragment_shader)
            for index, name in enumerate(attributes):
                glBindAttribLocation(handle, index, c_string(name))
                attribute_location[name] = index
            glLinkProgram(handle)
            glValidateProgram(handle)
            for uniform in uniforms:
                uniform_location[uniform] = glGetUniformLocation(handle, c_string(uniform))
        except GLException:
            debug_program(handle)

        super(Program, self).__init__(handle)
        self.vertex_shader = vertex_shader
        self.fragment_shader = fragment_shader
        self.attribute_location = attribute_location
        self.uniform_location = uniform_location

        if CHECK_ERROR:
            debug_program(self)
            # scan(self)

    def __repr__(self):
        return 'Shader program (ID=%s)' % self.value

    def __enter__(self):
        glUseProgram(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        glUseProgram(0)

    def load_uniform_matrix(self, matrix, *, name=None):
        """

        Args:
            matrix: A numpy array. 
            name: 

        Returns:

        """
        row, col = matrix.shape
        func = ((glUniformMatrix2fv, glUniformMatrix2x3fv, glUniformMatrix2x4fv),
                (glUniformMatrix3x2fv, glUniformMatrix3fv, glUniformMatrix3x4fv),
                (glUniformMatrix4x2fv, glUniformMatrix4x3fv, glUniformMatrix4fv))[row - 2][col - 2]

        if CHECK_ERROR:
            if name is None:
                raise ValueError('Uniform name must be specified as keyword!')
            elif row not in (2, 3, 4) or col not in (2, 3, 4):
                raise TypeError('Matrix can not be of shape {}x{}!'.format(row, col))

        location = self.uniform_location[name]
        data = matrix.ctypes.data_as(POINTER(GLfloat))
        func(location, 1, GL_TRUE, data)


    def load_uniform_floats(self, *values, name=None):
        """
        Uploads float values to a scalar or vector in the shader program.

        Args:
            *values: 
            name: 

        Returns:

        """
        # TODO Maybe just use load_uniform_array since it can do the same and more?
        count = len(values) - 1
        func = (glUniform1f, glUniform2f, glUniform3f, glUniform4f)[count]

        if CHECK_ERROR:
            if name is None:
                raise ValueError('Uniform name must be specified as keyword!')
            elif len(values) > 4:
                raise ValueError('Can only load up to 4 floats, not %i!' % len(values))

        location = self.uniform_location[name]
        func(location, *values)

        # The following does not work since a vec3 needs glUniform3fv(loc, 1, data) and float glUniform1fv(loc, 1, data)
        # array = c_array(values, GLfloat)
        # data = cast(pointer(array), POINTER(GLfloat))
        # glUniform1fv(location, count, data)

    def load_uniform_uints(self, *values, name=None):
        """
        Uploads float values to a scalar or vector in the shader program.

        Args:
            *values: 
            name: 

        Returns:

        """
        # TODO Maybe just use load_uniform_array since it can do the same and more?
        count = len(values) - 1
        func = (glUniform1ui, glUniform2ui, glUniform3ui, glUniform4ui)[count]

        if CHECK_ERROR:
            if name is None:
                raise ValueError('Uniform name must be specified as keyword!')
            elif len(values) > 4:
                raise ValueError('Can only load up to 4 unsigned ints, not %i!' % len(values))

        location = self.uniform_location[name]
        func(location, *values)

    def load_uniform_ints(self, *values, name=None):
        """
        Uploads float values to a scalar or vector in the shader program.

        Args:
            *values: 
            name: 

        Returns:

        """
        # TODO Maybe just use load_uniform_array since it can do the same and more?
        count = len(values) - 1
        func = (glUniform1i, glUniform2i, glUniform3i, glUniform4i)[count]

        if CHECK_ERROR:
            if name is None:
                raise ValueError('Uniform name must be specified as keyword!')
            elif len(values) > 4:
                raise ValueError('Can only load up to 4 unsigned ints, not %i!' % len(values))

        location = self.uniform_location[name]
        func(location, *values)


    def load_uniform_struct(self, struct, name=None):
        """
        Upload a struct to the shader. 

        Args:
            struct: 
            name: 

        Returns:

        """
        for attribute_name in struct.__slots__:
            attribute = getattr(struct, attribute_name)
            full_name = name + '.' + attribute_name

            try:
                rows, *cols = attribute.shape  # Could be problem if matrix is of shape (rows, 1), but that shouldn't be.
            except ValueError:
                if attribute.dtype == GLfloat:
                    self.load_uniform_floats(attribute, name=full_name)
                elif attribute.dtype == GLuint:
                    self.load_uniform_uints(attribute, name=full_name)
                elif attribute.dtype == GLint:
                    self.load_uniform_ints(attribute, name=full_name)
                else:
                    raise TypeError('Not implemented yet. Only have for floats and uints.')
            else:
                if cols:  # Is multi-dimensional.
                    self.load_uniform_matrix(attribute, name=full_name)
                elif rows > 4:  # Is 1-dimensional but longer than 4.
                    self.load_uniform_array(attribute, name=full_name)
                elif attribute.dtype == GLfloat:  # Is 1-dimensional, less than 4 and float.
                    self.load_uniform_floats(*attribute, name=full_name)
                else:  # Is 1-dimensional, less than 4 and int/uint.
                    location = self.uniform_location[name]
                    glUniform1i(location, attribute)  # Samplers should be set with integers.

    def load_uniform_array(self, array: numpy.ndarray, name=None):
        """
        Upload an array to the shader.

        Args:
            array: A numpy array.
            name:  The name of the array.

        Returns:

        """

        # glUniform1fv(location_to_first_index, size, data)

        row, col = array.shape
        if array.dtype == GLfloat:
            func = (glUniform1fv, glUniform2fv, glUniform3fv, glUniform4fv)[col - 1]
        elif array.dtype == GLint:
            func = (glUniform1iv, glUniform2iv, glUniform3iv, glUniform4iv)[col - 1]
        elif array.dtype == GLuint:
            func = (glUniform1uiv, glUniform2uiv, glUniform3uiv, glUniform4uiv)[col - 1]
        else:
            raise TypeError('Other data types are not implemented yet.')

        location = self.uniform_location[name]
        data = array.ctypes.data_as(POINTER(GLfloat))
        func(location, len(data), data)


def get_uniform_data(program):
    """
    Args:
        program: 

    Returns:

    """
    uniforms = {}

    count = pointer(GLint())
    buffer_size = GLsizei(32)
    length = GLsizei()
    size = GLint()
    data_type = GLenum()
    uniform_name = c_string('', size=buffer_size.value)

    glGetProgramiv(program, GL_ACTIVE_UNIFORMS, count)

    for i in range(count.contents.value):
        glGetActiveUniform(program, GLuint(i), buffer_size, length, size, data_type, uniform_name)
        uniform_name_ = uniform_name.value.decode('utf-8')
        data_type_string = temp[data_type.value]
        uniforms[uniform_name_] = {
            'dtype'   : table[data_type_string]['dtype'], 'index': i, 'size': size.value, 'value': None,
            'location': glGetUniformLocation(program, uniform_name), 'function': table[data_type_string]['function'],
        }
        print(uniform_name_, uniforms[uniform_name_])
    return uniforms


def program_status(program: GLuint, status_type: int) -> int:
    """

    Args:
        program:      The handle to the program.
        status_type:  GL_DELETE_STATUS, GL_LINK_STATUS, GL_VALIDATE_STATUS, GL_INFO_LOG_LENGTH, GL_ATTACHED_SHADERS, 
                      GL_ACTIVE_ATOMIC_COUNTER_BUFFERS, GL_ACTIVE_ATTRIBUTES, GL_ACTIVE_ATTRIBUTE_MAX_LENGTH, 
                      GL_ACTIVE_UNIFORMS, GL_ACTIVE_UNIFORM_BLOCKS, GL_ACTIVE_UNIFORM_BLOCK_MAX_NAME_LENGTH, 
                      GL_ACTIVE_UNIFORM_MAX_LENGTH, GL_COMPUTE_WORK_GROUP_SIZE GL_PROGRAM_BINARY_LENGTH, 
                      GL_TRANSFORM_FEEDBACK_BUFFER_MODE, GL_TRANSFORM_FEEDBACK_VARYINGS, 
                      GL_TRANSFORM_FEEDBACK_VARYING_MAX_LENGTH, GL_GEOMETRY_VERTICES_OUT, GL_GEOMETRY_INPUT_TYPE, 
                      GL_GEOMETRY_OUTPUT_TYPE.

    Returns:
        Status code.
    """
    status = GLint()
    glGetProgramiv(program, status_type, byref(status))
    return status.value


def debug_program(program: Program):
    """

    Args:
        program: The handle to the program.

    Returns:

    """
    error = False

    def print_error(message):
        nonlocal error
        error = True

        status = GLint()
        glGetProgramiv(program, GL_INFO_LOG_LENGTH, byref(status))  # Getting the number of char in info log to 'status'

        output = create_string_buffer(status.value)  # status.value)
        glGetProgramInfoLog(program, status, None, output)

        print(message, output.value.decode('utf-8'), file=sys.stderr)

    if program == -1:
        print_error('Could not create program!')
    if program_status(program, GL_LINK_STATUS) == GL_FALSE:
        print_error('Could not link program!')
    if program_status(program, GL_VALIDATE_STATUS) == GL_FALSE:
        print_error('Validation failed!')
    if program_status(program, GL_ATTACHED_SHADERS) != 2:
        print_error('Wrong amount of shaders attached!')

    # # TODO These are more warnings than errors.
    # if program_status(program, GL_ACTIVE_ATTRIBUTES) != len(program.attribute_location):
    #     # TODO There are non user defined attributes and uniforms. Also fails for structs!
    #     print_error('Unused attributes attributes in shader program!')
    # if program_status(program, GL_ACTIVE_UNIFORMS) != len(program.uniform_location):
    #     print_error('Unused uniforms attributes in shader program!')

    if error and CRASH_ON_ERROR:
        sys.exit(-1)


def scan(program: Program):
    """
    We scan through the vertex shader and the fragment shader to see if the attributes and uniforms uploaded to the 
    program match those in the shaders.

    All attributes starts with the keyword `attribute` at the lowest indention level. Some attributes are not loaded to
    the program, which are the ones that start with the `gl_` prefix.

    Uniforms starts with the keyword `uniform` at the lowest indention level. Uniforms are more flexible than attributes
    since they can be basic data types, structs, array or array of structs. There are also predefined uniforms 
    `sampler1D`, `sampler2D` och `sampler3D`.


    Built-in data types are:
        bool, int, uint, float, double
        bvec, ivec, uvec, vec, dvec
        mat
        sampler

    Args:
        program: 

    Returns:
        None
    """
    # TODO Tidy up function.
    # TODO Maybe separate into warnings and errors?

    struct_members = {}
    attributes = set()
    uniforms = set()

    source = program.vertex_shader.source.split()
    index = 0
    while index < len(source):
        if source[index] == 'struct':
            index += 1
            struct_name = source[index].replace('{', '')
            struct_members[struct_name] = []
            while not '};' in source[index]:
                if source[index] in GLSL_DATA_TYPES:
                    index += 1
                    if '[' in source[index]:
                        temp = []
                        for character in source[index]:
                            if character == '[':
                                break
                            else:
                                temp.append(character)
                        member = ''.join(temp)
                    else:
                        member = source[index].replace(';', '')
                    struct_members[struct_name].append(member)
                index += 1
        elif source[index] == 'attribute':
            index += 2
            attributes.add(source[index].replace(';', ''))
        elif source[index] == 'uniform':
            index += 1
            if source[index] in struct_members:
                struct = source[index]
                index += 1
                if '[' in source[index]:
                    temp = []
                    for character in source[index]:
                        if character == '[':
                            break
                        else:
                            temp.append(character)
                    name = ''.join(temp)
                else:
                    name = source[index].replace(';', '')
                for member in struct_members[struct]:
                    uniforms.add(name + '.' + member)
        index += 1

    source = program.fragment_shader.source.split()
    index = 0
    while index < len(source):
        if source[index] == 'struct':
            index += 1
            struct_name = source[index].replace('{', '')
            struct_members[struct_name] = []
            while not '};' in source[index]:
                if source[index] in GLSL_DATA_TYPES:
                    index += 1
                    if '[' in source[index]:
                        temp = []
                        for character in source[index]:
                            if character == '[':
                                break
                            else:
                                temp.append(character)
                        member = ''.join(temp)
                    else:
                        member = source[index].replace(';', '')
                    struct_members[struct_name].append(member)
                index += 1
        elif source[index] == 'uniform':
            index += 1
            if source[index] in struct_members:
                struct = source[index]
                index += 1
                if '[' in source[index]:
                    temp = []
                    for character in source[index]:
                        if character == '[':
                            break
                        else:
                            temp.append(character)
                    name = ''.join(temp)
                else:
                    name = source[index].replace(';', '')
                for member in struct_members[struct]:
                    uniforms.add(name + '.' + member)
        index += 1

    template = """
{name} uploaded to the program do not match those used the shaders.

    {name} in the program: {program_attributes}
    {name} in the shaders: {attributes}
"""

    error = False

    if set(attributes) != set(program.attribute_data):
        print(
            template.format(
                name='Attributes',
                program_attributes=', '.join(sorted(program.attribute_data.keys())),
                attributes=', '.join(sorted(attributes))
            ),
            file=sys.stderr
        )
        error = True
    if set(uniforms) != set(program.uniform_data):
        print(
            template.format(
                name='Uniforms',
                program_attributes=', '.join(sorted(program.uniform_data)),
                attributes=', '.join(sorted(uniforms))
            ),
            file=sys.stderr
        )
        error = True

    if error and CRASH_ON_ERROR:
        sys.exit(-1)


def struct(name, fields, print_class=False):
    """
    Creates a struct class which can be sent in the shader program.

    Examples:
        >>> PointLight = struct('PointLight', fields=['vec3 position', 'vec3 ambient', 'vec3 diffuse', 'vec3 specular'])
        >>> light = PointLight()
        >>> light
        Sosf
        >>> light.position = 0, -50, 0
        >>> light.position
        array([  0., -50.,   0.], dtype=float32)


    Args:
        name: 
        fields: 
        print_class: Prints the class definition. Could be useful if you want to copy and modify it yourself and/or not
                     create the class at runtime.

    Returns:

    """
    # TODO Make these two global?
    data_type_mapping = {'bool'  : 'GLboolean', 'int': 'GLint', 'uint': 'GLuint', 'float': 'GLfloat',
                         'double': 'GLdouble'}
    prefix_mapping = {'b': 'GLboolean', 'i': 'GLint', 'u': 'GLuint', '': 'GLfloat', 'd': 'GLdouble'}

    field_types = []
    field_names = []
    for field in fields:
        field_type, field_name = field.split()

        array_length = ''
        if '[' in field_name:
            field_name, length = field_name.split('[')
            array_length = length[:-1]

        if field_type in GLSL_SCALARS:
            shape = '1' if not array_length else array_length
            dtype = data_type_mapping.get(field_type)
        elif field_type in GLSL_VECTORS:
            shape = field_type[-1] if not array_length else array_length + ', ' + field_type[-1]
            dtype = prefix_mapping.get(field_type[0], 'GLfloat')  # Since absence of prefix means float.
        elif field_type in GLSL_MATRICES:
            if 'x' in field_type:
                shape = field_type[-3] + ', ' + field_type[-1]
            else:
                shape = field_type[-1] + ', ' + field_type[-1]
            dtype = prefix_mapping.get(field_type[0], 'GLfloat')  # Since absence of prefix means float.
        elif field_type in GLSL_SAMPLERS:
            shape = '1' if not array_length else array_length
            dtype = 'GLuint'
        else:
            raise NotImplemented(field_type + ' is not yet supported!')

        temp = 'numpy.empty(shape=({}), dtype={}, order="C")'.format(shape, dtype)
        field_types.append(temp)
        field_names.append(field_name)

    # TODO Make theses lines in a function in a different module?
    slots = ', '.join(['"_{}"'.format(field_name) for field_name in field_names])
    attributes = '\n        '.join(
        ('self._' + field_name + ' = ' + field_type) for field_name, field_type in zip(field_names, field_types))

    # TODO Refactor the templates elsewhere=?
    properties = ''.join("""
    @property
    def {name}(self):
        return self._{name}

    @{name}.setter
    def {name}(self, value):
        self._{name}[:] = value 
""".format(name=name) for name in field_names)
    class_template = """
class {name}:
    __slots__ = ({slots})

    def __init__(self):
        {attributes}

    def __repr__(self):
        attributes = '\\n'.join('    %s = %s' % (field, getattr(self, name)) for field, name in zip({fields}, self.__slots__))
        return '{name}:\\n' + attributes
    {properties}
""".format(name=name, slots=slots, attributes=attributes, properties=properties, fields=fields)

    if print_class:
        print(class_template)

    namespace = {
        'numpy' : numpy, 'GLboolean': GLboolean, 'GLint': GLint,
        'GLuint': GLuint, 'GLfloat': GLfloat, 'GLdouble': GLdouble
    }
    exec(class_template, namespace)
    return namespace[name]
