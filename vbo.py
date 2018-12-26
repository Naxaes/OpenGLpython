from pyglet.gl import (
    glGenBuffers, glBindBuffer, glBufferData, glEnableVertexAttribArray, glVertexAttribPointer, glDrawElements,
    glDisableVertexAttribArray, glDrawArrays, glGetAttribLocation,

    GL_ARRAY_BUFFER, GL_STATIC_DRAW, GL_ELEMENT_ARRAY_BUFFER, GL_FLOAT, GL_FALSE, GL_TRIANGLES, GL_UNSIGNED_INT,
)

from ctypes import c_uint, c_float, sizeof


class VBO(c_uint):

    def __init__(self, data, dimension=3):
        """
        Vertex Buffer Object for storing data in OpenGl.

        Args:
            data: An array of values.
            dimension: Whether the array is 1D, 2D, 3D or 4D.
        """
        data_type = c_float
        elements = len(data)

        buffer_type = data_type * elements
        buffer = buffer_type()
        buffer[:] = data  # About 2.5 times faster than passing arguments during initialization.

        handle = c_uint()
        glGenBuffers(1, handle)
        glBindBuffer(GL_ARRAY_BUFFER, handle)
        glBufferData(GL_ARRAY_BUFFER, elements * sizeof(data_type), buffer, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        super(VBO, self).__init__(handle.value)
        self.data_type = GL_FLOAT
        self.count = elements // dimension
        self.dimension = dimension

    def bind(self):
        glBindBuffer(GL_ARRAY_BUFFER, self)


class IndexedVBO(c_uint):

    def __init__(self, data):
        count = len(data)

        buffer_type = c_uint * count
        buffer = buffer_type()
        buffer[:] = data

        handle = c_uint()
        glGenBuffers(1, handle)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, handle)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, count * sizeof(c_uint), buffer, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

        super(IndexedVBO, self).__init__(handle.value)
        self.data_type = GL_UNSIGNED_INT
        self.count = count
        self.dimension = 1

    def bind(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self)


class VAO:

    def __init__(self, indexed_vbo=None, **vbo_array):
        self.indexed_vbo = indexed_vbo
        self.vbo_array = vbo_array

    def draw(self, shader):
        attribute_table = shader.attribute_table

        self.indexed_vbo.bind()

        # Bind all attributes.
        location_list = []  # Used to disable all VertexAttribArrays.
        for name, vbo in self.vbo_array.items():
            vbo.bind()
            attribute_location = attribute_table[name]
            location_list.append(attribute_location)
            glEnableVertexAttribArray(attribute_location)
            # specify that the data for the attribute will be pulled from the buffer that is currently bound to
            # GL_ARRAY_BUFFER. (http://stackoverflow.com/questions/30016833/multiple-in-attributes-in-shader-opengl)
            glVertexAttribPointer(attribute_location, vbo.dimension, vbo.data_type, GL_FALSE, 0, 0)

        # Draw.
        # glDrawArrays(GL_TRIANGLES, 0, vbo.count)
        glDrawElements(GL_TRIANGLES, self.indexed_vbo.count, self.indexed_vbo.data_type, 0)

        # Disable and unbind everything.
        for location in location_list:
            glDisableVertexAttribArray(location)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)


def load_model(path: str, add_normals=True, add_texture_coordinates=True) -> VAO:
    """
    Loads a obj-file to a VAO (Vertex Array Object).

    Args:
        path: Path to the obj file.
        add_normals: True if VAO should contain normals.
        add_texture_coordinates: True if VAO should contain texture coordinates.

    Returns:
        VAO.
    """

    def get_face_data(line):
        temp = filter(None, line.replace('f', ' ').replace('/', ' ').split(' '))
        for _ in range(3):
            yield int(next(temp)), int(next(temp)), int(next(temp))

    vertices = []
    normals = []
    texture_coordinates = []

    with open(path) as text_file:  # TODO Is it streamed? Does it matter?
        line = text_file.readline()

        while not line.startswith('vt'):
            if line.startswith('v'):
                _, x, y, z = line.split()
                vertices.append((float(x), float(y), float(z)))
            line = text_file.readline()


        while not line.startswith('vn'):
            if line.startswith('vt') and add_texture_coordinates:
                _, u, t = line.split()
                texture_coordinates.append((float(u), float(t)))
            line = text_file.readline()

        while not line.startswith('f'):
            if line.startswith('vn') and add_normals:
                _, x, y, z = line.split()
                normals.append((float(x), float(y), float(z)))
            line = text_file.readline()

        indices = []
        unique_data = []
        sorted_vertices = []
        sorted_normals = []
        sorted_texture_coordinates = []
        index = 0

        while line.startswith('f'):
            for data in get_face_data(line):
                if data not in unique_data:
                    unique_data.append(data)
                    vertex_index, texture_index, normal_index = data
                    indices.append(index)
                    sorted_vertices.extend(vertices[vertex_index - 1])
                    sorted_normals.extend(normals[normal_index - 1])
                    sorted_texture_coordinates.extend(texture_coordinates[texture_index - 1])
                    index += 1
                else:
                    indices.append(unique_data.index(data))
            line = text_file.readline()

    vao = VAO(
        indexed_vbo=IndexedVBO(indices), location=VBO(sorted_vertices),
        texture_coordinate=VBO(sorted_texture_coordinates), normal=VBO(sorted_normals)
    )
    return vao


def create_square(topleft, bottomleft, topright, bottomright, normal):
    locations = [
        *topleft,
        *bottomleft,
        *bottomright,
        *topright
    ]
    indices = [
        0, 1, 3,
        3, 1, 2,
    ]
    texture_coordinates = [
        0, 0,
        0, 1,
        1, 1,
        1, 0
    ]
    normals = [
        *normal,
        *normal,
        *normal,
        *normal
    ]
    return VAO(
        indexed_vbo=IndexedVBO(indices), location=VBO(locations),
        texture_coordinate=VBO(texture_coordinates), normal=VBO(normals)
    )