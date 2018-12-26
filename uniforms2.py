from numpy import array, empty
from pyglet.gl import GLfloat, GLuint, GLint, GLboolean, GLdouble
from glsl import *


def is_struct(x):
    return isinstance(x, Struct)


class Struct:
    """
    Just a convenience class to inherit in order to allow 'isinstance(x, Struct)'.
    """
    __slots__ = ()

    def __setattr__(self, key, value):
        # All attributes must remain of the same type, so every time an attribute is set it's not actually
        # setting the attribute but fills the attribute with the value.
        attribute = getattr(self, key)
        attribute[:] = value


class Material(Struct):

    __slots__ = ('ambient', 'diffuse', 'specular', 'shininess')

    def __init__(self, ambient, diffuse, specular, shininess):
        self.ambient  = Vec3(ambient)
        self.diffuse  = Vec3(diffuse)
        self.specular = Vec3(specular)

        self.shininess = Float(shininess)


class TexturedMaterial(Struct):
    __slots__ = ('diffuse', 'specular', 'emission', 'shininess')

    def __init__(self, shininess, diffuse=0, specular=1, emission=2):
        self.diffuse = array((diffuse,), dtype=GLint)  # Defines the texture unit.
        self.specular = array((specular,), dtype=GLint)
        self.emission = array((emission,), dtype=GLint)

        self.shininess = array((shininess,), dtype=GLfloat)


class SunLight(Struct):
    __slots__ = ('direction', 'ambient', 'diffuse', 'specular')

    def __init__(self, direction, ambient, diffuse, specular):
        self.direction = Vec3(direction)

        self.ambient  = Vec3(ambient)
        self.diffuse  = Vec3(diffuse)
        self.specular = Vec3(specular)


class PointLight(Struct):
    __slots__ = ('location', 'ambient', 'diffuse', 'specular', 'constant', 'linear', 'quadratic')

    def __init__(self, ambient, diffuse, specular, location, constant, linear, quadratic):
        self.location = Vec3(location)

        self.ambient = Vec3(ambient)
        self.diffuse = Vec3(diffuse)
        self.specular = Vec3(specular)

        self.constant = Float(constant)
        self.linear = Float(linear)
        self.quadratic = Float(quadratic)


class SpotLight(Struct):
    __slots__ = (
        'location', 'direction', 'ambient', 'diffuse', 'specular', 'inner_angle', 'outer_angle', 'constant', 'linear',
        'quadratic'
    )

    def __init__(self, location, direction, ambient, diffuse, specular, inner_angle, outer_angle, constant, linear,
                 quadratic):
        self.location = Vec3(location)
        self.direction = Vec3(direction)

        self.ambient = Vec3(ambient)
        self.diffuse = Vec3(diffuse)
        self.specular = Vec3(specular)

        self.inner_angle = Float(inner_angle)  # Should be cos of angle.
        self.outer_angle = Float(outer_angle)  # Should be cos of angle.

        self.constant = Float(constant)
        self.linear = Float(linear)
        self.quadratic = Float(quadratic)


def uniform_struct(struct_name, uniform):
    return [struct_name + '.' + attribute for attribute in uniform.__slots__]


def uniform_struct_array(struct_name, length, uniform):
    return [struct_name + '[{}].'.format(i) + attribute for i in range(length) for attribute in uniform.__slots__]


def uniform_struct_with_arrays(struct_name, length, uniform):
    return [struct_name + '.' + attribute + '[{}]'.format(i) for i in range(length) for attribute in uniform.__slots__]


# Default materials: http://devernay.free.fr/cours/opengl/materials.html
default_materials = """
emerald	        0.0215	 0.1745	  0.0215	0.07568	0.61424	0.07568	0.633	0.727811	0.633	0.6
jade	        0.135	 0.2225	  0.1575	0.54	0.89	0.63	0.316228	0.316228	0.316228	0.1
obsidian	    0.05375	 0.05	  0.06625	0.18275	0.17	0.22525	0.332741	0.328634	0.346435	0.3
pearl	        0.25	 0.20725  0.20725	1	0.829	0.829	0.296648	0.296648	0.296648	0.088
ruby	        0.1745	 0.01175  0.01175	0.61424	0.04136	0.04136	0.727811	0.626959	0.626959	0.6
turquoise	    0.1	     0.18725  0.1745	0.396	0.74151	0.69102	0.297254	0.30829	0.306678	0.1
brass	        0.329412 0.223529 0.027451	0.780392	0.568627	0.113725	0.992157	0.941176	0.807843	0.21794872
bronze      	0.2125	 0.1275	  0.054	    0.714	0.4284	0.18144	0.393548	0.271906	0.166721	0.2
chrome	        0.25	 0.25	  0.25	    0.4	0.4	0.4	0.774597	0.774597	0.774597	0.6
copper	        0.19125	 0.0735	  0.0225	0.7038	0.27048	0.0828	0.256777	0.137622	0.086014	0.1
gold	        0.24725	 0.1995	  0.0745	0.75164	0.60648	0.22648	0.628281	0.555802	0.366065	0.4
silver      	0.19225	 0.19225  0.19225	0.50754	0.50754	0.50754	0.508273	0.508273	0.508273	0.4
black_plastic	0.0  	 0.0	  0.0	    0.01	0.01	0.01	0.50	0.50	0.50	.25
cyan_plastic	0.0	     0.1	  0.06	    0.0	0.50980392	0.50980392	0.50196078	0.50196078	0.50196078	.25
green_plastic	0.0	     0.0	  0.0	    0.1	0.35	0.1	0.45	0.55	0.45	.25
red_plastic	    0.0	     0.0	  0.0	    0.5	0.0	0.0	0.7	0.6	0.6	.25
white_plastic	0.0	     0.0	  0.0	    0.55	0.55	0.55	0.70	0.70	0.70	.25
yellow_plastic	0.0	     0.0	  0.0	    0.5	0.5	0.0	0.60	0.60	0.50	.25
black_rubber	0.02	 0.02	  0.02	    0.01	0.01	0.01	0.4	0.4	0.4	.078125
cyan_rubber 	0.0	     0.05	  0.05	    0.4	0.5	0.5	0.04	0.7	0.7	.078125
green_rubber	0.0	     0.05	  0.0	    0.4	0.5	0.4	0.04	0.7	0.04	.078125
red_rubber	    0.05	 0.0	  0.0	    0.5	0.4	0.4	0.7	0.04	0.04	.078125
white_rubber	0.05	 0.05	  0.05	    0.5	0.5	0.5	0.7	0.7	0.7	.078125
yellow_rubber	0.05	 0.05	  0.0	    0.5	0.5	0.4	0.7	0.7	0.04	.078125
"""