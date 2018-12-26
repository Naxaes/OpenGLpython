from pyglet.gl import (
    glGenBuffers, glBindBuffer, glBufferData, glEnableVertexAttribArray, glDisableVertexAttribArray,
    glVertexAttribPointer, glDrawElements, glUniformMatrix4fv, glUniformMatrix3fv,

    GL_ARRAY_BUFFER, GL_ELEMENT_ARRAY_BUFFER, GL_STATIC_DRAW, GL_FLOAT, GL_FALSE, GL_TRIANGLES, GL_UNSIGNED_INT,
    GL_TRUE,

    GLfloat, GLuint
)
from ctypes import sizeof, POINTER
import numpy

from restart.mathematics import create_transformation_matrix, create_2D_transformation_matrix, sin, cos



class Entity(GLuint):

    __slots__ = 'location', 'rotation', 'scale', 'model', 'textures'

    ID = 0

    def __init__(self, location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), model=0, textures=()):
        super().__init__(Entity.ID)
        Entity.ID += 1

        self.location = numpy.array(location, dtype=GLfloat)
        self.rotation = numpy.array(rotation, dtype=GLfloat)
        self.scale = numpy.array(scale, dtype=GLfloat)
        self.model = model

        if isinstance(textures, tuple):
            self.textures = textures
        elif hasattr(textures, '__iter__'):
            self.textures = tuple(textures)
        else:
            self.textures = (textures, )

    # @property
    # def location(self):
    #     return self._location
    #
    # @location.setter
    # def location(self, values):
    #     self._location[:] = values
    #     self.transformation[3, 0:3] = values
    #
    # @property
    # def rotation(self):
    #     return self._rotation
    #
    # @rotation.setter
    # def rotation(self, values):
    #     self._rotation[:] = values
    #     rx, ry, rz = values
    #     matrices = []
    #     if rx:
    #         matrices.append(
    #             numpy.array(
    #                 ((1, 0,        0,     ),
    #                  (0, cos(rx), -sin(rx)),
    #                  (0, sin(rx),  cos(rx)),
    #                  ), dtype=self.transformation.dtype
    #             )
    #         )
    #     if ry:
    #         matrices.append(
    #             numpy.array(
    #             ((cos(ry), 0, sin(ry), 0),
    #              (0, 1, 0, 0),
    #              (-sin(ry), 0, cos(ry), 0),
    #              (0, 0, 0, 1)), dtype=GLfloat
    #             )
    #         )
    #     if rz:
    #         matrices.append(
    #             numpy.array(
    #                 ((cos(rz), -sin(rz), 0),
    #                  (sin(rz),  cos(rz), 0),
    #                  (0,        0,       1)
    #                  ), dtype=GLfloat
    #             )
    #         )
    #     self.transformation[3, 0:3] += values
    #
    # @property
    # def scale(self):
    #     return self._scale
    #
    # @scale.setter
    # def scale(self, values):
    #     self._scale[:] = values
    #     numpy.fill_diagonal(self.transformation, values)

    def get_transformation_matrix(self):
        return create_transformation_matrix(*self.location, *self.rotation, *self.scale)

    def get_transformation_matrix_2D(self):
        return create_2D_transformation_matrix(*self.location[0:2], self.rotation[0], *self.scale[0:2])


class Light(Entity):

    __slots__ = 'color', 'attenuation'

    def __init__(self, *args, **kwargs):
        self.color = kwargs.pop('color', (1.0, 1.0, 1.0))
        self.attenuation = kwargs.pop('attenuation', (1.0, 0.009, 0.032))
        super().__init__(*args, **kwargs)


class VBO(GLuint):

    DATA_TYPE_CONSTANT = {
        GLfloat: GL_FLOAT,
    }

    BOUND_BUFFER = None

    def __init__(self, attribute_index, buffer, dimension, data_type=GLfloat):
        # TODO Make so you don't have to initialize with a buffer.

        super().__init__()
        count = len(buffer)
        size = count * sizeof(data_type)
        Array = data_type * count

        glGenBuffers(1, self)
        glBindBuffer(GL_ARRAY_BUFFER, self)
        glBufferData(GL_ARRAY_BUFFER, size, Array(*buffer), GL_STATIC_DRAW)

        self.count = count
        self.size = size

        self.attribute_index = attribute_index
        self.dimension = dimension
        self.data_type_constant = VBO.DATA_TYPE_CONSTANT[data_type]

    def enable(self):
        VBO.BOUND_BUFFER = self
        glBindBuffer(GL_ARRAY_BUFFER, self)
        glEnableVertexAttribArray(self.attribute_index)
        glVertexAttribPointer(self.attribute_index, self.dimension, self.data_type_constant, GL_FALSE, 0, 0)

    @staticmethod
    def reset():
        VBO.BOUND_BUFFER = None
        glBindBuffer(GL_ARRAY_BUFFER, 0)


class IBO(GLuint):

    BOUND_BUFFER = None

    def __init__(self, buffer, data_type=GLuint):
        # TODO Make so you don't have to initialize with a buffer.
        super().__init__()
        count = len(buffer)
        size  = count * sizeof(data_type)
        Array = data_type * count
        
        glGenBuffers(1, self)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, size, Array(*buffer), GL_STATIC_DRAW)

        self.count = count
        self.size  = size

    def enable(self):
        IBO.BOUND_BUFFER = self
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self)

    @staticmethod
    def reset():
        IBO.BOUND_BUFFER = None
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        

class StaticModel(GLuint):

    __slots__ = 'positions', 'texture_coordinates', 'normals', 'indices', 'count'

    ID = 0

    def __init__(self, positions, texture_coordinates, normals, indices):
        super().__init__(StaticModel.ID)
        StaticModel.ID += 1

        position_vbo = VBO(0, positions, 3)
        texture_coordinates_vbo = VBO(1, texture_coordinates, 2)
        normal_vbo = VBO(2, normals, 3)

        indexed_vbo = IBO(indices)

        self.positions = position_vbo
        self.texture_coordinates = texture_coordinates_vbo
        self.normals = normal_vbo
        self.indices = indexed_vbo
        self.count = indexed_vbo.count

    def enable(self):
        self.positions.enable()
        self.texture_coordinates.enable()
        self.normals.enable()
        self.indices.enable()

    def draw(self):
        """
        This function depends on:

            1. The bound shader.
            2. The bound textures.
            3. The uploaded uniforms

        Returns:

        """
        glDrawElements(GL_TRIANGLES, self.count, GL_UNSIGNED_INT, 0)

    @staticmethod
    def reset():
        VBO.reset()
        IBO.reset()

    @classmethod
    def as_cube(cls):
        vertices = [
            -0.5,  0.5, -0.5, -0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5, -0.5,  # Top.
            -0.5, -0.5, -0.5,  0.5, -0.5, -0.5,  0.5, -0.5,  0.5, -0.5, -0.5,  0.5,  # Bottom.
            -0.5, -0.5, -0.5, -0.5, -0.5,  0.5, -0.5,  0.5,  0.5, -0.5,  0.5, -0.5,  # Left.
             0.5, -0.5,  0.5,  0.5, -0.5, -0.5,  0.5,  0.5, -0.5,  0.5,  0.5,  0.5,  # Right.
            -0.5, -0.5,  0.5,  0.5, -0.5,  0.5,  0.5,  0.5,  0.5, -0.5,  0.5,  0.5,  # Front.
             0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5,  0.5, -0.5,  0.5,  0.5, -0.5,  # Back.
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
             0.0,  1.0,  0.0,  0.0,  1.0,  0.0,  0.0,  1.0,  0.0,  0.0,  1.0,  0.0,  # Top.
             0.0, -1.0,  0.0,  0.0, -1.0,  0.0,  0.0, -1.0,  0.0,  0.0, -1.0,  0.0,  # Bottom.
            -1.0,  0.0,  0.0, -1.0,  0.0,  0.0, -1.0,  0.0,  0.0, -1.0,  0.0,  0.0,  # Left.
             1.0,  0.0,  0.0,  1.0,  0.0,  0.0,  1.0,  0.0,  0.0,  1.0,  0.0,  0.0,  # Right.
             0.0,  0.0,  1.0,  0.0,  0.0,  1.0,  0.0,  0.0,  1.0,  0.0,  0.0,  1.0,  # Front.
             0.0,  0.0, -1.0,  0.0,  0.0, -1.0,  0.0,  0.0, -1.0,  0.0,  0.0, -1.0,  # Back.
        ]
        indices = [
            0,  1,  3,  3,  1,  2,
            4,  5,  7,  7,  5,  6,
            8,  9,  11, 11, 9,  10,
            12, 13, 15, 15, 13, 14,
            16, 17, 19, 19, 17, 18,
            20, 21, 23, 23, 21, 22
        ]
        return cls(vertices, texture_coordinates, normals, indices)

    @classmethod
    def from_obj_file(cls, path):

        vertices = []
        normals = []
        texture_coordinates = []

        with open(path) as text_file:

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
                        vertex_index, texture_index, normal_index = map(int, vertex)
                        sorted_vertices.extend(vertices[vertex_index - 1])
                        sorted_normals.extend(normals[normal_index - 1])
                        sorted_texture_coordinates.extend(texture_coordinates[texture_index - 1])
                        index += 1
                    else:
                        indices.append(unique_data.index(vertex))

                line = text_file.readline()

        return cls(sorted_vertices, sorted_texture_coordinates, sorted_normals, indices)


class Quad2D(GLuint):

    ID = 0

    def __init__(self, positions, texture_coordinates, indices):

        assert len(positions) // 2 == len(texture_coordinates) // 2, 'Size mismatch'

        super().__init__(Quad2D.ID)
        Quad2D.ID += 1

        position_vbo = VBO(0, positions, 2)
        texture_coordinates_vbo = VBO(1, texture_coordinates, 2)

        indexed_vbo = IBO(indices)

        self.positions = position_vbo
        self.texture_coordinates = texture_coordinates_vbo
        self.indices = indexed_vbo
        self.count = self.indices.count

    def enable(self):
        self.positions.enable()
        self.texture_coordinates.enable()
        self.indices.enable()

    def draw(self):
        """
        This function depends on:

            1. The bound shader.
            2. The bound textures.
            3. The uploaded uniforms

        Returns:

        """
        glDrawElements(GL_TRIANGLES, self.count, GL_UNSIGNED_INT, 0)