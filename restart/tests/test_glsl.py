import unittest
from glsl2 import *
from itertools import combinations_with_replacement


class TestGLSL(unittest.TestCase):


    def test_initialize_vectors(self):
        vector_classes = [
            (Vec2, BVec2, IVec2, UVec2, DVec2), (Vec3, BVec3, IVec3, UVec3, DVec3), (Vec4, BVec4, IVec4, UVec4, DVec4)
        ]

        for dimension, vector_list in enumerate(vector_classes, start=2):
            for vector in vector_list:
                iterable1 = (1,) * dimension
                iterable2 = (1,) * (dimension - 1)

                a = vector()                         # ALL
                b = vector(None)                     # ALL
                c = vector(1)                        # ALL
                e = vector(*iterable1)               # ALL
                f = vector(*iterable2, 1)            # ALL
                g = vector(1, *iterable2)            # ALL
                h = vector(*iterable2)               # ALL

                self.assertTrue(all(x == 0 for x in a))
                self.assertTrue(all(x == 0 for x in b))
                self.assertTrue(all(x == 1 for x in c))
                self.assertTrue(all(x == 1 for x in e))
                self.assertTrue(all(x == 1 for x in f))
                self.assertTrue(all(x == 1 for x in g))
                self.assertTrue(h[-1] == 0 and all(x == 1 for x in h[:-1]))

                # vector(iterable2, 1)          # Does not work!
                # vector(1, iterable2)          # Does not work!

                if vector in (Vec2, DVec2, Vec3, DVec3, Vec4, DVec4):
                    iterable3 = (1.0,) * dimension
                    iterable4 = (1.0,) * (dimension - 1)

                    i = vector(1.0)                # Float and double only
                    j = vector(*iterable3)         # Float and double only
                    k = vector(*iterable4, 1.0)    # Float and double only
                    l = vector(1.0, *iterable4)    # Float and double only
                    m = vector(*iterable4)         # Float and double only

                    self.assertTrue(all(x == 1 for x in i))
                    self.assertTrue(all(x == 1 for x in j))
                    self.assertTrue(all(x == 1 for x in k))
                    self.assertTrue(all(x == 1 for x in l))
                    self.assertTrue(m[-1] == 0 and all(x == 1 for x in m[:-1]))


    def test_positive_binary_operation_integers(self):
        """
        Assumes all vectors can be iterated properly.
        """
        vector_classes = [
            (BVec2, UVec2, IVec2), (BVec3, UVec3, IVec3), (BVec4, UVec4, IVec4)
        ]
        binaries = ['+', '-', '*', '//', '%', '**', '<<', '>>', '&', '^', '|']
        namespace = {}

        for vector_list in vector_classes:
            for vector1, vector2 in combinations_with_replacement(vector_list, 2):
                a = vector1(2)  # Must be higher than b for test a - b to work for unsigned values.
                b = vector2(1)

                namespace['a'] = a
                namespace['b'] = b

                for binary in binaries:
                    exec('x = a {} b'.format(binary), namespace)
                    exec('test = all(x0 == (a0 {} b0) for x0, (a0, b0) in zip(x, zip(a, b)))'.format(binary), namespace)

                    self.assertTrue(namespace['test'], msg='Failed at binary {} for class {} and {}'.format(binary, vector1, vector2))

    def test_positive_binary_operation_decimals(self):
        """
        Assumes all vectors can be iterated properly.
        """
        vector_classes = [
            (Vec2, DVec2), (Vec3, DVec3), (Vec4, DVec4)
        ]
        binaries = ['+', '-', '*', '//', '/', '%', '**']
        namespace = {}

        for vector_list in vector_classes:
            for vector1, vector2 in combinations_with_replacement(vector_list, 2):
                a = vector1(2)
                b = vector2(1)

                namespace['a'] = a
                namespace['b'] = b

                for binary in binaries:
                    exec('x = a {} b'.format(binary), namespace)
                    exec('test = all(x0 == (a0 {} b0) for x0, (a0, b0) in zip(x, zip(a, b)))'.format(binary), namespace)

                    self.assertTrue(namespace['test'], msg='Failed at binary {} for class {} and {}'.format(binary, vector1, vector2))


    def test_comparison_operators(self):
        vector_classes = [
            (BVec2, UVec2, IVec2, Vec2, DVec2), (BVec3, UVec3, IVec3, Vec3, DVec3), (BVec4, UVec4, IVec4, Vec4, DVec4)
        ]
        operators = ['<', '<=', '==', '!=', '>=', '>']
        namespace = {}

        for vector_list in vector_classes:
            for vector1, vector2 in combinations_with_replacement(vector_list, 2):
                a = vector1(2)
                b = vector2(1)

                namespace['a'] = a
                namespace['b'] = b

                for operator in operators:
                    exec('x = a {} b'.format(operator), namespace)
                    exec('test = all(x0 == (a0 {} b0) for x0, (a0, b0) in zip(x, zip(a, b)))'.format(operator), namespace)

                    self.assertTrue(namespace['test'], msg='Failed at binary {} for class {} and {}'.format(operator, vector1, vector2))




if __name__ == '__main__':
    unittest.main()