from abc import abstractmethod

from pyglet.gl import (
    glBindBuffer, glEnableVertexAttribArray, glVertexAttribPointer, GL_FLOAT, GL_ARRAY_BUFFER, GL_FALSE,
    GL_ELEMENT_ARRAY_BUFFER, glDisableVertexAttribArray, glDrawElements, GL_TRIANGLES, GL_UNSIGNED_INT,
    glDrawArrays, GLuint, glGenBuffers, glBufferData, GL_STATIC_DRAW, GLfloat, GLushort, GLubyte
)
from source.c_bindings import sizeof
from source.gl_helpers import GL_TYPE_TO_CONSTANT, GL_TYPES, GL_UNSIGNED_INTEGER_TYPES


class VBO:

    TARGET = GL_ARRAY_BUFFER
    VALID_TYPES = GL_TYPES

    @classmethod
    def create(cls, data, dimension, type=GLfloat, draw_mode=GL_STATIC_DRAW):
        assert type in VBO.VALID_TYPES, "Invalid type for VBO!"

        handle = GLuint()
        glGenBuffers(1, handle)
        glBindBuffer(VBO.TARGET, handle)
        glBufferData(VBO.TARGET, len(data) * sizeof(type), (type * len(data))(*data), draw_mode)
        return cls(handle, dimension, GL_TYPE_TO_CONSTANT[type])

    def __init__(self, id_, dimension, type=GL_FLOAT):
        self.id = id_
        self.dimension = dimension
        self.type = type

    def enable(self, index):
        glBindBuffer(VBO.TARGET, self.id)
        glEnableVertexAttribArray(index)

        # TODO(ted): Assuming data should not be normalized and without stride or a pointer
        normalized = GL_FALSE
        stride  = 0
        pointer = 0
        glVertexAttribPointer(index, self.dimension, self.type, normalized, stride, pointer)

    @staticmethod
    def disable():
        glBindBuffer(VBO.TARGET, 0)


class IBO:

    TARGET = GL_ELEMENT_ARRAY_BUFFER
    VALID_TYPES = GL_UNSIGNED_INTEGER_TYPES

    @classmethod
    def create(cls, data, type=GLuint, draw_mode=GL_STATIC_DRAW):
        assert type in IBO.VALID_TYPES, "Invalid type for IBO!"

        handle = GLuint()
        glGenBuffers(1, handle)
        glBindBuffer(IBO.TARGET, handle)
        glBufferData(IBO.TARGET, len(data) * sizeof(type), (type * len(data))(*data), draw_mode)

        return cls(handle, len(data), GL_TYPE_TO_CONSTANT[type])

    def __init__(self, id_, count, type=GL_UNSIGNED_INT):
        self.id = id_
        self.type  = type
        self.count = count


    def enable(self):
        glBindBuffer(IBO.TARGET, self.id)

    @staticmethod
    def disable():
        glBindBuffer(IBO.TARGET, 0)


class Model:

    @staticmethod
    def create(vbos, *, ibo=None, count=-1, draw_mode=GL_TRIANGLES):
        assert ibo is not None or count != -1, "Must specify either IBO or count to create model!"

        if ibo is not None:
            return ModelWithIndexBuffer(vbos, ibo, draw_mode)
        else:
            return ModelWithoutIndexBuffer(vbos, count, draw_mode)

    @abstractmethod
    def enable(self):
        pass

    @abstractmethod
    def disable(self):
        pass

    @abstractmethod
    def render(self):
        pass


class ModelWithIndexBuffer(Model):
    def __init__(self, vbos, ibo, draw_mode=GL_TRIANGLES):
        self.vbos = vbos
        self.ibo  = ibo
        self.draw_mode = draw_mode

    def enable(self):
        for index, vbo in enumerate(self.vbos):
            vbo.enable(index=index)
        self.ibo.enable()

    def disable(self):
        for index in range(len(self.vbos)):
            glDisableVertexAttribArray(index)
        self.ibo.disable()

    def render(self):
        glDrawElements(self.draw_mode, self.ibo.count, self.ibo.type, 0)



class ModelWithoutIndexBuffer(Model):
    def __init__(self, vbos, count, draw_mode=GL_TRIANGLES):
        self.vbos  = vbos
        self.count = count
        self.draw_mode = draw_mode

    def enable(self):
        for index, vbo in enumerate(self.vbos):
            vbo.enable(index=index)

    def disable(self):
        for index in range(len(self.vbos)):
            glDisableVertexAttribArray(index)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def render(self):
        glDrawArrays(self.draw_mode, 0, self.count)



def create_cube():
    positions = VBO.create(data=[
        -0.5, 0.5, -0.5, -0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, -0.5,  # Top.
        -0.5, -0.5, -0.5, 0.5, -0.5, -0.5, 0.5, -0.5, 0.5, -0.5, -0.5, 0.5,  # Bottom.
        -0.5, -0.5, -0.5, -0.5, -0.5, 0.5, -0.5, 0.5, 0.5, -0.5, 0.5, -0.5,  # Left.
        0.5, -0.5, 0.5, 0.5, -0.5, -0.5, 0.5, 0.5, -0.5, 0.5, 0.5, 0.5,  # Right.
        -0.5, -0.5, 0.5, 0.5, -0.5, 0.5, 0.5, 0.5, 0.5, -0.5, 0.5, 0.5,  # Front.
        0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5, -0.5, 0.5, 0.5, -0.5,  # Back.
    ], dimension=3)

    texture_coordinates = VBO.create(data=[
        0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0,  # Top.
        0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0,  # Bottom.
        0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0,  # Left.
        0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0,  # Right.
        0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0,  # Front.
        0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0,  # Back.
    ], dimension=2)

    normals = VBO.create(data=[
        0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,  # Top.
        0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0,  # Bottom.
        -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0,  # Left.
        1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0,  # Right.
        0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,  # Front.
        0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0,  # Back.
    ], dimension=3)

    indices = IBO.create(data=[
        0, 1, 3, 3, 1, 2,
        4, 5, 7, 7, 5, 6,
        8, 9, 11, 11, 9, 10,
        12, 13, 15, 15, 13, 14,
        16, 17, 19, 19, 17, 18,
        20, 21, 23, 23, 21, 22
    ])

    return Model.create(vbos=(positions, texture_coordinates, normals), ibo=indices)



def load_model(path):
    # TODO(ted): Assumes vertices of dimension 3, texture coordinates of dimension 2 and normals of dimension 3.

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
                    vertex_index, texture_index, normal_index = vertex
                    vertex_index, texture_index, normal_index = int(vertex_index), int(texture_index), int(normal_index)
                    sorted_vertices.extend(vertices[vertex_index - 1])
                    sorted_normals.extend(normals[normal_index - 1])
                    sorted_texture_coordinates.extend(texture_coordinates[texture_index - 1])
                    index += 1
                else:
                    indices.append(unique_data.index(vertex))

            line = text_file.readline()


    vertices            = VBO.create(data=sorted_vertices,            dimension=3)
    texture_coordinates = VBO.create(data=sorted_texture_coordinates, dimension=2)
    normals             = VBO.create(data=sorted_normals,             dimension=3)

    indices = IBO.create(data=indices)

    return Model.create(vbos=(vertices, texture_coordinates, normals), ibo=indices)
