from pyglet.gl import GLboolean, GLint, GLuint, GLfloat, GLdouble
import numpy
"""
Initialization:
vecn()              -> vecn(0, 0, ..., 0)
vecn(x)             -> vecn(x, x, ..., x)
vecn(x0, x1, ...)   -> vecn(x0, x1, ..., xn)
vecn(*iterable)     -> vecn(x0, x1, ..., xn)
vecn(*iterable, xn) -> vecn(x0, x1, ..., xn)
vecn(x0, *iterable) -> vecn(x0, x1, ..., xn)

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


def create_integer_scalar_class(name, inherit):
    binary_method = """
    def {name}(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value {operation} other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value {operation} other)
        else:
            raise TypeError('{{}} {{}} is not compatible with {{}}.'.format(type(other), other, type(self)))
    """

    binary_assignment_method = """
    def {name}(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value {operation}= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value {operation}= other
        else:
            raise TypeError('{{}} {{}} is not compatible with {{}}.'.format(type(other), other, type(self)))
    """

    unary_method = """
    def {name}(self, other):
        return {operation}self.value
    """

    comparison_method = """
    def {name}(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value {operation} other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value {operation} other
        else:
            raise TypeError('{{}} {{}} is not compatible with {{}}.'.format(type(other), other, type(self)))
    """

    binary_operations = {
        '__add__'     : '+',
        '__sub__'     : '-',
        '__mul__'     : '*',
        '__floordiv__': '//',
        '__mod__'     : '%',
        '__pow__'     : '**',
        '__lshift__'  : '<<',
        '__rshift__'  : '>>',
        '__and__'     : '&',
        '__xor__'     : '^',
        '__or__'      : '|',
    }
    binary_assignment_operations = {
        '__iadd__'     : '+',
        '__isub__'     : '-',
        '__imul__'     : '*',
        '__ifloordiv__': '//',
        '__imod__'     : '%',
        '__ipow__'     : '**',
        '__ilshift__'  : '<<',
        '__irshift__'  : '>>',
        '__iand__'     : '&',
        '__ixor__'     : '^',
        '__ior__'      : '|',
    }
    binary_reverse_operations = {
        '__radd__'     : '+',
        '__rsub__'     : '-',
        '__rmul__'     : '*',
        '__rfloordiv__': '//',
        '__rmod__'     : '%',
        '__rpow__'     : '**',
        '__rlshift__'  : '<<',
        '__rrshift__'  : '>>',
        '__rand__'     : '&',
        '__rxor__'     : '^',
        '__ror__'      : '|',
    }
    unary_operations = {
        '__pos__'   : '+',
        '__neg__'   : '-',
        '__invert__': '~'
    }
    comparison_operations = {
        '__lt__': '<',
        '__le__': '<=',
        '__eq__': '==',
        '__ne__': '!=',
        '__ge__': '>=',
        '__gt__': '>',
    }

    start = """
class {name}({inherit}):

    def __init__(self, value):
        if value:
            super().__init__(value)
        else:
            super().__init__()

        self.__dict__['dtype'] = super()._type_

    def __repr__(self):
        return '{{class_name}}({{value}})'.format(class_name=self.__class__.__name__, value=self.value)
""".format(name=name, inherit=inherit)

    methods = []

    methods.extend(
        binary_method.format(name=name, operation=operation) for name, operation in binary_operations.items())
    methods.extend(binary_assignment_method.format(name=name, operation=operation) for name, operation in
                   binary_assignment_operations.items())
    methods.extend(
        binary_method.format(name=name, operation=operation) for name, operation in binary_reverse_operations.items())
    methods.extend(unary_method.format(name=name, operation=operation) for name, operation in unary_operations.items())
    methods.extend(
        comparison_method.format(name=name, operation=operation) for name, operation in comparison_operations.items())

    class_definition = start + ''.join(methods)
    return class_definition


def create_decimal_scalar_class(name, inherit):
    binary_method = """
    def {name}(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.__class__(self.value {operation} other.value)
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__(self.value {operation} other)
        else:
            raise TypeError('{{}} {{}} is not compatible with {{}}.'.format(type(other), other, type(self)))
    """

    binary_assignment_method = """
    def {name}(self, other):
        if isinstance(other, GLSL_NUMBER):
            self.value {operation}= other.value
        elif isinstance(other, PYTHON_NUMBER):
            self.value {operation}= other
        else:
            raise TypeError('{{}} {{}} is not compatible with {{}}.'.format(type(other), other, type(self)))
    """

    unary_method = """
    def {name}(self, other):
        return {operation}self.value
    """

    comparison_method = """
    def {name}(self, other):
        if isinstance(other, GLSL_NUMBER):
            return self.value {operation} other.value
        elif isinstance(other, PYTHON_NUMBER):
            return self.value {operation} other
        else:
            raise TypeError('{{}} {{}} is not compatible with {{}}.'.format(type(other), other, type(self)))
    """

    binary_operations = {
        '__add__'     : '+',
        '__sub__'     : '-',
        '__mul__'     : '*',
        '__floordiv__': '//',
        '__truediv__' : '/',
        '__mod__'     : '%',
        '__pow__'     : '**',
    }
    binary_assignment_operations = {
        '__iadd__'     : '+',
        '__isub__'     : '-',
        '__imul__'     : '*',
        '__ifloordiv__': '//',
        '__itruediv__' : '/',
        '__imod__'     : '%',
        '__ipow__'     : '**',
    }
    binary_reverse_operations = {
        '__radd__'     : '+',
        '__rsub__'     : '-',
        '__rmul__'     : '*',
        '__rfloordiv__': '//',
        '__rtruediv__' : '/',
        '__rmod__'     : '%',
        '__rpow__'     : '**',
    }
    unary_operations = {
        '__pos__'   : '+',
        '__neg__'   : '-',
    }
    comparison_operations = {
        '__lt__': '<',
        '__le__': '<=',
        '__eq__': '==',
        '__ne__': '!=',
        '__ge__': '>=',
        '__gt__': '>',
    }

    start = """
class {name}({inherit}):

    def __init__(self, value):
        if value:
            super().__init__(value)
        else:
            super().__init__()
            
        self.__dict__['dtype'] = super()._type_
    
    def __repr__(self):
        return '{{class_name}}({{value}})'.format(class_name=self.__class__.__name__, value=self.value)
""".format(name=name, inherit=inherit)

    methods = []

    methods.extend(binary_method.format(name=name, operation=operation) for name, operation in binary_operations.items())
    methods.extend(binary_assignment_method.format(name=name, operation=operation) for name, operation in binary_assignment_operations.items())
    methods.extend(binary_method.format(name=name, operation=operation) for name, operation in binary_reverse_operations.items())
    methods.extend(unary_method.format(name=name, operation=operation) for name, operation in unary_operations.items())
    methods.extend(comparison_method.format(name=name, operation=operation) for name, operation in comparison_operations.items())

    class_definition = start + ''.join(methods)
    return class_definition


def create_integer_vector_class(name, inherit, elements):
    binary_method = """
    def {{name}}(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__({term1})
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__({term2})
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__({term3})
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__({term2})
        else:
            raise TypeError('{{{{}}}} {{{{}}}} is not compatible with {{{{}}}}.'.format(type(other), other, type(self)))
    """.format(
        term1=', '.join('self[{i}] {{operation}} other.value'.format(i=i) for i in range(elements)),
        term2=', '.join('self[{i}] {{operation}} other[{i}]'.format(i=i) for i in range(elements)),
        term3=', '.join('self[{i}] {{operation}} other'.format(i=i) for i in range(elements)),
    )

    unary_method = """
    def {{name}}(self):
        return self.__class__({term})
    """.format(term=', '.join('{{operation}}self[{i}]'.format(i=i) for i in range(elements)))

    comparison_method = """
    def {{name}}(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec{i}({term1})
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec{i}({term2})
        elif isinstance(other, PYTHON_NUMBER):
            return BVec{i}({term3})
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec{i}({term2})
        else:
            raise TypeError('{{{{}}}} {{{{}}}} is not compatible with {{{{}}}}.'.format(type(other), other, type(self)))
    """.format(
        i=elements,
        term1=', '.join('self[{i}] {{operation}} other.value'.format(i=i) for i in range(elements)),
        term2=', '.join('self[{i}] {{operation}} other[{i}]'.format(i=i) for i in range(elements)),
        term3=', '.join('self[{i}] {{operation}} other'.format(i=i) for i in range(elements)),
    )

    binary_operations = {
        '__add__'     : '+',
        '__sub__'     : '-',
        '__mul__'     : '*',
        '__floordiv__': '//',
        '__mod__'     : '%',
        '__pow__'     : '**',
        '__lshift__'  : '<<',
        '__rshift__'  : '>>',
        '__and__'     : '&',
        '__xor__'     : '^',
        '__or__'      : '|',
    }
    binary_reverse_operations = {
        '__radd__'     : '+',
        '__rsub__'     : '-',
        '__rmul__'     : '*',
        '__rfloordiv__': '//',
        '__rmod__'     : '%',
        '__rpow__'     : '**',
        '__rlshift__'  : '<<',
        '__rrshift__'  : '>>',
        '__rand__'     : '&',
        '__rxor__'     : '^',
        '__ror__'      : '|',
    }
    unary_operations = {
        '__pos__'   : '+',
        '__neg__'   : '-',
        '__invert__': '~'
    }
    comparison_operations = {
        '__lt__': '<',
        '__le__': '<=',
        '__eq__': '==',
        '__ne__': '!=',
        '__ge__': '>=',
        '__gt__': '>',
    }

    start = """
class {name}({inherit} * {elements}):

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
    
    def __len__(self):
        return super()._length_

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
        return '{{class_name}}({{value}})'.format(class_name=self.__class__.__name__, value=', '.join(str(x) for x in self))
    """.format(name=name, inherit=inherit, elements=elements)

    methods = []
    methods.extend(
        binary_method.format(name=name, operation=operation) for name, operation in binary_operations.items())
    # methods.extend(binary_assignment_method.format(name=name, operation=operation) for name, operation in binary_assignment_operations.items())
    methods.extend(
        binary_method.format(name=name, operation=operation) for name, operation in binary_reverse_operations.items())
    methods.extend(unary_method.format(name=name, operation=operation) for name, operation in unary_operations.items())
    methods.extend(
        comparison_method.format(name=name, operation=operation) for name, operation in comparison_operations.items())

    class_definition = start + ''.join(methods)
    return class_definition


def create_decimal_vector_class(name, inherit, elements):
    binary_method = """
    def {{name}}(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__({term1})
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__({term2})
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__({term3})
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__({term2})
        else:
            raise TypeError('{{{{}}}} {{{{}}}} is not compatible with {{{{}}}}.'.format(type(other), other, type(self)))
    """.format(
        term1=', '.join('self[{i}] {{operation}} other.value'.format(i=i) for i in range(elements)),
        term2=', '.join('self[{i}] {{operation}} other[{i}]'.format(i=i) for i in range(elements)),
        term3=', '.join('self[{i}] {{operation}} other'.format(i=i) for i in range(elements)),
    )

    binary_assignment_method = """
    def {{name}}(self, other):
        if isinstance(other, GLSL_NUMBER): 
            self[:] {{operation}} {term1}
        elif isinstance(other, GLSL_SEQUENCE):
            self[:] {{operation}} {term2}
        elif isinstance(other, PYTHON_NUMBER):
            self[:] {{operation}} {term3}
        elif isinstance(other, PYTHON_SEQUENCE):
            self[:] {{operation}} {term2}
        else:
            raise TypeError('{{{{}}}} {{{{}}}} is not compatible with {{{{}}}}.'.format(type(other), other, type(self)))
    """.format(
        term1=', '.join('other.value'.format(i=i) for i in range(elements)),
        term2=', '.join('other[{i}]'.format(i=i) for i in range(elements)),
        term3=', '.join('other'.format(i=i) for i in range(elements)),
    )

    unary_method = """
    def {{name}}(self):
        return self.__class__({term})
    """.format(term=', '.join('{{operation}}self[{i}]'.format(i=i) for i in range(elements)))

    comparison_method = """
    def {{name}}(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec{i}({term1})
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec{i}({term2})
        elif isinstance(other, PYTHON_NUMBER):
            return BVec{i}({term3})
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec{i}({term2})
        else:
            raise TypeError('{{{{}}}} {{{{}}}} is not compatible with {{{{}}}}.'.format(type(other), other, type(self)))
    """.format(
        i=elements,
        term1=', '.join('self[{i}] {{operation}} other.value'.format(i=i) for i in range(elements)),
        term2=', '.join('self[{i}] {{operation}} other[{i}]'.format(i=i) for i in range(elements)),
        term3=', '.join('self[{i}] {{operation}} other'.format(i=i) for i in range(elements)),
    )

    binary_operations = {
        '__add__'     : '+',
        '__sub__'     : '-',
        '__mul__'     : '*',
        '__floordiv__': '//',
        '__truediv__' : '/',
        '__mod__'     : '%',
        '__pow__'     : '**',
    }
    binary_assignment_operations = {
        '__iadd__'     : '+=',
        '__isub__'     : '-=',
        '__imul__'     : '*=',
        '__ifloordiv__': '//=',
        '__itruediv__' : '/=',
        '__imod__'     : '%=',
        '__ipow__'     : '**=',
        '__ilshift__'  : '<<=',
        '__irshift__'  : '>>=',
        '__iand__'     : '&=',
        '__ixor__'     : '^=',
        '__ior__'      : '|=',
    }
    binary_reverse_operations = {
        '__radd__'     : '+',
        '__rsub__'     : '-',
        '__rmul__'     : '*',
        '__rfloordiv__': '//',
        '__rtruediv__' : '/',
        '__rmod__'     : '%',
        '__rpow__'     : '**',
        '__rlshift__'  : '<<',
        '__rrshift__'  : '>>',
        '__rand__'     : '&',
        '__rxor__'     : '^',
        '__ror__'      : '|',
    }
    unary_operations = {
        '__pos__'   : '+',
        '__neg__'   : '-',
    }
    comparison_operations = {
        '__lt__': '<',
        '__le__': '<=',
        '__eq__': '==',
        '__ne__': '!=',
        '__ge__': '>=',
        '__gt__': '>',
    }

    start = """
class {name}({inherit} * {elements}):

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
    
    def __len__(self):
        return super()._length_

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
        return '{{class_name}}({{value}})'.format(class_name=self.__class__.__name__, value=', '.join(str(x) for x in self))
    """.format(name=name, inherit=inherit, elements=elements)

    methods = []
    methods.extend(binary_method.format(name=name, operation=operation) for name, operation in binary_operations.items())
    # methods.extend(binary_assignment_method.format(name=name, operation=operation) for name, operation in binary_assignment_operations.items())
    methods.extend(binary_method.format(name=name, operation=operation) for name, operation in binary_reverse_operations.items())
    methods.extend(unary_method.format(name=name, operation=operation) for name, operation in unary_operations.items())
    methods.extend(comparison_method.format(name=name, operation=operation) for name, operation in comparison_operations.items())

    class_definition = start + ''.join(methods)
    return class_definition


def create_decimal_matrix_class(name, inherit, rows, cols):
    elements = rows * cols

    binary_method = """
    def {{name}}(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return self.__class__({term1})
        elif isinstance(other, GLSL_SEQUENCE):
            return self.__class__({term2})
        elif isinstance(other, PYTHON_NUMBER):
            return self.__class__({term3})
        elif isinstance(other, PYTHON_SEQUENCE):
            return self.__class__({term2})
        else:
            raise TypeError('{{{{}}}} {{{{}}}} is not compatible with {{{{}}}}.'.format(type(other), other, type(self)))
    """.format(
        term1=', '.join('self[{i}] {{operation}} other.value'.format(i=i) for i in range(elements)),
        term2=', '.join('self[{i}] {{operation}} other[{i}]'.format(i=i) for i in range(elements)),
        term3=', '.join('self[{i}] {{operation}} other'.format(i=i) for i in range(elements)),
    )

    binary_assignment_method = """
    def {{name}}(self, other):
        if isinstance(other, GLSL_NUMBER): 
            self[:] {{operation}} {term1}
        elif isinstance(other, GLSL_SEQUENCE):
            self[:] {{operation}} {term2}
        elif isinstance(other, PYTHON_NUMBER):
            self[:] {{operation}} {term3}
        elif isinstance(other, PYTHON_SEQUENCE):
            self[:] {{operation}} {term2}
        else:
            raise TypeError('{{{{}}}} {{{{}}}} is not compatible with {{{{}}}}.'.format(type(other), other, type(self)))
    """.format(
        term1=', '.join('other.value'.format(i=i) for i in range(elements)),
        term2=', '.join('other[{i}]'.format(i=i) for i in range(elements)),
        term3=', '.join('other'.format(i=i) for i in range(elements)),
    )

    unary_method = """
    def {{name}}(self):
        return self.__class__({term})
    """.format(term=', '.join('{{operation}}self[{i}]'.format(i=i) for i in range(elements)))

    comparison_method = """
    def {{name}}(self, other):
        if isinstance(other, GLSL_NUMBER): 
            return BVec{i}({term1})
        elif isinstance(other, GLSL_SEQUENCE):
            return BVec{i}({term2})
        elif isinstance(other, PYTHON_NUMBER):
            return BVec{i}({term3})
        elif isinstance(other, PYTHON_SEQUENCE):
            return BVec{i}({term2})
        else:
            raise TypeError('{{{{}}}} {{{{}}}} is not compatible with {{{{}}}}.'.format(type(other), other, type(self)))
    """.format(
        i=elements,
        term1=', '.join('self[{i}] {{operation}} other.value'.format(i=i) for i in range(elements)),
        term2=', '.join('self[{i}] {{operation}} other[{i}]'.format(i=i) for i in range(elements)),
        term3=', '.join('self[{i}] {{operation}} other'.format(i=i) for i in range(elements)),
    )

    binary_operations = {
        '__add__'     : '+',
        '__sub__'     : '-',
        '__mul__'     : '*',
        '__floordiv__': '//',
        '__truediv__' : '/',
        '__mod__'     : '%',
        '__pow__'     : '**',
    }
    binary_assignment_operations = {
        '__iadd__'     : '+=',
        '__isub__'     : '-=',
        '__imul__'     : '*=',
        '__ifloordiv__': '//=',
        '__itruediv__' : '/=',
        '__imod__'     : '%=',
        '__ipow__'     : '**=',
        '__ilshift__'  : '<<=',
        '__irshift__'  : '>>=',
        '__iand__'     : '&=',
        '__ixor__'     : '^=',
        '__ior__'      : '|=',
    }
    binary_reverse_operations = {
        '__radd__'     : '+',
        '__rsub__'     : '-',
        '__rmul__'     : '*',
        '__rfloordiv__': '//',
        '__rtruediv__' : '/',
        '__rmod__'     : '%',
        '__rpow__'     : '**',
        '__rlshift__'  : '<<',
        '__rrshift__'  : '>>',
        '__rand__'     : '&',
        '__rxor__'     : '^',
        '__ror__'      : '|',
    }
    unary_operations = {
        '__pos__': '+',
        '__neg__': '-',
    }
    comparison_operations = {
        '__lt__': '<',
        '__le__': '<=',
        '__eq__': '==',
        '__ne__': '!=',
        '__ge__': '>=',
        '__gt__': '>',
    }

    start = """
class {name}({inherit} * {elements}):

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

    def __len__(self):
        return super()._length_

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
        return '{{class_name}}({{value}})'.format(class_name=self.__class__.__name__, value=', '.join(str(x) for x in self))
    """.format(name=name, inherit=inherit, elements=elements)

    methods = []
    methods.extend(
        binary_method.format(name=name, operation=operation) for name, operation in binary_operations.items())
    # methods.extend(binary_assignment_method.format(name=name, operation=operation) for name, operation in binary_assignment_operations.items())
    methods.extend(
        binary_method.format(name=name, operation=operation) for name, operation in binary_reverse_operations.items())
    methods.extend(unary_method.format(name=name, operation=operation) for name, operation in unary_operations.items())
    methods.extend(
        comparison_method.format(name=name, operation=operation) for name, operation in comparison_operations.items())

    class_definition = start + ''.join(methods)
    return class_definition


module_start = """from pyglet.gl import GLboolean, GLint, GLuint, GLfloat, GLdouble
import numpy

\"""
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
\"""

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

"""

tests = """



"""

with open('glsl2.py', 'w') as test:
    test.write(module_start)

    test.write(create_integer_scalar_class('Boolean', 'GLboolean'))
    test.write(create_integer_scalar_class('Int', 'GLint'))
    test.write(create_integer_scalar_class('Uint', 'GLuint'))
    test.write(create_decimal_scalar_class('Float', 'GLfloat'))
    test.write(create_decimal_scalar_class('Double', 'GLdouble'))

    for i in range(2, 5):
        test.write(create_integer_vector_class('BVec{}'.format(i), 'GLboolean', i))
        test.write(create_integer_vector_class('UVec{}'.format(i), 'GLuint', i))
        test.write(create_integer_vector_class('IVec{}'.format(i), 'GLint', i))
        test.write(create_decimal_vector_class('Vec{}'.format(i), 'GLfloat', i))
        test.write(create_decimal_vector_class('DVec{}'.format(i), 'GLdouble', i))



