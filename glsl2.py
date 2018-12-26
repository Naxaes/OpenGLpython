from pyglet.gl import GLboolean, GLint, GLuint, GLfloat, GLdouble
import numpy

"""
Initialization:
vecn()                 -> vecn(0, 0, ..., 0)
vecn(x)                -> vecn(x, x, ..., x)
vecn(x0, x1, ..., xn)  -> vecn(x0, x1, ..., xn)
vecn(x0, x1)           -> vecn(x0, x1, 0, 0, ..., 0)
vecn(*iterable)        -> vecn(x0, x1, ..., xn)
vecn(*iterable, xn)    -> vecn(x0, x1, ..., xn)
vecn(x0, *iterable)    -> vecn(x0, x1, ..., xn)

Adding/subtracting/multiplication/division (element-wise):
vecn(1, 2, 3) + 1               -> vecn(2, 3, 4)
vecn(1, 2, 3) + vecn(1, 2, 3)   -> vecn(2, 4, 6)

Data types:
bool, int, uint, float, double (for scalars and vectors)
float, double (for matrices)
"""

PYTHON_NUMBER = (int, float)
GLSL_NUMBER = (GLboolean, GLint, GLuint, GLfloat, GLdouble)

PYTHON_SEQUENCE = (tuple, list, set, numpy.ndarray)
GLSL_SEQUENCE = tuple(dtype * i for dtype in GLSL_NUMBER for i in range(2, 16))

PYTHON_AND_GLSL_NUMBER = PYTHON_NUMBER + GLSL_NUMBER
PYTHON_AND_GLSL_SEQUENCE = PYTHON_SEQUENCE + GLSL_SEQUENCE

ATTRIBUTE_MAPPING  = {
    'x': 0, 'r': 0, 's': 0,
    'y': 1, 'g': 1, 't': 1,
    'z': 2, 'b': 2, 'p': 2,
    'w': 3, 'a': 3, 'q': 3,
}



class Boolean(GLboolean):

    def __init__(self, value):
        if value:
            super().__init__(value)
        else:
            super().__init__()

        self.__dict__['dtype'] = super()._type_

    def __repr__(self):
        return '{class_name}({value})'.format(class_name=self.__class__.__name__, value=self.value)

    def __and__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value & other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value & other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __add__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value + other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value + other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __lshift__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value << other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value << other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mod__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value % other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value % other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __pow__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value ** other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value ** other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __floordiv__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value // other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value // other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __xor__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value ^ other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value ^ other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mul__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value * other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value * other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rshift__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value >> other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value >> other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __or__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value | other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value | other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __sub__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value - other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value - other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __imod__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value %= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value %= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ilshift__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value <<= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value <<= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __irshift__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value >>= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value >>= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __imul__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value *= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value *= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ior__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value |= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value |= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __isub__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value -= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value -= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __iand__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value &= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value &= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ixor__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value ^= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value ^= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __iadd__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value += other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value += other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ifloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value //= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value //= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ipow__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value **= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value **= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rlshift__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value << other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value << other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rand__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value & other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value & other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmul__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value * other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value * other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __radd__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value + other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value + other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rxor__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value ^ other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value ^ other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmod__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value % other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value % other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rpow__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value ** other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value ** other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ror__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value | other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value | other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rrshift__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value >> other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value >> other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rsub__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value - other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value - other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rfloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value // other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value // other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __neg__(self, other):
        return -self.value
    
    def __pos__(self, other):
        return +self.value
    
    def __invert__(self, other):
        return ~self.value
    
    def __lt__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value < other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value < other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __le__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value <= other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value <= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __eq__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value == other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value == other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ge__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value >= other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value >= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ne__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value != other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value != other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __gt__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value > other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value > other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
class Int(GLint):

    def __init__(self, value):
        if value:
            super().__init__(value)
        else:
            super().__init__()

        self.__dict__['dtype'] = super()._type_

    def __repr__(self):
        return '{class_name}({value})'.format(class_name=self.__class__.__name__, value=self.value)

    def __and__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value & other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value & other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __add__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value + other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value + other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __lshift__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value << other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value << other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mod__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value % other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value % other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __pow__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value ** other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value ** other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __floordiv__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value // other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value // other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __xor__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value ^ other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value ^ other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mul__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value * other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value * other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rshift__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value >> other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value >> other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __or__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value | other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value | other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __sub__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value - other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value - other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __imod__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value %= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value %= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ilshift__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value <<= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value <<= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __irshift__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value >>= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value >>= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __imul__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value *= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value *= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ior__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value |= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value |= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __isub__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value -= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value -= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __iand__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value &= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value &= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ixor__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value ^= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value ^= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __iadd__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value += other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value += other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ifloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value //= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value //= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ipow__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value **= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value **= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rlshift__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value << other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value << other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rand__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value & other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value & other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmul__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value * other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value * other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __radd__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value + other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value + other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rxor__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value ^ other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value ^ other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmod__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value % other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value % other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rpow__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value ** other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value ** other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ror__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value | other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value | other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rrshift__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value >> other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value >> other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rsub__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value - other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value - other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rfloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value // other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value // other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __neg__(self, other):
        return -self.value
    
    def __pos__(self, other):
        return +self.value
    
    def __invert__(self, other):
        return ~self.value
    
    def __lt__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value < other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value < other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __le__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value <= other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value <= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __eq__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value == other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value == other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ge__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value >= other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value >= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ne__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value != other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value != other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __gt__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value > other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value > other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
class Uint(GLuint):

    def __init__(self, value):
        if value:
            super().__init__(value)
        else:
            super().__init__()

        self.__dict__['dtype'] = super()._type_

    def __repr__(self):
        return '{class_name}({value})'.format(class_name=self.__class__.__name__, value=self.value)

    def __and__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value & other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value & other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __add__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value + other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value + other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __lshift__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value << other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value << other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mod__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value % other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value % other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __pow__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value ** other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value ** other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __floordiv__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value // other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value // other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __xor__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value ^ other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value ^ other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mul__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value * other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value * other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rshift__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value >> other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value >> other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __or__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value | other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value | other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __sub__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value - other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value - other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __imod__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value %= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value %= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ilshift__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value <<= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value <<= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __irshift__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value >>= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value >>= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __imul__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value *= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value *= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ior__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value |= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value |= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __isub__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value -= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value -= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __iand__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value &= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value &= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ixor__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value ^= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value ^= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __iadd__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value += other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value += other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ifloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value //= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value //= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ipow__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value **= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value **= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rlshift__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value << other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value << other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rand__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value & other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value & other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmul__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value * other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value * other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __radd__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value + other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value + other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rxor__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value ^ other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value ^ other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmod__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value % other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value % other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rpow__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value ** other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value ** other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ror__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value | other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value | other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rrshift__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value >> other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value >> other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rsub__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value - other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value - other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rfloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value // other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value // other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __neg__(self, other):
        return -self.value
    
    def __pos__(self, other):
        return +self.value
    
    def __invert__(self, other):
        return ~self.value
    
    def __lt__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value < other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value < other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __le__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value <= other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value <= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __eq__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value == other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value == other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ge__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value >= other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value >= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ne__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value != other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value != other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __gt__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value > other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value > other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
class Float(GLfloat):

    def __init__(self, value):
        if value:
            super().__init__(value)
        else:
            super().__init__()
            
        self.__dict__['dtype'] = super()._type_
    
    def __repr__(self):
        return '{class_name}({value})'.format(class_name=self.__class__.__name__, value=self.value)

    def __add__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value + other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value + other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mod__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value % other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value % other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __truediv__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value / other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value / other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __floordiv__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value // other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value // other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mul__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value * other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value * other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __pow__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value ** other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value ** other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __sub__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value - other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value - other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __imod__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value %= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value %= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __imul__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value *= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value *= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __isub__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value -= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value -= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __iadd__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value += other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value += other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ifloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value //= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value //= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __itruediv__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value /= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value /= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ipow__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value **= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value **= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rtruediv__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value / other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value / other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmul__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value * other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value * other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __radd__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value + other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value + other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmod__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value % other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value % other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rpow__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value ** other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value ** other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rsub__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value - other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value - other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rfloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value // other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value // other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __neg__(self, other):
        return -self.value
    
    def __pos__(self, other):
        return +self.value
    
    def __lt__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value < other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value < other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __le__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value <= other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value <= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __eq__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value == other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value == other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ge__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value >= other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value >= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ne__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value != other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value != other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __gt__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value > other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value > other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
class Double(GLdouble):

    def __init__(self, value):
        if value:
            super().__init__(value)
        else:
            super().__init__()
            
        self.__dict__['dtype'] = super()._type_
    
    def __repr__(self):
        return '{class_name}({value})'.format(class_name=self.__class__.__name__, value=self.value)

    def __add__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value + other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value + other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mod__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value % other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value % other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __truediv__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value / other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value / other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __floordiv__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value // other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value // other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mul__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value * other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value * other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __pow__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value ** other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value ** other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __sub__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value - other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value - other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __imod__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value %= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value %= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __imul__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value *= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value *= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __isub__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value -= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value -= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __iadd__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value += other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value += other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ifloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value //= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value //= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __itruediv__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value /= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value /= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ipow__(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value **= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value **= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rtruediv__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value / other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value / other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmul__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value * other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value * other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __radd__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value + other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value + other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmod__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value % other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value % other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rpow__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value ** other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value ** other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rsub__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value - other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value - other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rfloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value // other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value // other)
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __neg__(self, other):
        return -self.value
    
    def __pos__(self, other):
        return +self.value
    
    def __lt__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value < other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value < other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __le__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value <= other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value <= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __eq__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value == other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value == other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ge__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value >= other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value >= other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ne__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value != other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value != other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __gt__(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value > other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value > other
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
class BVec2(GLboolean * 2):

    def __init__(self, first=None, *data):
        if first is None:
            super().__init__()
        elif not data:
            data = (first, ) * super()._length_
            super().__init__(*data)
        else:
            data = (first, ) + data
            super().__init__(*data)

        self.__dict__['dtype'] = super()._type_

    def __setattr__(self, key, value):
        try:
            if len(key) == 1:                # Setting a single value.
                self[ATTRIBUTE_MAPPING[key]] = value
            else:
                for i, character in enumerate(key):     # Setting multiple values.
                    self[ATTRIBUTE_MAPPING[character]] = value[i]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + key)

    def __getattr__(self, item):
        try:
            if len(item) > 1:
                return tuple(self[ATTRIBUTE_MAPPING[character]] for character in item)
            else:
                return self[ATTRIBUTE_MAPPING[item]]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + item)

    def __iter__(self):
        return iter(self[:])

    def __repr__(self):
        return '{class_name}({value})'.format(class_name=self.__class__.__name__, value=', '.join(str(x) for x in self))
    
    def __and__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] & other.value, self[1] & other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] & other, self[1] & other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __add__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __lshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] << other.value, self[1] << other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] << other, self[1] << other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __pow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __floordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __xor__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ^ other.value, self[1] ^ other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ^ other, self[1] ^ other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] >> other.value, self[1] >> other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] >> other, self[1] >> other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __or__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] | other.value, self[1] | other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] | other, self[1] | other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __sub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rlshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] << other.value, self[1] << other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] << other, self[1] << other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rand__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] & other.value, self[1] & other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] & other, self[1] & other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __radd__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rxor__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ^ other.value, self[1] ^ other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ^ other, self[1] ^ other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rpow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ror__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] | other.value, self[1] | other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] | other, self[1] | other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rrshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] >> other.value, self[1] >> other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] >> other, self[1] >> other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rsub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rfloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __neg__(self):
        return self.__class__(-self[0], -self[1])
    
    def __pos__(self):
        return self.__class__(+self[0], +self[1])
    
    def __invert__(self):
        return self.__class__(~self[0], ~self[1])
    
    def __lt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] < other.value, self[1] < other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] < other[0], self[1] < other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] < other, self[1] < other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] < other[0], self[1] < other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __le__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] <= other.value, self[1] <= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] <= other[0], self[1] <= other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] <= other, self[1] <= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] <= other[0], self[1] <= other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __eq__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] == other.value, self[1] == other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] == other[0], self[1] == other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] == other, self[1] == other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] == other[0], self[1] == other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ge__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] >= other.value, self[1] >= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] >= other[0], self[1] >= other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] >= other, self[1] >= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] >= other[0], self[1] >= other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ne__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] != other.value, self[1] != other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] != other[0], self[1] != other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] != other, self[1] != other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] != other[0], self[1] != other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __gt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] > other.value, self[1] > other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] > other[0], self[1] > other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] > other, self[1] > other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] > other[0], self[1] > other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
class UVec2(GLuint * 2):

    def __init__(self, first=None, *data):
        if first is None:
            super().__init__()
        elif not data:
            data = (first, ) * super()._length_
            super().__init__(*data)
        else:
            data = (first, ) + data
            super().__init__(*data)

        self.__dict__['dtype'] = super()._type_

    def __setattr__(self, key, value):
        try:
            if len(key) == 1:                # Setting a single value.
                self[ATTRIBUTE_MAPPING[key]] = value
            else:
                for i, character in enumerate(key):     # Setting multiple values.
                    self[ATTRIBUTE_MAPPING[character]] = value[i]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + key)

    def __getattr__(self, item):
        try:
            if len(item) > 1:
                return tuple(self[ATTRIBUTE_MAPPING[character]] for character in item)
            else:
                return self[ATTRIBUTE_MAPPING[item]]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + item)

    def __iter__(self):
        return iter(self[:])

    def __repr__(self):
        return '{class_name}({value})'.format(class_name=self.__class__.__name__, value=', '.join(str(x) for x in self))
    
    def __and__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] & other.value, self[1] & other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] & other, self[1] & other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __add__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __lshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] << other.value, self[1] << other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] << other, self[1] << other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __pow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __floordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __xor__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ^ other.value, self[1] ^ other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ^ other, self[1] ^ other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] >> other.value, self[1] >> other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] >> other, self[1] >> other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __or__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] | other.value, self[1] | other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] | other, self[1] | other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __sub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rlshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] << other.value, self[1] << other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] << other, self[1] << other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rand__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] & other.value, self[1] & other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] & other, self[1] & other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __radd__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rxor__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ^ other.value, self[1] ^ other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ^ other, self[1] ^ other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rpow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ror__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] | other.value, self[1] | other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] | other, self[1] | other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rrshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] >> other.value, self[1] >> other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] >> other, self[1] >> other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rsub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rfloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __neg__(self):
        return self.__class__(-self[0], -self[1])
    
    def __pos__(self):
        return self.__class__(+self[0], +self[1])
    
    def __invert__(self):
        return self.__class__(~self[0], ~self[1])
    
    def __lt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] < other.value, self[1] < other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] < other[0], self[1] < other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] < other, self[1] < other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] < other[0], self[1] < other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __le__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] <= other.value, self[1] <= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] <= other[0], self[1] <= other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] <= other, self[1] <= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] <= other[0], self[1] <= other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __eq__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] == other.value, self[1] == other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] == other[0], self[1] == other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] == other, self[1] == other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] == other[0], self[1] == other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ge__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] >= other.value, self[1] >= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] >= other[0], self[1] >= other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] >= other, self[1] >= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] >= other[0], self[1] >= other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ne__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] != other.value, self[1] != other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] != other[0], self[1] != other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] != other, self[1] != other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] != other[0], self[1] != other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __gt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] > other.value, self[1] > other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] > other[0], self[1] > other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] > other, self[1] > other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] > other[0], self[1] > other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
class IVec2(GLint * 2):

    def __init__(self, first=None, *data):
        if first is None:
            super().__init__()
        elif not data:
            data = (first, ) * super()._length_
            super().__init__(*data)
        else:
            data = (first, ) + data
            super().__init__(*data)

        self.__dict__['dtype'] = super()._type_

    def __setattr__(self, key, value):
        try:
            if len(key) == 1:                # Setting a single value.
                self[ATTRIBUTE_MAPPING[key]] = value
            else:
                for i, character in enumerate(key):     # Setting multiple values.
                    self[ATTRIBUTE_MAPPING[character]] = value[i]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + key)

    def __getattr__(self, item):
        try:
            if len(item) > 1:
                return tuple(self[ATTRIBUTE_MAPPING[character]] for character in item)
            else:
                return self[ATTRIBUTE_MAPPING[item]]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + item)

    def __iter__(self):
        return iter(self[:])

    def __repr__(self):
        return '{class_name}({value})'.format(class_name=self.__class__.__name__, value=', '.join(str(x) for x in self))
    
    def __and__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] & other.value, self[1] & other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] & other, self[1] & other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __add__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __lshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] << other.value, self[1] << other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] << other, self[1] << other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __pow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __floordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __xor__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ^ other.value, self[1] ^ other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ^ other, self[1] ^ other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] >> other.value, self[1] >> other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] >> other, self[1] >> other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __or__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] | other.value, self[1] | other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] | other, self[1] | other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __sub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rlshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] << other.value, self[1] << other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] << other, self[1] << other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rand__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] & other.value, self[1] & other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] & other, self[1] & other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __radd__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rxor__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ^ other.value, self[1] ^ other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ^ other, self[1] ^ other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rpow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ror__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] | other.value, self[1] | other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] | other, self[1] | other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rrshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] >> other.value, self[1] >> other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] >> other, self[1] >> other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rsub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rfloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __neg__(self):
        return self.__class__(-self[0], -self[1])
    
    def __pos__(self):
        return self.__class__(+self[0], +self[1])
    
    def __invert__(self):
        return self.__class__(~self[0], ~self[1])
    
    def __lt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] < other.value, self[1] < other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] < other[0], self[1] < other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] < other, self[1] < other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] < other[0], self[1] < other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __le__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] <= other.value, self[1] <= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] <= other[0], self[1] <= other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] <= other, self[1] <= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] <= other[0], self[1] <= other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __eq__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] == other.value, self[1] == other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] == other[0], self[1] == other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] == other, self[1] == other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] == other[0], self[1] == other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ge__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] >= other.value, self[1] >= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] >= other[0], self[1] >= other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] >= other, self[1] >= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] >= other[0], self[1] >= other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ne__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] != other.value, self[1] != other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] != other[0], self[1] != other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] != other, self[1] != other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] != other[0], self[1] != other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __gt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] > other.value, self[1] > other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] > other[0], self[1] > other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] > other, self[1] > other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] > other[0], self[1] > other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
class Vec2(GLfloat * 2):

    def __init__(self, first=None, *data):
        if first is None:
            super().__init__()
        elif not data:
            data = (first, ) * super()._length_
            super().__init__(*data)
        else:
            data = (first, ) + data
            super().__init__(*data)

        self.__dict__['dtype'] = super()._type_

    def __setattr__(self, key, value):
        try:
            if len(key) == 1:                # Setting a single value.
                self[ATTRIBUTE_MAPPING[key]] = value
            else:
                for i, character in enumerate(key):     # Setting multiple values.
                    self[ATTRIBUTE_MAPPING[character]] = value[i]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + key)

    def __getattr__(self, item):
        try:
            if len(item) > 1:
                return tuple(self[ATTRIBUTE_MAPPING[character]] for character in item)
            else:
                return self[ATTRIBUTE_MAPPING[item]]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + item)
    
    def __iter__(self):
        return iter(self[:])

    def __repr__(self):
        return '{class_name}({value})'.format(class_name=self.__class__.__name__, value=', '.join(str(x) for x in self))
    
    def __add__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __truediv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] / other.value, self[1] / other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] / other[0], self[1] / other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] / other, self[1] / other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] / other[0], self[1] / other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __floordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __pow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __sub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rand__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] & other.value, self[1] & other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] & other, self[1] & other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rxor__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ^ other.value, self[1] ^ other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ^ other, self[1] ^ other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rpow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rsub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rtruediv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] / other.value, self[1] / other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] / other[0], self[1] / other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] / other, self[1] / other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] / other[0], self[1] / other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rlshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] << other.value, self[1] << other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] << other, self[1] << other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __radd__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rrshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] >> other.value, self[1] >> other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] >> other, self[1] >> other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ror__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] | other.value, self[1] | other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] | other, self[1] | other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rfloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __neg__(self):
        return self.__class__(-self[0], -self[1])
    
    def __pos__(self):
        return self.__class__(+self[0], +self[1])
    
    def __lt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] < other.value, self[1] < other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] < other[0], self[1] < other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] < other, self[1] < other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] < other[0], self[1] < other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __le__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] <= other.value, self[1] <= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] <= other[0], self[1] <= other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] <= other, self[1] <= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] <= other[0], self[1] <= other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __eq__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] == other.value, self[1] == other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] == other[0], self[1] == other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] == other, self[1] == other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] == other[0], self[1] == other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ge__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] >= other.value, self[1] >= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] >= other[0], self[1] >= other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] >= other, self[1] >= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] >= other[0], self[1] >= other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ne__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] != other.value, self[1] != other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] != other[0], self[1] != other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] != other, self[1] != other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] != other[0], self[1] != other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __gt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] > other.value, self[1] > other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] > other[0], self[1] > other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] > other, self[1] > other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] > other[0], self[1] > other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
class DVec2(GLdouble * 2):

    def __init__(self, first=None, *data):
        if first is None:
            super().__init__()
        elif not data:
            data = (first, ) * super()._length_
            super().__init__(*data)
        else:
            data = (first, ) + data
            super().__init__(*data)

        self.__dict__['dtype'] = super()._type_

    def __setattr__(self, key, value):
        try:
            if len(key) == 1:                # Setting a single value.
                self[ATTRIBUTE_MAPPING[key]] = value
            else:
                for i, character in enumerate(key):     # Setting multiple values.
                    self[ATTRIBUTE_MAPPING[character]] = value[i]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + key)

    def __getattr__(self, item):
        try:
            if len(item) > 1:
                return tuple(self[ATTRIBUTE_MAPPING[character]] for character in item)
            else:
                return self[ATTRIBUTE_MAPPING[item]]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + item)
    
    def __iter__(self):
        return iter(self[:])

    def __repr__(self):
        return '{class_name}({value})'.format(class_name=self.__class__.__name__, value=', '.join(str(x) for x in self))
    
    def __add__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __truediv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] / other.value, self[1] / other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] / other[0], self[1] / other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] / other, self[1] / other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] / other[0], self[1] / other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __floordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __pow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __sub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rand__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] & other.value, self[1] & other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] & other, self[1] & other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rxor__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ^ other.value, self[1] ^ other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ^ other, self[1] ^ other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rpow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rsub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rtruediv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] / other.value, self[1] / other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] / other[0], self[1] / other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] / other, self[1] / other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] / other[0], self[1] / other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rlshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] << other.value, self[1] << other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] << other, self[1] << other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __radd__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rrshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] >> other.value, self[1] >> other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] >> other, self[1] >> other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ror__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] | other.value, self[1] | other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] | other, self[1] | other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rfloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __neg__(self):
        return self.__class__(-self[0], -self[1])
    
    def __pos__(self):
        return self.__class__(+self[0], +self[1])
    
    def __lt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] < other.value, self[1] < other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] < other[0], self[1] < other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] < other, self[1] < other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] < other[0], self[1] < other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __le__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] <= other.value, self[1] <= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] <= other[0], self[1] <= other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] <= other, self[1] <= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] <= other[0], self[1] <= other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __eq__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] == other.value, self[1] == other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] == other[0], self[1] == other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] == other, self[1] == other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] == other[0], self[1] == other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ge__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] >= other.value, self[1] >= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] >= other[0], self[1] >= other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] >= other, self[1] >= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] >= other[0], self[1] >= other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ne__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] != other.value, self[1] != other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] != other[0], self[1] != other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] != other, self[1] != other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] != other[0], self[1] != other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __gt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec2(self[0] > other.value, self[1] > other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec2(self[0] > other[0], self[1] > other[1])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec2(self[0] > other, self[1] > other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec2(self[0] > other[0], self[1] > other[1])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
class BVec3(GLboolean * 3):

    def __init__(self, first=None, *data):
        if first is None:
            super().__init__()
        elif not data:
            data = (first, ) * super()._length_
            super().__init__(*data)
        else:
            data = (first, ) + data
            super().__init__(*data)

        self.__dict__['dtype'] = super()._type_

    def __setattr__(self, key, value):
        try:
            if len(key) == 1:                # Setting a single value.
                self[ATTRIBUTE_MAPPING[key]] = value
            else:
                for i, character in enumerate(key):     # Setting multiple values.
                    self[ATTRIBUTE_MAPPING[character]] = value[i]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + key)

    def __getattr__(self, item):
        try:
            if len(item) > 1:
                return tuple(self[ATTRIBUTE_MAPPING[character]] for character in item)
            else:
                return self[ATTRIBUTE_MAPPING[item]]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + item)

    def __iter__(self):
        return iter(self[:])

    def __repr__(self):
        return '{class_name}({value})'.format(class_name=self.__class__.__name__, value=', '.join(str(x) for x in self))
    
    def __and__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] & other.value, self[1] & other.value, self[2] & other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] & other, self[1] & other, self[2] & other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __add__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value, self[2] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other, self[2] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __lshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] << other.value, self[1] << other.value, self[2] << other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] << other, self[1] << other, self[2] << other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value, self[2] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other, self[2] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __pow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value, self[2] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other, self[2] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __floordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value, self[2] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other, self[2] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __xor__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ^ other.value, self[1] ^ other.value, self[2] ^ other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ^ other, self[1] ^ other, self[2] ^ other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value, self[2] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other, self[2] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] >> other.value, self[1] >> other.value, self[2] >> other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] >> other, self[1] >> other, self[2] >> other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __or__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] | other.value, self[1] | other.value, self[2] | other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] | other, self[1] | other, self[2] | other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __sub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value, self[2] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other, self[2] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rlshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] << other.value, self[1] << other.value, self[2] << other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] << other, self[1] << other, self[2] << other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rand__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] & other.value, self[1] & other.value, self[2] & other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] & other, self[1] & other, self[2] & other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value, self[2] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other, self[2] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __radd__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value, self[2] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other, self[2] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rxor__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ^ other.value, self[1] ^ other.value, self[2] ^ other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ^ other, self[1] ^ other, self[2] ^ other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value, self[2] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other, self[2] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rpow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value, self[2] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other, self[2] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ror__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] | other.value, self[1] | other.value, self[2] | other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] | other, self[1] | other, self[2] | other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rrshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] >> other.value, self[1] >> other.value, self[2] >> other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] >> other, self[1] >> other, self[2] >> other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rsub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value, self[2] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other, self[2] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rfloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value, self[2] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other, self[2] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __neg__(self):
        return self.__class__(-self[0], -self[1], -self[2])
    
    def __pos__(self):
        return self.__class__(+self[0], +self[1], +self[2])
    
    def __invert__(self):
        return self.__class__(~self[0], ~self[1], ~self[2])
    
    def __lt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] < other.value, self[1] < other.value, self[2] < other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] < other[0], self[1] < other[1], self[2] < other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] < other, self[1] < other, self[2] < other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] < other[0], self[1] < other[1], self[2] < other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __le__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] <= other.value, self[1] <= other.value, self[2] <= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] <= other[0], self[1] <= other[1], self[2] <= other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] <= other, self[1] <= other, self[2] <= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] <= other[0], self[1] <= other[1], self[2] <= other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __eq__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] == other.value, self[1] == other.value, self[2] == other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] == other[0], self[1] == other[1], self[2] == other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] == other, self[1] == other, self[2] == other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] == other[0], self[1] == other[1], self[2] == other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ge__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] >= other.value, self[1] >= other.value, self[2] >= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] >= other[0], self[1] >= other[1], self[2] >= other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] >= other, self[1] >= other, self[2] >= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] >= other[0], self[1] >= other[1], self[2] >= other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ne__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] != other.value, self[1] != other.value, self[2] != other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] != other[0], self[1] != other[1], self[2] != other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] != other, self[1] != other, self[2] != other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] != other[0], self[1] != other[1], self[2] != other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __gt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] > other.value, self[1] > other.value, self[2] > other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] > other[0], self[1] > other[1], self[2] > other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] > other, self[1] > other, self[2] > other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] > other[0], self[1] > other[1], self[2] > other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
class UVec3(GLuint * 3):

    def __init__(self, first=None, *data):
        if first is None:
            super().__init__()
        elif not data:
            data = (first, ) * super()._length_
            super().__init__(*data)
        else:
            data = (first, ) + data
            super().__init__(*data)

        self.__dict__['dtype'] = super()._type_

    def __setattr__(self, key, value):
        try:
            if len(key) == 1:                # Setting a single value.
                self[ATTRIBUTE_MAPPING[key]] = value
            else:
                for i, character in enumerate(key):     # Setting multiple values.
                    self[ATTRIBUTE_MAPPING[character]] = value[i]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + key)

    def __getattr__(self, item):
        try:
            if len(item) > 1:
                return tuple(self[ATTRIBUTE_MAPPING[character]] for character in item)
            else:
                return self[ATTRIBUTE_MAPPING[item]]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + item)

    def __iter__(self):
        return iter(self[:])

    def __repr__(self):
        return '{class_name}({value})'.format(class_name=self.__class__.__name__, value=', '.join(str(x) for x in self))
    
    def __and__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] & other.value, self[1] & other.value, self[2] & other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] & other, self[1] & other, self[2] & other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __add__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value, self[2] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other, self[2] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __lshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] << other.value, self[1] << other.value, self[2] << other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] << other, self[1] << other, self[2] << other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value, self[2] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other, self[2] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __pow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value, self[2] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other, self[2] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __floordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value, self[2] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other, self[2] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __xor__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ^ other.value, self[1] ^ other.value, self[2] ^ other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ^ other, self[1] ^ other, self[2] ^ other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value, self[2] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other, self[2] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] >> other.value, self[1] >> other.value, self[2] >> other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] >> other, self[1] >> other, self[2] >> other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __or__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] | other.value, self[1] | other.value, self[2] | other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] | other, self[1] | other, self[2] | other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __sub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value, self[2] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other, self[2] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rlshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] << other.value, self[1] << other.value, self[2] << other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] << other, self[1] << other, self[2] << other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rand__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] & other.value, self[1] & other.value, self[2] & other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] & other, self[1] & other, self[2] & other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value, self[2] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other, self[2] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __radd__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value, self[2] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other, self[2] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rxor__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ^ other.value, self[1] ^ other.value, self[2] ^ other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ^ other, self[1] ^ other, self[2] ^ other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value, self[2] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other, self[2] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rpow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value, self[2] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other, self[2] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ror__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] | other.value, self[1] | other.value, self[2] | other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] | other, self[1] | other, self[2] | other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rrshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] >> other.value, self[1] >> other.value, self[2] >> other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] >> other, self[1] >> other, self[2] >> other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rsub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value, self[2] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other, self[2] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rfloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value, self[2] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other, self[2] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __neg__(self):
        return self.__class__(-self[0], -self[1], -self[2])
    
    def __pos__(self):
        return self.__class__(+self[0], +self[1], +self[2])
    
    def __invert__(self):
        return self.__class__(~self[0], ~self[1], ~self[2])
    
    def __lt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] < other.value, self[1] < other.value, self[2] < other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] < other[0], self[1] < other[1], self[2] < other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] < other, self[1] < other, self[2] < other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] < other[0], self[1] < other[1], self[2] < other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __le__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] <= other.value, self[1] <= other.value, self[2] <= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] <= other[0], self[1] <= other[1], self[2] <= other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] <= other, self[1] <= other, self[2] <= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] <= other[0], self[1] <= other[1], self[2] <= other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __eq__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] == other.value, self[1] == other.value, self[2] == other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] == other[0], self[1] == other[1], self[2] == other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] == other, self[1] == other, self[2] == other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] == other[0], self[1] == other[1], self[2] == other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ge__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] >= other.value, self[1] >= other.value, self[2] >= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] >= other[0], self[1] >= other[1], self[2] >= other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] >= other, self[1] >= other, self[2] >= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] >= other[0], self[1] >= other[1], self[2] >= other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ne__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] != other.value, self[1] != other.value, self[2] != other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] != other[0], self[1] != other[1], self[2] != other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] != other, self[1] != other, self[2] != other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] != other[0], self[1] != other[1], self[2] != other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __gt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] > other.value, self[1] > other.value, self[2] > other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] > other[0], self[1] > other[1], self[2] > other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] > other, self[1] > other, self[2] > other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] > other[0], self[1] > other[1], self[2] > other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
class IVec3(GLint * 3):

    def __init__(self, first=None, *data):
        if first is None:
            super().__init__()
        elif not data:
            data = (first, ) * super()._length_
            super().__init__(*data)
        else:
            data = (first, ) + data
            super().__init__(*data)

        self.__dict__['dtype'] = super()._type_

    def __setattr__(self, key, value):
        try:
            if len(key) == 1:                # Setting a single value.
                self[ATTRIBUTE_MAPPING[key]] = value
            else:
                for i, character in enumerate(key):     # Setting multiple values.
                    self[ATTRIBUTE_MAPPING[character]] = value[i]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + key)

    def __getattr__(self, item):
        try:
            if len(item) > 1:
                return tuple(self[ATTRIBUTE_MAPPING[character]] for character in item)
            else:
                return self[ATTRIBUTE_MAPPING[item]]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + item)

    def __iter__(self):
        return iter(self[:])

    def __repr__(self):
        return '{class_name}({value})'.format(class_name=self.__class__.__name__, value=', '.join(str(x) for x in self))
    
    def __and__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] & other.value, self[1] & other.value, self[2] & other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] & other, self[1] & other, self[2] & other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __add__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value, self[2] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other, self[2] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __lshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] << other.value, self[1] << other.value, self[2] << other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] << other, self[1] << other, self[2] << other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value, self[2] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other, self[2] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __pow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value, self[2] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other, self[2] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __floordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value, self[2] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other, self[2] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __xor__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ^ other.value, self[1] ^ other.value, self[2] ^ other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ^ other, self[1] ^ other, self[2] ^ other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value, self[2] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other, self[2] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] >> other.value, self[1] >> other.value, self[2] >> other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] >> other, self[1] >> other, self[2] >> other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __or__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] | other.value, self[1] | other.value, self[2] | other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] | other, self[1] | other, self[2] | other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __sub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value, self[2] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other, self[2] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rlshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] << other.value, self[1] << other.value, self[2] << other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] << other, self[1] << other, self[2] << other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rand__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] & other.value, self[1] & other.value, self[2] & other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] & other, self[1] & other, self[2] & other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value, self[2] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other, self[2] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __radd__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value, self[2] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other, self[2] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rxor__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ^ other.value, self[1] ^ other.value, self[2] ^ other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ^ other, self[1] ^ other, self[2] ^ other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value, self[2] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other, self[2] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rpow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value, self[2] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other, self[2] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ror__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] | other.value, self[1] | other.value, self[2] | other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] | other, self[1] | other, self[2] | other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rrshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] >> other.value, self[1] >> other.value, self[2] >> other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] >> other, self[1] >> other, self[2] >> other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rsub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value, self[2] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other, self[2] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rfloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value, self[2] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other, self[2] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __neg__(self):
        return self.__class__(-self[0], -self[1], -self[2])
    
    def __pos__(self):
        return self.__class__(+self[0], +self[1], +self[2])
    
    def __invert__(self):
        return self.__class__(~self[0], ~self[1], ~self[2])
    
    def __lt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] < other.value, self[1] < other.value, self[2] < other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] < other[0], self[1] < other[1], self[2] < other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] < other, self[1] < other, self[2] < other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] < other[0], self[1] < other[1], self[2] < other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __le__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] <= other.value, self[1] <= other.value, self[2] <= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] <= other[0], self[1] <= other[1], self[2] <= other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] <= other, self[1] <= other, self[2] <= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] <= other[0], self[1] <= other[1], self[2] <= other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __eq__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] == other.value, self[1] == other.value, self[2] == other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] == other[0], self[1] == other[1], self[2] == other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] == other, self[1] == other, self[2] == other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] == other[0], self[1] == other[1], self[2] == other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ge__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] >= other.value, self[1] >= other.value, self[2] >= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] >= other[0], self[1] >= other[1], self[2] >= other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] >= other, self[1] >= other, self[2] >= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] >= other[0], self[1] >= other[1], self[2] >= other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ne__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] != other.value, self[1] != other.value, self[2] != other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] != other[0], self[1] != other[1], self[2] != other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] != other, self[1] != other, self[2] != other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] != other[0], self[1] != other[1], self[2] != other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __gt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] > other.value, self[1] > other.value, self[2] > other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] > other[0], self[1] > other[1], self[2] > other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] > other, self[1] > other, self[2] > other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] > other[0], self[1] > other[1], self[2] > other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
class Vec3(GLfloat * 3):

    def __init__(self, first=None, *data):
        if first is None:
            super().__init__()
        elif not data:
            data = (first, ) * super()._length_
            super().__init__(*data)
        else:
            data = (first, ) + data
            super().__init__(*data)

        self.__dict__['dtype'] = super()._type_

    def __setattr__(self, key, value):
        try:
            if len(key) == 1:                # Setting a single value.
                self[ATTRIBUTE_MAPPING[key]] = value
            else:
                for i, character in enumerate(key):     # Setting multiple values.
                    self[ATTRIBUTE_MAPPING[character]] = value[i]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + key)

    def __getattr__(self, item):
        try:
            if len(item) > 1:
                return tuple(self[ATTRIBUTE_MAPPING[character]] for character in item)
            else:
                return self[ATTRIBUTE_MAPPING[item]]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + item)
    
    def __iter__(self):
        return iter(self[:])

    def __repr__(self):
        return '{class_name}({value})'.format(class_name=self.__class__.__name__, value=', '.join(str(x) for x in self))
    
    def __add__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value, self[2] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other, self[2] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value, self[2] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other, self[2] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __truediv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] / other.value, self[1] / other.value, self[2] / other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] / other[0], self[1] / other[1], self[2] / other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] / other, self[1] / other, self[2] / other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] / other[0], self[1] / other[1], self[2] / other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __floordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value, self[2] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other, self[2] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value, self[2] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other, self[2] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __pow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value, self[2] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other, self[2] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __sub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value, self[2] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other, self[2] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rand__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] & other.value, self[1] & other.value, self[2] & other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] & other, self[1] & other, self[2] & other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rxor__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ^ other.value, self[1] ^ other.value, self[2] ^ other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ^ other, self[1] ^ other, self[2] ^ other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value, self[2] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other, self[2] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rpow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value, self[2] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other, self[2] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rsub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value, self[2] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other, self[2] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rtruediv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] / other.value, self[1] / other.value, self[2] / other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] / other[0], self[1] / other[1], self[2] / other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] / other, self[1] / other, self[2] / other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] / other[0], self[1] / other[1], self[2] / other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rlshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] << other.value, self[1] << other.value, self[2] << other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] << other, self[1] << other, self[2] << other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __radd__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value, self[2] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other, self[2] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value, self[2] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other, self[2] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rrshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] >> other.value, self[1] >> other.value, self[2] >> other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] >> other, self[1] >> other, self[2] >> other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ror__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] | other.value, self[1] | other.value, self[2] | other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] | other, self[1] | other, self[2] | other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rfloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value, self[2] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other, self[2] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __neg__(self):
        return self.__class__(-self[0], -self[1], -self[2])
    
    def __pos__(self):
        return self.__class__(+self[0], +self[1], +self[2])
    
    def __lt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] < other.value, self[1] < other.value, self[2] < other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] < other[0], self[1] < other[1], self[2] < other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] < other, self[1] < other, self[2] < other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] < other[0], self[1] < other[1], self[2] < other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __le__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] <= other.value, self[1] <= other.value, self[2] <= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] <= other[0], self[1] <= other[1], self[2] <= other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] <= other, self[1] <= other, self[2] <= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] <= other[0], self[1] <= other[1], self[2] <= other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __eq__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] == other.value, self[1] == other.value, self[2] == other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] == other[0], self[1] == other[1], self[2] == other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] == other, self[1] == other, self[2] == other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] == other[0], self[1] == other[1], self[2] == other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ge__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] >= other.value, self[1] >= other.value, self[2] >= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] >= other[0], self[1] >= other[1], self[2] >= other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] >= other, self[1] >= other, self[2] >= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] >= other[0], self[1] >= other[1], self[2] >= other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ne__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] != other.value, self[1] != other.value, self[2] != other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] != other[0], self[1] != other[1], self[2] != other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] != other, self[1] != other, self[2] != other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] != other[0], self[1] != other[1], self[2] != other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __gt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] > other.value, self[1] > other.value, self[2] > other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] > other[0], self[1] > other[1], self[2] > other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] > other, self[1] > other, self[2] > other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] > other[0], self[1] > other[1], self[2] > other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
class DVec3(GLdouble * 3):

    def __init__(self, first=None, *data):
        if first is None:
            super().__init__()
        elif not data:
            data = (first, ) * super()._length_
            super().__init__(*data)
        else:
            data = (first, ) + data
            super().__init__(*data)

        self.__dict__['dtype'] = super()._type_

    def __setattr__(self, key, value):
        try:
            if len(key) == 1:                # Setting a single value.
                self[ATTRIBUTE_MAPPING[key]] = value
            else:
                for i, character in enumerate(key):     # Setting multiple values.
                    self[ATTRIBUTE_MAPPING[character]] = value[i]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + key)

    def __getattr__(self, item):
        try:
            if len(item) > 1:
                return tuple(self[ATTRIBUTE_MAPPING[character]] for character in item)
            else:
                return self[ATTRIBUTE_MAPPING[item]]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + item)
    
    def __iter__(self):
        return iter(self[:])

    def __repr__(self):
        return '{class_name}({value})'.format(class_name=self.__class__.__name__, value=', '.join(str(x) for x in self))
    
    def __add__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value, self[2] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other, self[2] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value, self[2] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other, self[2] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __truediv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] / other.value, self[1] / other.value, self[2] / other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] / other[0], self[1] / other[1], self[2] / other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] / other, self[1] / other, self[2] / other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] / other[0], self[1] / other[1], self[2] / other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __floordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value, self[2] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other, self[2] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value, self[2] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other, self[2] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __pow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value, self[2] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other, self[2] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __sub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value, self[2] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other, self[2] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rand__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] & other.value, self[1] & other.value, self[2] & other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] & other, self[1] & other, self[2] & other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rxor__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ^ other.value, self[1] ^ other.value, self[2] ^ other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ^ other, self[1] ^ other, self[2] ^ other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value, self[2] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other, self[2] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rpow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value, self[2] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other, self[2] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rsub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value, self[2] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other, self[2] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rtruediv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] / other.value, self[1] / other.value, self[2] / other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] / other[0], self[1] / other[1], self[2] / other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] / other, self[1] / other, self[2] / other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] / other[0], self[1] / other[1], self[2] / other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rlshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] << other.value, self[1] << other.value, self[2] << other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] << other, self[1] << other, self[2] << other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __radd__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value, self[2] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other, self[2] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value, self[2] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other, self[2] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rrshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] >> other.value, self[1] >> other.value, self[2] >> other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] >> other, self[1] >> other, self[2] >> other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ror__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] | other.value, self[1] | other.value, self[2] | other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] | other, self[1] | other, self[2] | other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rfloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value, self[2] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other, self[2] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __neg__(self):
        return self.__class__(-self[0], -self[1], -self[2])
    
    def __pos__(self):
        return self.__class__(+self[0], +self[1], +self[2])
    
    def __lt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] < other.value, self[1] < other.value, self[2] < other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] < other[0], self[1] < other[1], self[2] < other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] < other, self[1] < other, self[2] < other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] < other[0], self[1] < other[1], self[2] < other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __le__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] <= other.value, self[1] <= other.value, self[2] <= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] <= other[0], self[1] <= other[1], self[2] <= other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] <= other, self[1] <= other, self[2] <= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] <= other[0], self[1] <= other[1], self[2] <= other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __eq__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] == other.value, self[1] == other.value, self[2] == other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] == other[0], self[1] == other[1], self[2] == other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] == other, self[1] == other, self[2] == other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] == other[0], self[1] == other[1], self[2] == other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ge__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] >= other.value, self[1] >= other.value, self[2] >= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] >= other[0], self[1] >= other[1], self[2] >= other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] >= other, self[1] >= other, self[2] >= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] >= other[0], self[1] >= other[1], self[2] >= other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ne__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] != other.value, self[1] != other.value, self[2] != other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] != other[0], self[1] != other[1], self[2] != other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] != other, self[1] != other, self[2] != other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] != other[0], self[1] != other[1], self[2] != other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __gt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec3(self[0] > other.value, self[1] > other.value, self[2] > other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec3(self[0] > other[0], self[1] > other[1], self[2] > other[2])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec3(self[0] > other, self[1] > other, self[2] > other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec3(self[0] > other[0], self[1] > other[1], self[2] > other[2])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
class BVec4(GLboolean * 4):

    def __init__(self, first=None, *data):
        if first is None:
            super().__init__()
        elif not data:
            data = (first, ) * super()._length_
            super().__init__(*data)
        else:
            data = (first, ) + data
            super().__init__(*data)

        self.__dict__['dtype'] = super()._type_

    def __setattr__(self, key, value):
        try:
            if len(key) == 1:                # Setting a single value.
                self[ATTRIBUTE_MAPPING[key]] = value
            else:
                for i, character in enumerate(key):     # Setting multiple values.
                    self[ATTRIBUTE_MAPPING[character]] = value[i]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + key)

    def __getattr__(self, item):
        try:
            if len(item) > 1:
                return tuple(self[ATTRIBUTE_MAPPING[character]] for character in item)
            else:
                return self[ATTRIBUTE_MAPPING[item]]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + item)

    def __iter__(self):
        return iter(self[:])

    def __repr__(self):
        return '{class_name}({value})'.format(class_name=self.__class__.__name__, value=', '.join(str(x) for x in self))
    
    def __and__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] & other.value, self[1] & other.value, self[2] & other.value, self[3] & other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2], self[3] & other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] & other, self[1] & other, self[2] & other, self[3] & other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2], self[3] & other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __add__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value, self[2] + other.value, self[3] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other, self[2] + other, self[3] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __lshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] << other.value, self[1] << other.value, self[2] << other.value, self[3] << other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2], self[3] << other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] << other, self[1] << other, self[2] << other, self[3] << other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2], self[3] << other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value, self[2] % other.value, self[3] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2], self[3] % other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other, self[2] % other, self[3] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2], self[3] % other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __pow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value, self[2] ** other.value, self[3] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2], self[3] ** other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other, self[2] ** other, self[3] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2], self[3] ** other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __floordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value, self[2] // other.value, self[3] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2], self[3] // other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other, self[2] // other, self[3] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2], self[3] // other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __xor__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ^ other.value, self[1] ^ other.value, self[2] ^ other.value, self[3] ^ other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2], self[3] ^ other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ^ other, self[1] ^ other, self[2] ^ other, self[3] ^ other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2], self[3] ^ other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value, self[2] * other.value, self[3] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2], self[3] * other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other, self[2] * other, self[3] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2], self[3] * other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] >> other.value, self[1] >> other.value, self[2] >> other.value, self[3] >> other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2], self[3] >> other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] >> other, self[1] >> other, self[2] >> other, self[3] >> other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2], self[3] >> other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __or__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] | other.value, self[1] | other.value, self[2] | other.value, self[3] | other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2], self[3] | other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] | other, self[1] | other, self[2] | other, self[3] | other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2], self[3] | other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __sub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value, self[2] - other.value, self[3] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other, self[2] - other, self[3] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rlshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] << other.value, self[1] << other.value, self[2] << other.value, self[3] << other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2], self[3] << other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] << other, self[1] << other, self[2] << other, self[3] << other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2], self[3] << other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rand__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] & other.value, self[1] & other.value, self[2] & other.value, self[3] & other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2], self[3] & other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] & other, self[1] & other, self[2] & other, self[3] & other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2], self[3] & other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value, self[2] * other.value, self[3] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2], self[3] * other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other, self[2] * other, self[3] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2], self[3] * other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __radd__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value, self[2] + other.value, self[3] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other, self[2] + other, self[3] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rxor__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ^ other.value, self[1] ^ other.value, self[2] ^ other.value, self[3] ^ other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2], self[3] ^ other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ^ other, self[1] ^ other, self[2] ^ other, self[3] ^ other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2], self[3] ^ other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value, self[2] % other.value, self[3] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2], self[3] % other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other, self[2] % other, self[3] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2], self[3] % other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rpow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value, self[2] ** other.value, self[3] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2], self[3] ** other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other, self[2] ** other, self[3] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2], self[3] ** other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ror__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] | other.value, self[1] | other.value, self[2] | other.value, self[3] | other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2], self[3] | other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] | other, self[1] | other, self[2] | other, self[3] | other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2], self[3] | other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rrshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] >> other.value, self[1] >> other.value, self[2] >> other.value, self[3] >> other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2], self[3] >> other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] >> other, self[1] >> other, self[2] >> other, self[3] >> other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2], self[3] >> other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rsub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value, self[2] - other.value, self[3] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other, self[2] - other, self[3] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rfloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value, self[2] // other.value, self[3] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2], self[3] // other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other, self[2] // other, self[3] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2], self[3] // other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __neg__(self):
        return self.__class__(-self[0], -self[1], -self[2], -self[3])
    
    def __pos__(self):
        return self.__class__(+self[0], +self[1], +self[2], +self[3])
    
    def __invert__(self):
        return self.__class__(~self[0], ~self[1], ~self[2], ~self[3])
    
    def __lt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] < other.value, self[1] < other.value, self[2] < other.value, self[3] < other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] < other[0], self[1] < other[1], self[2] < other[2], self[3] < other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] < other, self[1] < other, self[2] < other, self[3] < other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] < other[0], self[1] < other[1], self[2] < other[2], self[3] < other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __le__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] <= other.value, self[1] <= other.value, self[2] <= other.value, self[3] <= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] <= other[0], self[1] <= other[1], self[2] <= other[2], self[3] <= other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] <= other, self[1] <= other, self[2] <= other, self[3] <= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] <= other[0], self[1] <= other[1], self[2] <= other[2], self[3] <= other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __eq__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] == other.value, self[1] == other.value, self[2] == other.value, self[3] == other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] == other[0], self[1] == other[1], self[2] == other[2], self[3] == other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] == other, self[1] == other, self[2] == other, self[3] == other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] == other[0], self[1] == other[1], self[2] == other[2], self[3] == other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ge__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] >= other.value, self[1] >= other.value, self[2] >= other.value, self[3] >= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] >= other[0], self[1] >= other[1], self[2] >= other[2], self[3] >= other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] >= other, self[1] >= other, self[2] >= other, self[3] >= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] >= other[0], self[1] >= other[1], self[2] >= other[2], self[3] >= other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ne__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] != other.value, self[1] != other.value, self[2] != other.value, self[3] != other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] != other[0], self[1] != other[1], self[2] != other[2], self[3] != other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] != other, self[1] != other, self[2] != other, self[3] != other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] != other[0], self[1] != other[1], self[2] != other[2], self[3] != other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __gt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] > other.value, self[1] > other.value, self[2] > other.value, self[3] > other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] > other[0], self[1] > other[1], self[2] > other[2], self[3] > other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] > other, self[1] > other, self[2] > other, self[3] > other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] > other[0], self[1] > other[1], self[2] > other[2], self[3] > other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
class UVec4(GLuint * 4):

    def __init__(self, first=None, *data):
        if first is None:
            super().__init__()
        elif not data:
            data = (first, ) * super()._length_
            super().__init__(*data)
        else:
            data = (first, ) + data
            super().__init__(*data)

        self.__dict__['dtype'] = super()._type_

    def __setattr__(self, key, value):
        try:
            if len(key) == 1:                # Setting a single value.
                self[ATTRIBUTE_MAPPING[key]] = value
            else:
                for i, character in enumerate(key):     # Setting multiple values.
                    self[ATTRIBUTE_MAPPING[character]] = value[i]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + key)

    def __getattr__(self, item):
        try:
            if len(item) > 1:
                return tuple(self[ATTRIBUTE_MAPPING[character]] for character in item)
            else:
                return self[ATTRIBUTE_MAPPING[item]]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + item)

    def __iter__(self):
        return iter(self[:])

    def __repr__(self):
        return '{class_name}({value})'.format(class_name=self.__class__.__name__, value=', '.join(str(x) for x in self))
    
    def __and__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] & other.value, self[1] & other.value, self[2] & other.value, self[3] & other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2], self[3] & other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] & other, self[1] & other, self[2] & other, self[3] & other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2], self[3] & other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __add__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value, self[2] + other.value, self[3] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other, self[2] + other, self[3] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __lshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] << other.value, self[1] << other.value, self[2] << other.value, self[3] << other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2], self[3] << other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] << other, self[1] << other, self[2] << other, self[3] << other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2], self[3] << other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value, self[2] % other.value, self[3] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2], self[3] % other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other, self[2] % other, self[3] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2], self[3] % other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __pow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value, self[2] ** other.value, self[3] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2], self[3] ** other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other, self[2] ** other, self[3] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2], self[3] ** other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __floordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value, self[2] // other.value, self[3] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2], self[3] // other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other, self[2] // other, self[3] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2], self[3] // other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __xor__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ^ other.value, self[1] ^ other.value, self[2] ^ other.value, self[3] ^ other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2], self[3] ^ other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ^ other, self[1] ^ other, self[2] ^ other, self[3] ^ other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2], self[3] ^ other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value, self[2] * other.value, self[3] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2], self[3] * other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other, self[2] * other, self[3] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2], self[3] * other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] >> other.value, self[1] >> other.value, self[2] >> other.value, self[3] >> other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2], self[3] >> other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] >> other, self[1] >> other, self[2] >> other, self[3] >> other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2], self[3] >> other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __or__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] | other.value, self[1] | other.value, self[2] | other.value, self[3] | other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2], self[3] | other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] | other, self[1] | other, self[2] | other, self[3] | other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2], self[3] | other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __sub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value, self[2] - other.value, self[3] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other, self[2] - other, self[3] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rlshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] << other.value, self[1] << other.value, self[2] << other.value, self[3] << other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2], self[3] << other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] << other, self[1] << other, self[2] << other, self[3] << other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2], self[3] << other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rand__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] & other.value, self[1] & other.value, self[2] & other.value, self[3] & other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2], self[3] & other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] & other, self[1] & other, self[2] & other, self[3] & other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2], self[3] & other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value, self[2] * other.value, self[3] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2], self[3] * other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other, self[2] * other, self[3] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2], self[3] * other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __radd__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value, self[2] + other.value, self[3] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other, self[2] + other, self[3] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rxor__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ^ other.value, self[1] ^ other.value, self[2] ^ other.value, self[3] ^ other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2], self[3] ^ other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ^ other, self[1] ^ other, self[2] ^ other, self[3] ^ other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2], self[3] ^ other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value, self[2] % other.value, self[3] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2], self[3] % other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other, self[2] % other, self[3] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2], self[3] % other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rpow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value, self[2] ** other.value, self[3] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2], self[3] ** other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other, self[2] ** other, self[3] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2], self[3] ** other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ror__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] | other.value, self[1] | other.value, self[2] | other.value, self[3] | other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2], self[3] | other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] | other, self[1] | other, self[2] | other, self[3] | other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2], self[3] | other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rrshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] >> other.value, self[1] >> other.value, self[2] >> other.value, self[3] >> other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2], self[3] >> other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] >> other, self[1] >> other, self[2] >> other, self[3] >> other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2], self[3] >> other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rsub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value, self[2] - other.value, self[3] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other, self[2] - other, self[3] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rfloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value, self[2] // other.value, self[3] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2], self[3] // other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other, self[2] // other, self[3] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2], self[3] // other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __neg__(self):
        return self.__class__(-self[0], -self[1], -self[2], -self[3])
    
    def __pos__(self):
        return self.__class__(+self[0], +self[1], +self[2], +self[3])
    
    def __invert__(self):
        return self.__class__(~self[0], ~self[1], ~self[2], ~self[3])
    
    def __lt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] < other.value, self[1] < other.value, self[2] < other.value, self[3] < other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] < other[0], self[1] < other[1], self[2] < other[2], self[3] < other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] < other, self[1] < other, self[2] < other, self[3] < other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] < other[0], self[1] < other[1], self[2] < other[2], self[3] < other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __le__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] <= other.value, self[1] <= other.value, self[2] <= other.value, self[3] <= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] <= other[0], self[1] <= other[1], self[2] <= other[2], self[3] <= other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] <= other, self[1] <= other, self[2] <= other, self[3] <= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] <= other[0], self[1] <= other[1], self[2] <= other[2], self[3] <= other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __eq__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] == other.value, self[1] == other.value, self[2] == other.value, self[3] == other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] == other[0], self[1] == other[1], self[2] == other[2], self[3] == other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] == other, self[1] == other, self[2] == other, self[3] == other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] == other[0], self[1] == other[1], self[2] == other[2], self[3] == other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ge__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] >= other.value, self[1] >= other.value, self[2] >= other.value, self[3] >= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] >= other[0], self[1] >= other[1], self[2] >= other[2], self[3] >= other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] >= other, self[1] >= other, self[2] >= other, self[3] >= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] >= other[0], self[1] >= other[1], self[2] >= other[2], self[3] >= other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ne__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] != other.value, self[1] != other.value, self[2] != other.value, self[3] != other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] != other[0], self[1] != other[1], self[2] != other[2], self[3] != other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] != other, self[1] != other, self[2] != other, self[3] != other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] != other[0], self[1] != other[1], self[2] != other[2], self[3] != other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __gt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] > other.value, self[1] > other.value, self[2] > other.value, self[3] > other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] > other[0], self[1] > other[1], self[2] > other[2], self[3] > other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] > other, self[1] > other, self[2] > other, self[3] > other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] > other[0], self[1] > other[1], self[2] > other[2], self[3] > other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
class IVec4(GLint * 4):

    def __init__(self, first=None, *data):
        if first is None:
            super().__init__()
        elif not data:
            data = (first, ) * super()._length_
            super().__init__(*data)
        else:
            data = (first, ) + data
            super().__init__(*data)

        self.__dict__['dtype'] = super()._type_

    def __setattr__(self, key, value):
        try:
            if len(key) == 1:                # Setting a single value.
                self[ATTRIBUTE_MAPPING[key]] = value
            else:
                for i, character in enumerate(key):     # Setting multiple values.
                    self[ATTRIBUTE_MAPPING[character]] = value[i]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + key)

    def __getattr__(self, item):
        try:
            if len(item) > 1:
                return tuple(self[ATTRIBUTE_MAPPING[character]] for character in item)
            else:
                return self[ATTRIBUTE_MAPPING[item]]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + item)

    def __iter__(self):
        return iter(self[:])

    def __repr__(self):
        return '{class_name}({value})'.format(class_name=self.__class__.__name__, value=', '.join(str(x) for x in self))
    
    def __and__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] & other.value, self[1] & other.value, self[2] & other.value, self[3] & other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2], self[3] & other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] & other, self[1] & other, self[2] & other, self[3] & other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2], self[3] & other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __add__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value, self[2] + other.value, self[3] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other, self[2] + other, self[3] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __lshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] << other.value, self[1] << other.value, self[2] << other.value, self[3] << other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2], self[3] << other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] << other, self[1] << other, self[2] << other, self[3] << other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2], self[3] << other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value, self[2] % other.value, self[3] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2], self[3] % other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other, self[2] % other, self[3] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2], self[3] % other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __pow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value, self[2] ** other.value, self[3] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2], self[3] ** other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other, self[2] ** other, self[3] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2], self[3] ** other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __floordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value, self[2] // other.value, self[3] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2], self[3] // other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other, self[2] // other, self[3] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2], self[3] // other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __xor__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ^ other.value, self[1] ^ other.value, self[2] ^ other.value, self[3] ^ other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2], self[3] ^ other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ^ other, self[1] ^ other, self[2] ^ other, self[3] ^ other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2], self[3] ^ other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value, self[2] * other.value, self[3] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2], self[3] * other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other, self[2] * other, self[3] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2], self[3] * other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] >> other.value, self[1] >> other.value, self[2] >> other.value, self[3] >> other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2], self[3] >> other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] >> other, self[1] >> other, self[2] >> other, self[3] >> other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2], self[3] >> other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __or__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] | other.value, self[1] | other.value, self[2] | other.value, self[3] | other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2], self[3] | other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] | other, self[1] | other, self[2] | other, self[3] | other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2], self[3] | other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __sub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value, self[2] - other.value, self[3] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other, self[2] - other, self[3] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rlshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] << other.value, self[1] << other.value, self[2] << other.value, self[3] << other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2], self[3] << other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] << other, self[1] << other, self[2] << other, self[3] << other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2], self[3] << other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rand__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] & other.value, self[1] & other.value, self[2] & other.value, self[3] & other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2], self[3] & other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] & other, self[1] & other, self[2] & other, self[3] & other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2], self[3] & other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value, self[2] * other.value, self[3] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2], self[3] * other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other, self[2] * other, self[3] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2], self[3] * other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __radd__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value, self[2] + other.value, self[3] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other, self[2] + other, self[3] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rxor__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ^ other.value, self[1] ^ other.value, self[2] ^ other.value, self[3] ^ other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2], self[3] ^ other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ^ other, self[1] ^ other, self[2] ^ other, self[3] ^ other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2], self[3] ^ other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value, self[2] % other.value, self[3] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2], self[3] % other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other, self[2] % other, self[3] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2], self[3] % other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rpow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value, self[2] ** other.value, self[3] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2], self[3] ** other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other, self[2] ** other, self[3] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2], self[3] ** other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ror__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] | other.value, self[1] | other.value, self[2] | other.value, self[3] | other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2], self[3] | other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] | other, self[1] | other, self[2] | other, self[3] | other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2], self[3] | other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rrshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] >> other.value, self[1] >> other.value, self[2] >> other.value, self[3] >> other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2], self[3] >> other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] >> other, self[1] >> other, self[2] >> other, self[3] >> other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2], self[3] >> other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rsub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value, self[2] - other.value, self[3] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other, self[2] - other, self[3] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rfloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value, self[2] // other.value, self[3] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2], self[3] // other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other, self[2] // other, self[3] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2], self[3] // other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __neg__(self):
        return self.__class__(-self[0], -self[1], -self[2], -self[3])
    
    def __pos__(self):
        return self.__class__(+self[0], +self[1], +self[2], +self[3])
    
    def __invert__(self):
        return self.__class__(~self[0], ~self[1], ~self[2], ~self[3])
    
    def __lt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] < other.value, self[1] < other.value, self[2] < other.value, self[3] < other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] < other[0], self[1] < other[1], self[2] < other[2], self[3] < other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] < other, self[1] < other, self[2] < other, self[3] < other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] < other[0], self[1] < other[1], self[2] < other[2], self[3] < other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __le__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] <= other.value, self[1] <= other.value, self[2] <= other.value, self[3] <= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] <= other[0], self[1] <= other[1], self[2] <= other[2], self[3] <= other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] <= other, self[1] <= other, self[2] <= other, self[3] <= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] <= other[0], self[1] <= other[1], self[2] <= other[2], self[3] <= other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __eq__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] == other.value, self[1] == other.value, self[2] == other.value, self[3] == other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] == other[0], self[1] == other[1], self[2] == other[2], self[3] == other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] == other, self[1] == other, self[2] == other, self[3] == other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] == other[0], self[1] == other[1], self[2] == other[2], self[3] == other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ge__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] >= other.value, self[1] >= other.value, self[2] >= other.value, self[3] >= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] >= other[0], self[1] >= other[1], self[2] >= other[2], self[3] >= other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] >= other, self[1] >= other, self[2] >= other, self[3] >= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] >= other[0], self[1] >= other[1], self[2] >= other[2], self[3] >= other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ne__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] != other.value, self[1] != other.value, self[2] != other.value, self[3] != other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] != other[0], self[1] != other[1], self[2] != other[2], self[3] != other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] != other, self[1] != other, self[2] != other, self[3] != other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] != other[0], self[1] != other[1], self[2] != other[2], self[3] != other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __gt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] > other.value, self[1] > other.value, self[2] > other.value, self[3] > other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] > other[0], self[1] > other[1], self[2] > other[2], self[3] > other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] > other, self[1] > other, self[2] > other, self[3] > other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] > other[0], self[1] > other[1], self[2] > other[2], self[3] > other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
class Vec4(GLfloat * 4):

    def __init__(self, first=None, *data):
        if first is None:
            super().__init__()
        elif not data:
            data = (first, ) * super()._length_
            super().__init__(*data)
        else:
            data = (first, ) + data
            super().__init__(*data)

        self.__dict__['dtype'] = super()._type_

    def __setattr__(self, key, value):
        try:
            if len(key) == 1:                # Setting a single value.
                self[ATTRIBUTE_MAPPING[key]] = value
            else:
                for i, character in enumerate(key):     # Setting multiple values.
                    self[ATTRIBUTE_MAPPING[character]] = value[i]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + key)

    def __getattr__(self, item):
        try:
            if len(item) > 1:
                return tuple(self[ATTRIBUTE_MAPPING[character]] for character in item)
            else:
                return self[ATTRIBUTE_MAPPING[item]]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + item)
    
    def __iter__(self):
        return iter(self[:])

    def __repr__(self):
        return '{class_name}({value})'.format(class_name=self.__class__.__name__, value=', '.join(str(x) for x in self))
    
    def __add__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value, self[2] + other.value, self[3] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other, self[2] + other, self[3] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value, self[2] % other.value, self[3] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2], self[3] % other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other, self[2] % other, self[3] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2], self[3] % other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __truediv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] / other.value, self[1] / other.value, self[2] / other.value, self[3] / other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] / other[0], self[1] / other[1], self[2] / other[2], self[3] / other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] / other, self[1] / other, self[2] / other, self[3] / other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] / other[0], self[1] / other[1], self[2] / other[2], self[3] / other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __floordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value, self[2] // other.value, self[3] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2], self[3] // other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other, self[2] // other, self[3] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2], self[3] // other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value, self[2] * other.value, self[3] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2], self[3] * other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other, self[2] * other, self[3] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2], self[3] * other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __pow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value, self[2] ** other.value, self[3] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2], self[3] ** other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other, self[2] ** other, self[3] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2], self[3] ** other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __sub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value, self[2] - other.value, self[3] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other, self[2] - other, self[3] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rand__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] & other.value, self[1] & other.value, self[2] & other.value, self[3] & other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2], self[3] & other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] & other, self[1] & other, self[2] & other, self[3] & other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2], self[3] & other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rxor__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ^ other.value, self[1] ^ other.value, self[2] ^ other.value, self[3] ^ other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2], self[3] ^ other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ^ other, self[1] ^ other, self[2] ^ other, self[3] ^ other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2], self[3] ^ other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value, self[2] % other.value, self[3] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2], self[3] % other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other, self[2] % other, self[3] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2], self[3] % other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rpow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value, self[2] ** other.value, self[3] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2], self[3] ** other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other, self[2] ** other, self[3] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2], self[3] ** other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rsub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value, self[2] - other.value, self[3] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other, self[2] - other, self[3] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rtruediv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] / other.value, self[1] / other.value, self[2] / other.value, self[3] / other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] / other[0], self[1] / other[1], self[2] / other[2], self[3] / other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] / other, self[1] / other, self[2] / other, self[3] / other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] / other[0], self[1] / other[1], self[2] / other[2], self[3] / other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rlshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] << other.value, self[1] << other.value, self[2] << other.value, self[3] << other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2], self[3] << other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] << other, self[1] << other, self[2] << other, self[3] << other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2], self[3] << other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __radd__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value, self[2] + other.value, self[3] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other, self[2] + other, self[3] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value, self[2] * other.value, self[3] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2], self[3] * other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other, self[2] * other, self[3] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2], self[3] * other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rrshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] >> other.value, self[1] >> other.value, self[2] >> other.value, self[3] >> other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2], self[3] >> other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] >> other, self[1] >> other, self[2] >> other, self[3] >> other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2], self[3] >> other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ror__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] | other.value, self[1] | other.value, self[2] | other.value, self[3] | other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2], self[3] | other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] | other, self[1] | other, self[2] | other, self[3] | other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2], self[3] | other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rfloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value, self[2] // other.value, self[3] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2], self[3] // other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other, self[2] // other, self[3] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2], self[3] // other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __neg__(self):
        return self.__class__(-self[0], -self[1], -self[2], -self[3])
    
    def __pos__(self):
        return self.__class__(+self[0], +self[1], +self[2], +self[3])
    
    def __lt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] < other.value, self[1] < other.value, self[2] < other.value, self[3] < other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] < other[0], self[1] < other[1], self[2] < other[2], self[3] < other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] < other, self[1] < other, self[2] < other, self[3] < other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] < other[0], self[1] < other[1], self[2] < other[2], self[3] < other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __le__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] <= other.value, self[1] <= other.value, self[2] <= other.value, self[3] <= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] <= other[0], self[1] <= other[1], self[2] <= other[2], self[3] <= other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] <= other, self[1] <= other, self[2] <= other, self[3] <= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] <= other[0], self[1] <= other[1], self[2] <= other[2], self[3] <= other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __eq__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] == other.value, self[1] == other.value, self[2] == other.value, self[3] == other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] == other[0], self[1] == other[1], self[2] == other[2], self[3] == other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] == other, self[1] == other, self[2] == other, self[3] == other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] == other[0], self[1] == other[1], self[2] == other[2], self[3] == other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ge__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] >= other.value, self[1] >= other.value, self[2] >= other.value, self[3] >= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] >= other[0], self[1] >= other[1], self[2] >= other[2], self[3] >= other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] >= other, self[1] >= other, self[2] >= other, self[3] >= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] >= other[0], self[1] >= other[1], self[2] >= other[2], self[3] >= other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ne__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] != other.value, self[1] != other.value, self[2] != other.value, self[3] != other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] != other[0], self[1] != other[1], self[2] != other[2], self[3] != other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] != other, self[1] != other, self[2] != other, self[3] != other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] != other[0], self[1] != other[1], self[2] != other[2], self[3] != other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __gt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] > other.value, self[1] > other.value, self[2] > other.value, self[3] > other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] > other[0], self[1] > other[1], self[2] > other[2], self[3] > other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] > other, self[1] > other, self[2] > other, self[3] > other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] > other[0], self[1] > other[1], self[2] > other[2], self[3] > other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
class DVec4(GLdouble * 4):

    def __init__(self, first=None, *data):
        if first is None:
            super().__init__()
        elif not data:
            data = (first, ) * super()._length_
            super().__init__(*data)
        else:
            data = (first, ) + data
            super().__init__(*data)

        self.__dict__['dtype'] = super()._type_

    def __setattr__(self, key, value):
        try:
            if len(key) == 1:                # Setting a single value.
                self[ATTRIBUTE_MAPPING[key]] = value
            else:
                for i, character in enumerate(key):     # Setting multiple values.
                    self[ATTRIBUTE_MAPPING[character]] = value[i]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + key)

    def __getattr__(self, item):
        try:
            if len(item) > 1:
                return tuple(self[ATTRIBUTE_MAPPING[character]] for character in item)
            else:
                return self[ATTRIBUTE_MAPPING[item]]
        except (KeyError, IndexError):
            raise AttributeError(self.__class__.__name__ + ' has no attribute ' + item)
    
    def __iter__(self):
        return iter(self[:])

    def __repr__(self):
        return '{class_name}({value})'.format(class_name=self.__class__.__name__, value=', '.join(str(x) for x in self))
    
    def __add__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value, self[2] + other.value, self[3] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other, self[2] + other, self[3] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value, self[2] % other.value, self[3] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2], self[3] % other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other, self[2] % other, self[3] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2], self[3] % other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __truediv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] / other.value, self[1] / other.value, self[2] / other.value, self[3] / other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] / other[0], self[1] / other[1], self[2] / other[2], self[3] / other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] / other, self[1] / other, self[2] / other, self[3] / other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] / other[0], self[1] / other[1], self[2] / other[2], self[3] / other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __floordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value, self[2] // other.value, self[3] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2], self[3] // other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other, self[2] // other, self[3] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2], self[3] // other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __mul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value, self[2] * other.value, self[3] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2], self[3] * other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other, self[2] * other, self[3] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2], self[3] * other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __pow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value, self[2] ** other.value, self[3] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2], self[3] ** other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other, self[2] ** other, self[3] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2], self[3] ** other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __sub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value, self[2] - other.value, self[3] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other, self[2] - other, self[3] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rand__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] & other.value, self[1] & other.value, self[2] & other.value, self[3] & other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2], self[3] & other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] & other, self[1] & other, self[2] & other, self[3] & other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] & other[0], self[1] & other[1], self[2] & other[2], self[3] & other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rxor__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ^ other.value, self[1] ^ other.value, self[2] ^ other.value, self[3] ^ other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2], self[3] ^ other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ^ other, self[1] ^ other, self[2] ^ other, self[3] ^ other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ^ other[0], self[1] ^ other[1], self[2] ^ other[2], self[3] ^ other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmod__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] % other.value, self[1] % other.value, self[2] % other.value, self[3] % other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2], self[3] % other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] % other, self[1] % other, self[2] % other, self[3] % other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] % other[0], self[1] % other[1], self[2] % other[2], self[3] % other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rpow__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] ** other.value, self[1] ** other.value, self[2] ** other.value, self[3] ** other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2], self[3] ** other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] ** other, self[1] ** other, self[2] ** other, self[3] ** other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] ** other[0], self[1] ** other[1], self[2] ** other[2], self[3] ** other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rsub__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] - other.value, self[1] - other.value, self[2] - other.value, self[3] - other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] - other, self[1] - other, self[2] - other, self[3] - other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rtruediv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] / other.value, self[1] / other.value, self[2] / other.value, self[3] / other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] / other[0], self[1] / other[1], self[2] / other[2], self[3] / other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] / other, self[1] / other, self[2] / other, self[3] / other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] / other[0], self[1] / other[1], self[2] / other[2], self[3] / other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rlshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] << other.value, self[1] << other.value, self[2] << other.value, self[3] << other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2], self[3] << other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] << other, self[1] << other, self[2] << other, self[3] << other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] << other[0], self[1] << other[1], self[2] << other[2], self[3] << other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __radd__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] + other.value, self[1] + other.value, self[2] + other.value, self[3] + other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] + other, self[1] + other, self[2] + other, self[3] + other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rmul__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] * other.value, self[1] * other.value, self[2] * other.value, self[3] * other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2], self[3] * other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] * other, self[1] * other, self[2] * other, self[3] * other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] * other[0], self[1] * other[1], self[2] * other[2], self[3] * other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rrshift__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] >> other.value, self[1] >> other.value, self[2] >> other.value, self[3] >> other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2], self[3] >> other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] >> other, self[1] >> other, self[2] >> other, self[3] >> other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] >> other[0], self[1] >> other[1], self[2] >> other[2], self[3] >> other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ror__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] | other.value, self[1] | other.value, self[2] | other.value, self[3] | other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2], self[3] | other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] | other, self[1] | other, self[2] | other, self[3] | other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] | other[0], self[1] | other[1], self[2] | other[2], self[3] | other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __rfloordiv__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__(self[0] // other.value, self[1] // other.value, self[2] // other.value, self[3] // other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2], self[3] // other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self[0] // other, self[1] // other, self[2] // other, self[3] // other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__(self[0] // other[0], self[1] // other[1], self[2] // other[2], self[3] // other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __neg__(self):
        return self.__class__(-self[0], -self[1], -self[2], -self[3])
    
    def __pos__(self):
        return self.__class__(+self[0], +self[1], +self[2], +self[3])
    
    def __lt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] < other.value, self[1] < other.value, self[2] < other.value, self[3] < other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] < other[0], self[1] < other[1], self[2] < other[2], self[3] < other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] < other, self[1] < other, self[2] < other, self[3] < other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] < other[0], self[1] < other[1], self[2] < other[2], self[3] < other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __le__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] <= other.value, self[1] <= other.value, self[2] <= other.value, self[3] <= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] <= other[0], self[1] <= other[1], self[2] <= other[2], self[3] <= other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] <= other, self[1] <= other, self[2] <= other, self[3] <= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] <= other[0], self[1] <= other[1], self[2] <= other[2], self[3] <= other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __eq__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] == other.value, self[1] == other.value, self[2] == other.value, self[3] == other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] == other[0], self[1] == other[1], self[2] == other[2], self[3] == other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] == other, self[1] == other, self[2] == other, self[3] == other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] == other[0], self[1] == other[1], self[2] == other[2], self[3] == other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ge__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] >= other.value, self[1] >= other.value, self[2] >= other.value, self[3] >= other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] >= other[0], self[1] >= other[1], self[2] >= other[2], self[3] >= other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] >= other, self[1] >= other, self[2] >= other, self[3] >= other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] >= other[0], self[1] >= other[1], self[2] >= other[2], self[3] >= other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __ne__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] != other.value, self[1] != other.value, self[2] != other.value, self[3] != other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] != other[0], self[1] != other[1], self[2] != other[2], self[3] != other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] != other, self[1] != other, self[2] != other, self[3] != other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] != other[0], self[1] != other[1], self[2] != other[2], self[3] != other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))
    
    def __gt__(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec4(self[0] > other.value, self[1] > other.value, self[2] > other.value, self[3] > other.value)
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec4(self[0] > other[0], self[1] > other[1], self[2] > other[2], self[3] > other[3])
        elif isinstance(other, PYTHON_NUMBER):
            return BVec4(self[0] > other, self[1] > other, self[2] > other, self[3] > other)
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec4(self[0] > other[0], self[1] > other[1], self[2] > other[2], self[3] > other[3])
        else:
            raise TypeError('{} {} is not compatible with {}.'.format(type(other), other, type(self)))


