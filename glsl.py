from pyglet.gl import GLfloat, glUniform1f, glUniform2f, glUniform3f, glUniform4f
import sys
import textwrap
import re

"""
vecn()              -> vecn(0, 0, ..., 0)
vecn(x)             -> vecn(x, x, ..., x)
vecn(x0, x1, ...)   -> vecn(x0, x1, ..., xn)
vecn(*iterable)     -> vecn(x0, x1, ..., xn)

"""


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

    # Only float exists in GLSL 2.1 (double exists in later versions).
    *GLSL_MATRICES,

    # The following uniforms all have three prefixes: None == float, i == integer and u == unsigned integer,
    *GLSL_SAMPLERS,
    *GLSL_IMAGES
}


DATA_TYPE_TO_FUNCTION = {
    'Float': glUniform1f,
    'Vec2' : glUniform2f,
    'Vec3' : glUniform3f,
    'Vec4' : glUniform4f
}


vector_mapping = {
    'x': 0, 'r': 0, 's': 0,
    'y': 1, 'g': 1, 't': 1,
    'z': 2, 'b': 2, 'p': 2,
    'w': 3, 'a': 3, 'q': 3,
}


class Float(GLfloat):

    def __init__(self, value=None):
        if value:
            super().__init__(value)
        else:
            super().__init__()

    def __add__(self, other):
        if isinstance(other, self.__class__.__bases__):
            return self.__class__(self.value + other.value)
        else:
            return self.__class__(self.value + other)

    def __radd__(self, other):
        if isinstance(other, self.__class__.__bases__):
            return self.__class__(self.value + other.value)
        else:
            return self.__class__(self.value + other)

    def __sub__(self, other):
        if isinstance(other, self.__class__.__bases__):
            return self.__class__(self.value - other.value)
        else:
            return self.__class__(self.value - other)

    def __rsub__(self, other):
        if isinstance(other, self.__class__.__bases__):
            return self.__class__(self.value - other.value)
        else:
            return self.__class__(self.value - other)

    def __mul__(self, other):
        if isinstance(other, self.__class__.__bases__):
            return self.__class__(self.value * other.value)
        else:
            return self.__class__(self.value * other)

    def __rmul__(self, other):
        if isinstance(other, self.__class__.__bases__):
            return self.__class__(self.value * other.value)
        else:
            return self.__class__(self.value * other)

    def __truediv__(self, other):
        if isinstance(other, self.__class__.__bases__):
            return self.__class__(self.value / other.value)
        else:
            return self.__class__(self.value / other)

    def __rtruediv__(self, other):
        if isinstance(other, self.__class__.__bases__):
            return self.__class__(self.value / other.value)
        else:
            return self.__class__(self.value / other)

    def __floordiv__(self, other):
        if isinstance(other, self.__class__.__bases__):
            return self.__class__(self.value // other.value)
        else:
            return self.__class__(self.value // other)

    def __rfloordiv__(self, other):
        if isinstance(other, self.__class__.__bases__):
            return self.__class__(self.value // other.value)
        else:
            return self.__class__(self.value // other)

    def __eq__(self, other):
        if isinstance(other, self.__class__.__bases__):
            return self.value == other.value
        else:
            return self.value == other

    def __ne__(self, other):
        if isinstance(other, self.__class__.__bases__):
            return self.value != other.value
        else:
            return self.value != other

    def __ge__(self, other):
        if isinstance(other, self.__class__.__bases__):
            return self.value >= other.value
        else:
            return self.value >= other

    def __le__(self, other):
        if isinstance(other, self.__class__.__bases__):
            return self.value <= other.value
        else:
            return self.value <= other

    def __gt__(self, other):
        if isinstance(other, self.__class__.__bases__):
            return self.value > other.value
        else:
            return self.value > other

    def __lt__(self, other):
        if isinstance(other, self.__class__.__bases__):
            return self.value < other.value
        else:
            return self.value < other

    def __setitem__(self, key, value):
        self.value = value

    def __repr__(self):
        return '{class_name}({value})'.format(class_name=self.__class__.__name__, value=self.value)


class Vec2(GLfloat * 2):  # For all glsl data structures, just change the type and the value. Then copy rest of class.

    def __init__(self, data_sequence=None, *data_varargs):
        if data_sequence is None:
            data = (0,)
        elif isinstance(data_sequence, (tuple, list, set)):
            data = data_sequence
        else:
            data = data_sequence, *data_varargs

        length = len(data)
        elements = super()._length_

        if length == 1:
            data *= elements
            super().__init__(*data)
        elif length <= elements:
            super().__init__(*data)
        else:
            raise TypeError('{} takes at most {} argument ({} given)'.format(self.__class__.__name__, elements, length))

        self.__dict__['dtype'] = super()._type_

    def __add__(self, other):
        return Vec2(self[0] + other[0], self[1] + other[1])

    def __radd__(self, other):
        return Vec2(self[0] + other[0], self[1] + other[1])

    def __sub__(self, other):
        return Vec2(self[0] - other[0], self[1] - other[1])

    def __rsub__(self, other):
        return Vec2(self[0] - other[0], self[1] - other[1])

    def __mul__(self, other):
        try:
            return Vec2(self[0] * other, self[1] * other)
        except:
            print("Multiplying two vectors is ambiguous. Use appropriate function call instead.", file=sys.stderr)

    def __rmul__(self, other):
        try:
            return Vec2(self[0] * other, self[1] * other)
        except:
            print("Multiplying two vectors is ambiguous. Use appropriate function call instead.", file=sys.stderr)

    def __iadd__(self, other):
        self[:] = self[0] + other[0], self[1] + other[1]

    def __isub__(self, other):
        self[:] = self[0] - other[0], self[1] - other[1]

    def __imul__(self, other):
        try:
            self[:] = self[0] * other, self[1] * other
        except IndexError:
            print("Multiplying two vectors is ambiguous. Use appropriate function call instead.", file=sys.stderr)

    def __eq__(self, other):
        return self[0] == other[0] and self[1] == other[1]

    def __ne__(self, other):
        return self[0] != other[0] or self[1] != other[1]

    def __setattr__(self, key, value):
        try:
            if isinstance(value, (float, int)):                # Setting a single value.
                self[vector_mapping[key]] = value
            else:
                for i, character in enumerate(key):     # Setting multiple values.
                    self[vector_mapping[character]] = value[i]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + key)

    def __getattr__(self, item):
        try:
            if isinstance(item, (list, tuple, set)):
                return tuple(self[vector_mapping[character]] for character in item)
            else:
                return self[vector_mapping[item]]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + item)

    def __repr__(self):
        return self.__class__.__name__ + '(' + ', '.join(str(x) for x in self[:]) + ')'


class Vec3(GLfloat * 3):

    def __init__(self, data_sequence=None, *data_varargs):
        if data_sequence is None:
            data = (0,)
        elif isinstance(data_sequence, (tuple, list, set)):
            data = data_sequence
        else:
            data = data_sequence, *data_varargs

        length = len(data)
        elements = super()._length_

        if length == 1:
            data *= elements
            super().__init__(*data)
        elif length <= elements:  # This should probably be removed.
            super().__init__(*data)
        else:
            raise TypeError('{} takes at most {} argument ({} given)'.format(self.__class__.__name__, elements, length))

        self.__dict__['dtype'] = super()._type_

    def __add__(self, other):
        return Vec3(self[0] + other[0], self[1] + other[1], self[2] + other[2])

    def __radd__(self, other):
        return Vec3(self[0] + other[0], self[1] + other[1], self[2] + other[2])

    def __sub__(self, other):
        return Vec3(self[0] - other[0], self[1] - other[1], self[2] - other[2])

    def __rsub__(self, other):
        return Vec3(self[0] - other[0], self[1] - other[1], self[2] - other[2])

    def __mul__(self, other):
        try:
            return Vec3(self[0] * other, self[1] * other, self[2] * other)
        except Exception as e:
            print(e)
            print("Multiplying two vectors is ambiguous. Use appropriate function call instead.", file=sys.stderr)

    def __rmul__(self, other):
        try:
            return Vec3(self[0] * other, self[1] * other, self[2] * other)
        except Exception as e:
            print(e)
            print("Multiplying two vectors is ambiguous. Use appropriate function call instead.", file=sys.stderr)

    def __iadd__(self, other):
        self[:] = self[0] + other[0], self[1] + other[1], self[2] + other[2]

    def __isub__(self, other):
        self[:] = self[0] - other[0], self[1] - other[1], self[2] - other[2]

    def __imul__(self, other):
        try:
            self[:] = self[0] * other, self[1] * other, self[2] * other
        except:
            print("Multiplying two vectors is ambiguous. Use appropriate function call instead.", file=sys.stderr)

    def __eq__(self, other):
        return self[0] == other[0] and self[1] == other[1] and self[2] == other[2]

    def __ne__(self, other):
        return self[0] != other[0] or self[1] != other[1] or self[2] != other[2]

    def __setattr__(self, key, value):
        try:
            if isinstance(value, (float, int)):                # Setting a single value.
                self[vector_mapping[key]] = value
            else:
                for i, character in enumerate(key):     # Setting multiple values.
                    self[vector_mapping[character]] = value[i]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + key)

    def __getattr__(self, item):
        try:
            if isinstance(item, (list, tuple, set)):
                return tuple(self[vector_mapping[character]] for character in item)
            else:
                return self[vector_mapping[item]]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + item)

    def __repr__(self):
        return self.__class__.__name__ + '(' + ', '.join(str(x) for x in self[:]) + ')'


class Vec4(GLfloat * 4):

    def __init__(self, data_sequence=None, *data_varargs):
        if data_sequence is None:
            data = (0,)
        elif isinstance(data_sequence, (tuple, list, set)):
            data = data_sequence
        else:
            data = data_sequence, *data_varargs

        length = len(data)
        elements = super()._length_

        if length == 1:
            data *= elements
            super().__init__(*data)
        elif length <= elements:  # This should probably be removed.
            super().__init__(*data)
        else:
            raise TypeError('{} takes at most {} argument ({} given)'.format(self.__class__.__name__, elements, length))

        self.__dict__['dtype'] = super()._type_

    def __add__(self, other):
        return Vec4(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])

    def __radd__(self, other):
        return Vec4(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])

    def __sub__(self, other):
        return Vec4(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3])

    def __rsub__(self, other):
        return Vec4(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3])

    def __mul__(self, other):
        try:
            return Vec4(self[0] * other, self[1] * other, self[2] * other, self[3] * other)
        except:
            print("Multiplying two vectors is ambiguous. Use appropriate function call instead.", file=sys.stderr)

    def __rmul__(self, other):
        try:
            return Vec4(self[0] * other, self[1] * other, self[2] * other, self[3] * other)
        except:
            print("Multiplying two vectors is ambiguous. Use appropriate function call instead.", file=sys.stderr)

    def __iadd__(self, other):
        self[:] = self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3]

    def __isub__(self, other):
        self[:] = self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3]

    def __imul__(self, other):
        try:
            self[:] = self[0] * other, self[1] * other, self[2] * other, self[3] * other
        except:
            print("Multiplying two vectors is ambiguous. Use appropriate function call instead.", file=sys.stderr)

    def __eq__(self, other):
        return self[0] == other[0] and self[1] == other[1] and self[2] == other[2] and self[3] == other[3]

    def __ne__(self, other):
        return self[0] != other[0] or self[1] != other[1] or self[2] != other[2] or self[3] != other[3]

    def __setattr__(self, key, value):
        try:
            if isinstance(value, (float, int)):                # Setting a single value.
                self[vector_mapping[key]] = value
            else:
                for i, character in enumerate(key):     # Setting multiple values.
                    self[vector_mapping[character]] = value[i]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + key)

    def __getattr__(self, item):
        try:
            if isinstance(item, (list, tuple, set)):
                return tuple(self[vector_mapping[character]] for character in item)
            else:
                return self[vector_mapping[item]]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + item)

    def __repr__(self):
        return self.__class__.__name__ + '(' + ', '.join(str(x) for x in self[:]) + ')'


class Mat4(GLfloat * 16):

    def __init__(self, data_sequence=None, *data_varargs):
        if data_sequence is None:
            data = (0,)
        elif isinstance(data_sequence, (tuple, list, set)):
            data = data_sequence
        else:
            data = data_sequence, *data_varargs

        length = len(data)
        elements = super()._length_

        if length == 1:
            data *= elements
            super().__init__(*data)
        elif length <= elements:  # This should probably be removed.
            super().__init__(*data)
        else:
            raise TypeError('{} takes at most {} argument ({} given)'.format(self.__class__.__name__, elements, length))

        self.__dict__['dtype'] = super()._type_

    def __add__(self, other):
        return Mat4(a + b for a, b in zip(self, other))

    def __sub__(self, other):
        return Mat4(a - b for a, b in zip(self, other))

    def __mul__(self, other):
        try:
            return Mat4(a * other for a in self)
        except:
            print("Multiplying two vectors is ambiguous. Use appropriate function call instead.", file=sys.stderr)

    def __iadd__(self, other):
        self[:] = (a + b for a, b in zip(self, other))

    def __isub__(self, other):
        self[:] = (a - b for a, b in zip(self, other))

    def __imul__(self, other):
        try:
            self[:] = (a * other for a in self)
        except:
            print("Multiplying two vectors is ambiguous. Use appropriate function call instead.", file=sys.stderr)

    # def __getitem__(self, item):
    #     return self[4 * item[0] + item[1]]
    #
    # def __setitem__(self, key, value):
    #     self[4 * key[0] + key[1]] = value

    def __setattr__(self, key, value):
        try:
            if isinstance(value, (float, int)):                # Setting a single value.
                self[vector_mapping[key]] = value
            else:
                for i, character in enumerate(key):     # Setting multiple values.
                    self[vector_mapping[character]] = value[i]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + key)

    def __getattr__(self, item):
        try:
            if isinstance(item, (list, tuple, set)):
                return tuple(self[vector_mapping[character]] for character in item)
            else:
                return self[vector_mapping[item]]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + item)

    def __repr__(self):
        start = self.__class__.__name__ + ' [\n\t'
        stop = ']'
        elements = []
        for row in range(4):
            temp = []
            for col in range(4):
                temp.append(str(self[row, col]))
            elements.append(temp)

        return start + '\n\t'.join(', '.join(rows) for rows in elements) + stop


class Array:

    def __init__(self, glsl_type, size, *data):
        a = (glsl_type.dtype * glsl_type._length_ * size)

        if len(data) == 1:
           a[:] = 0


def struct(class_name, fields, print_class=False):
    """
    Creates a struct class which can be sent in the shader program.

    Examples:
        # >>> PointLight = struct('PointLight', fields=['vec3 location', 'vec3 color', 'float intensity'])
        # >>> light = PointLight(color=(255, 0, 255))
        # >>> light.location = 0, -50, 0
        # >>> light
        PointLight:
            vec3 location = Vec3(0.0, -50.0, 0.0)
            vec3 color = Vec3(255.0, 0.0, 255.0)
            float intensity = Float(0.0)

    Args:
        class_name: Name of the created struct class.
        fields:
        print_class: Prints the class definition. Could be useful if you want to copy and modify it yourself and/or not
                     create the class at runtime.

    Returns:
        class
    """
    field_types = []
    field_names = []
    for field in fields:
        field_type, field_name = field.split()
        if field_type not in GLSL_DATA_TYPES:
            raise TypeError(field_type + ' is not a valid glsl data type')
        field_types.append(field_type.title())
        field_names.append(field_name)

    # TODO Make theses lines in a function in a different module?
    slots = ', '.join('"_{}"'.format(field_name) for field_name in field_names)
    attributes = '\n        '.join(
        'self._{field_name} = {field_type}({field_name})'.format(field_name=field_name, field_type=field_type)
        for field_name, field_type in zip(field_names, field_types))

    # TODO Refactor the templates elsewhere?
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

    def __init__(self, {field_names}):
        {attributes}

    def __repr__(self):
        attributes = '\\n'.join('    %s = %s' % (field, getattr(self, name)) for field, name in zip({fields}, self.__slots__))
        return '{name}:\\n' + attributes
    {properties}
""".format(
        name=class_name, slots=slots, attributes=attributes, properties=properties, fields=fields,
        field_names=', '.join(field + '=None' for field in field_names))

    if print_class:
        print(class_template)

    namespace = globals()
    exec(class_template, namespace)
    return namespace[class_name]



if __name__ == '__main__':

    a = Vec2(1, 2)
    a += 2, 3
    print(a)