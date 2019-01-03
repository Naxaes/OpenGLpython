from pyglet.gl import (
    glUseProgram,

    glUniform4ui, glUniform4ui, glUniform4ui, glUniform4ui,
    glUniform1i,  glUniform2i,  glUniform3i,  glUniform4i,
    glUniform1d,  glUniform2d,  glUniform3d,  glUniform4d,
    glUniform1f,  glUniform2f,  glUniform3f,  glUniform4f,

    glUniformMatrix4fv,

    GL_TRUE,

    GLException,

    glCreateShader, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, glShaderSource, glCompileShader, glCreateProgram,
    glAttachShader, glBindAttribLocation, glLinkProgram, glValidateProgram, glGetShaderiv, GL_INFO_LOG_LENGTH,
    glGetShaderInfoLog, glGetProgramInfoLog, glGetUniformLocation, glGetProgramiv, GLint, GLfloat,
)
from source.c_bindings import *


class Shader:

    bound = None  # This is okay if we assume we're only going to need one OpenGL context.

    @classmethod
    def create(cls, vertex_source, fragment_source, attributes, uniforms):
        number_of_string = 1

        # Create vertex shader.
        vertex_handle = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_handle, number_of_string, c_pointer_to_char_pointers(vertex_source), None)
        glCompileShader(vertex_handle)

        # Create fragment shader.
        fragment_handle = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_handle, number_of_string, c_pointer_to_char_pointers(fragment_source), None)
        glCompileShader(fragment_handle)


        # Create attributes.
        attribute_mapping = []
        for attribute in attributes:
            attribute_mapping.append(c_string(attribute))


        try:
            # Create program.
            program_handle = glCreateProgram()

            glAttachShader(program_handle, vertex_handle)
            glAttachShader(program_handle, fragment_handle)

            for index, name in enumerate(attribute_mapping):
                glBindAttribLocation(program_handle, index, name)

            glLinkProgram(program_handle)
            glValidateProgram(program_handle)
            glUseProgram(program_handle)

        except GLException as error:
            # Print vertex shader errors.
            status = GLint()
            glGetShaderiv(vertex_handle, GL_INFO_LOG_LENGTH, byref(status))
            output = create_string_buffer(status.value)
            glGetShaderInfoLog(vertex_handle, status, None, output)
            print(output.value.decode('utf-8'))

            # Print fragment shader errors.
            status = GLint()
            glGetShaderiv(fragment_handle, GL_INFO_LOG_LENGTH, byref(status))
            output = create_string_buffer(status.value)
            glGetShaderInfoLog(fragment_handle, status, None, output)
            print(output.value.decode('utf-8'))

            # Print program errors.
            status = GLint()
            glGetProgramiv(program_handle, GL_INFO_LOG_LENGTH, byref(status))  # Getting the number of char in info log to 'status'
            output = create_string_buffer(status.value)  # status.value)
            glGetProgramInfoLog(program_handle, status, None, output)
            print(output.value.decode('utf-8'))

            raise error

        # Get uniform location.
        uniform_mapping = {}
        for uniform in uniforms:
            name = c_string(uniform)
            location = glGetUniformLocation(program_handle, cast(pointer(name), POINTER(c_char)))
            uniform_mapping[uniform] = location

        return cls(program_handle, uniform_mapping)

    def __init__(self, id_, uniform_mapping):
        self.id = id_
        self.uniform = uniform_mapping

    def enable(self):
        glUseProgram(self.id)
        Shader.bound = self  # Just for safety.

    @staticmethod
    def disable():
        glUseProgram(0)
        Shader.bound = None

    def is_bound(self):
        return Shader.bound is self

    def _assert_bound(self):
        assert self.is_bound(), "Must bind this shader ({}) before being able to load uniform.".format(self.id)

    def load(self):
        pass

    def load_uniform_matrix(self, **uniforms):
        self._assert_bound()

        for name, data in uniforms.items():
            glUniformMatrix4fv(self.uniform[name], 1, GL_TRUE, data.ctypes.data_as(POINTER(GLfloat)))

    def load_uniform_floats(self, **uniforms):
        self._assert_bound()

        for name, data in uniforms.items():
            if isinstance(data, (float, int)):
                glUniform1f(self.uniform[name], data)
            else:
                functions = glUniform2f, glUniform3f, glUniform4f
                functions[len(data) - 2](self.uniform[name], *data)

    def load_uniform_sampler(self, **uniforms):
        self._assert_bound()

        for name, data in uniforms.items():
            glUniform1i(self.uniform[name], data)
