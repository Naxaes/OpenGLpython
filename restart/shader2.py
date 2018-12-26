from pyglet.gl import (
    glCreateShader, glShaderSource, glCompileShader, glCreateProgram, glAttachShader, glBindAttribLocation,
    glLinkProgram, glValidateProgram, glUseProgram, glGetShaderiv, glGetShaderInfoLog, glGetProgramiv,
    glGetProgramInfoLog, glGetUniformLocation, glUniformMatrix4fv, glBindBuffer, glEnableVertexAttribArray,
    glVertexAttribPointer, glUniform3f, glDrawElements, glDisableVertexAttribArray, glBindTexture, glActiveTexture,
    glUniform1f, glDisable, glColorMask, glStencilMask, glEnable, glStencilFunc, glUniformMatrix3fv, glGetActiveUniform,

    GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, GL_INFO_LOG_LENGTH, GL_TRUE, GL_ARRAY_BUFFER, GL_FLOAT,
    GL_FALSE, GL_ELEMENT_ARRAY_BUFFER, GL_TRIANGLES, GL_UNSIGNED_INT, GL_TEXTURE_2D, GL_TEXTURE0,
    GL_DEPTH_TEST, GL_NOTEQUAL, GL_ACTIVE_UNIFORMS,

    GLuint, GLint, GLchar, GLException, GLfloat, GLsizei, GLenum
)
from ctypes import cast, byref, pointer, POINTER, create_string_buffer, addressof, c_char_p

from restart.mathematics import create_transformation_matrix, create_2D_transformation_matrix
from restart.temp import uniform_function


class Uniform(GLuint):

    def __init__(self, name, location, data_type):
        super().__init__(location)

        self.name = name

        if hasattr(uniform_function[data_type], '__iter__'):
            self.function, *self.arguments = uniform_function[data_type]
        else:
            self.function = uniform_function[data_type]
            self.arguments = ()

    def load(self, *args):
        self.function(self.value, *self.arguments, *args)


class ShaderProgram(GLuint):
    def __init__(self, shaders, attributes, uniforms):
        vertex_shader = shaders[0]
        fragment_shader = shaders[1]

        vertex_handle = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_handle, 1,
                       cast(pointer(pointer(create_string_buffer(vertex_shader))), POINTER(POINTER(GLchar))), None)
        glCompileShader(vertex_handle)

        fragment_handle = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_handle, 1,
                       cast(pointer(pointer(create_string_buffer(fragment_shader))), POINTER(POINTER(GLchar))), None)
        glCompileShader(fragment_handle)

        # Create attributes.
        attribute_mapping = []
        for attribute in attributes:
            attribute_mapping.append(create_string_buffer(attribute))

        try:
            # Create program.
            program_handle = glCreateProgram()

            glAttachShader(program_handle, vertex_handle)
            glAttachShader(program_handle, fragment_handle)

            for index, name in enumerate(attributes):  # CHANGED
                glBindAttribLocation(program_handle, index, name)

            glLinkProgram(program_handle)
            glValidateProgram(program_handle)
            glUseProgram(program_handle)

        except GLException:
            # Print errors.
            status = GLint()
            glGetShaderiv(vertex_handle, GL_INFO_LOG_LENGTH, byref(status))
            output = create_string_buffer(status.value)
            glGetShaderInfoLog(vertex_handle, status, None, output)
            print(output.value.decode('utf-8'))

            status = GLint()
            glGetShaderiv(fragment_handle, GL_INFO_LOG_LENGTH, byref(status))
            output = create_string_buffer(status.value)
            glGetShaderInfoLog(fragment_handle, status, None, output)
            print(output.value.decode('utf-8'))

            status = GLint()
            glGetProgramiv(program_handle, GL_INFO_LOG_LENGTH,
                           byref(status))  # Getting the number of char in info log to 'status'
            output = create_string_buffer(status.value)  # status.value)
            glGetProgramInfoLog(program_handle, status, None, output)
            print(output.value.decode('utf-8'))

        # # Get uniform location.
        # uniform_mapping = {}
        # for uniform in uniforms:
        #     name = create_string_buffer(uniform)
        #     location = glGetUniformLocation(program_handle, cast(pointer(name), POINTER(GLchar)))
        #     uniform_mapping[uniform] = location


        active_shaders = GLint()
        glGetProgramiv(program_handle, GL_ACTIVE_UNIFORMS, active_shaders)

        buffer_size = GLsizei(255)
        data_type = GLenum(0)

        string_buffer = create_string_buffer(buffer_size.value)
        name = c_char_p(addressof(string_buffer))

        uniform_mapping = {}
        for index in range(active_shaders.value):
            glGetActiveUniform(program_handle, index, buffer_size, None, None, byref(data_type), name)
            if name.value in uniforms:
                location = glGetUniformLocation(program_handle, cast(pointer(name), POINTER(GLchar)))
                uniform = Uniform(name.value, location, data_type.value)
                uniform_mapping[name.value] = uniform

        super().__init__(program_handle)
        self.uniforms = uniform_mapping
        self.attributes = attribute_mapping

    def draw(self, uniforms, entities, models, textures=(), *args, **kwargs):
        """
        Attribute entities relies on a data structure:
            entities = {
                MODEL1 : {
                    TEXTURE0 : entity_list
                    TEXTURE1 : entity_list
                },
                MODEL2 : {
                    TEXTURE0 : entity_list
                    TEXTURE1 : entity_list
                },
            }
        where each key is the index to the corresponding model and texture.

        Args:
            uniforms:
            entities:
            models:
            textures:

        Returns:

        """
        raise NotImplemented('Draw method is not implemented!')


class LightShader(ShaderProgram):
    def __init__(self):
        super().__init__(
            shaders=[open('shaders/light_shader.vs', 'rb').read(), open('shaders/light_shader.fs', 'rb').read()],
            attributes=[b'position'],
            uniforms=[b'transformation', b'perspective', b'view', b'color']
        )

    def draw(self, uniforms, entities, models, *args, **kwargs):
        glUseProgram(self)

        self.uniforms[b'perspective'].load(uniforms.get(b'perspective').ctypes.data_as(POINTER(GLfloat)))
        self.uniforms[b'view'].load(uniforms.get(b'view').ctypes.data_as(POINTER(GLfloat)))

        for model_index, entity_list in entities.items():
            model = models[model_index]

            model.enable()

            for entity in entity_list:
                entity.get_transformation_matrix(self.uniforms[b'transformation'])
                self.uniforms[b'color'].load(*entity.color)

                model.draw()

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

        glDisableVertexAttribArray(0)


class ObjectShader(ShaderProgram):
    def __init__(self):
        temp = []
        for i in range(4):
            for attribute in [b'].position', b'].color', b'].intensity', b'].constant', b'].linear', b'].quadratic']:
                temp.append(b'light[' + bytes(str(i), 'utf-8') + attribute)
        super().__init__(
            shaders=[open('shaders/object_shader.vs', 'rb').read(), open('shaders/object_shader.fs', 'rb').read()],
            attributes=[b'position', b'texture_coordinate', b'normal'],
            uniforms=[b'transformation', b'perspective', b'view', *temp]
        )

    def draw(self, uniforms, entities, models, textures=(), lights=(), *args, **kwargs):
        glUseProgram(self)

        # PREPARE SHADER
        self.uniforms[b'perspective'].load(uniforms.get(b'perspective').ctypes.data_as(POINTER(GLfloat)))
        self.uniforms[b'view'].load(uniforms.get(b'view').ctypes.data_as(POINTER(GLfloat)))

        for i, entity in enumerate(lights):
            self.uniforms[b'light[' + bytes(str(i), 'utf-8') + b'].position'].load(*entity._location)
            self.uniforms[b'light[' + bytes(str(i), 'utf-8') + b'].color'].load(*entity.color)
            self.uniforms[b'light[' + bytes(str(i), 'utf-8') + b'].constant'].load(entity.attenuation[0])
            self.uniforms[b'light[' + bytes(str(i), 'utf-8') + b'].linear'].load(entity.attenuation[1])
            self.uniforms[b'light[' + bytes(str(i), 'utf-8') + b'].quadratic'].load(entity.attenuation[1])

        # PREPARE MODELS
        for model_index, texture_mapping in entities.items():

            model = models[model_index]
            model.enable()

            # PREPARE TEXTURES
            for texture_index, entity_list in texture_mapping.items():

                textures[texture_index].enable()

                # PREPARE ENTITIES
                for entity in entity_list:
                    entity.get_transformation_matrix(self.uniforms[b'transformation'])
                    model.draw()


class SelectShader(ShaderProgram):
    def __init__(self):
        super().__init__(
            shaders=[open('shaders/select_shader.vs', 'rb').read(), open('shaders/select_shader.fs', 'rb').read()],
            attributes=[b'position'],
            uniforms=[b'transformation', b'perspective', b'view', b'color']
        )

    def draw(self, uniforms, entity, models, textures=(), color=(1.0, 1.0, 1.0), *args, **kwargs):
        glUseProgram(self)
        glDisable(GL_DEPTH_TEST)

        # Draw objects once as invisible to set stencil values.
        glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)  # Don't write any color values to color buffer.
        glStencilMask(0xFF)  # Enable writing.

        model = models[entity.model]

        model.positions.enable()
        model.indices.enable()

        self.uniforms[b'perspective'].load(uniforms.get(b'perspective').ctypes.data_as(POINTER(GLfloat)))
        self.uniforms[b'view'].load(uniforms.get(b'view').ctypes.data_as(POINTER(GLfloat)))
        self.uniforms[b'color'].load(*color)

        entity.get_transformation_matrix(location=self.uniforms[b'transformation'])

        model.draw()

        # Draw again with larger model.
        glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)

        glStencilFunc(GL_NOTEQUAL, 1, 0xFF)  # Update with 1's where the objects are rendered.
        glStencilMask(0x00)  # Value that AND's the value written to buffer. 0x00 basically disables writing to stencil.

        glUniformMatrix4fv(
            self.uniforms[b'transformation'], 1, GL_TRUE,
            create_transformation_matrix(
                *entity._location, *entity.rotation, *(entity.scale + 0.05)
            ).ctypes.data_as(POINTER(GLfloat))
        )

        model.draw()

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

        glDisableVertexAttribArray(0)

        glEnable(GL_DEPTH_TEST)
        glStencilMask(0xFF)


class FontShader(ShaderProgram):
    def __init__(self):
        super().__init__(
            shaders=[open('shaders/font_shader.vs', 'rb').read(), open('shaders/font_shader.fs', 'rb').read()],
            attributes=[b'position', b'texture_coordinate'],
            uniforms=[b'transformation', b'color']
        )

    def draw(self, uniforms, text, quad, textures=(), *args, **kwargs):
        glUseProgram(self)
        glDisable(GL_DEPTH_TEST)

        quad.enable()

        self.uniforms[b'color'].load(0.3, 0.3, 0.5)

        text.get_transformation_matrix_2D(location=self.uniforms[b'transformation'])

        textures.enable()

        quad.draw()

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

        glDisableVertexAttribArray(0)

        glEnable(GL_DEPTH_TEST)

