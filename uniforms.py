from numpy import array, empty
from pyglet.gl import GLfloat, GLuint, GLint, GLboolean, GLdouble


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


def is_struct(x):
    return isinstance(x, Struct)


class Struct:  # TODO Make struct numpy array? Will convert to dtype object is dimensions don't match. Problem?
    """
    Just a convenience class to inherit in order to allow 'isinstance(x, Struct)'.
    """
    __slots__ = ()

    def __setattr__(self, key, value):
        try:
            attribute = getattr(self, key)  # AttributeError.
            attribute[:] = value
        except AttributeError:
            super().__setattr__(key, value)


class Material(Struct):

    __slots__ = ('ambient', 'diffuse', 'specular', 'shininess')

    def __init__(self, ambient, diffuse, specular, shininess):
        self.ambient   = array(ambient,   dtype=GLfloat, order='C')
        self.diffuse   = array(diffuse,   dtype=GLfloat, order='C')
        self.specular  = array(specular,  dtype=GLfloat, order='C')

        self.shininess = array((shininess,), dtype=GLfloat)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)


class TexturedMaterial(Struct):

    __slots__ = ('diffuse', 'specular', 'emission', 'shininess')

    def __init__(self, shininess, diffuse=0, specular=1, emission=2):
        self.diffuse   = array((diffuse,),   dtype=GLint)  # Defines the texture unit.
        self.specular  = array((specular,),  dtype=GLint)
        self.emission  = array((emission,),  dtype=GLint)

        self.shininess = array((shininess,), dtype=GLfloat)


class SunLight(Struct):

    __slots__ = ('direction', 'ambient', 'diffuse', 'specular')

    def __init__(self, direction, ambient, diffuse, specular):
        self.direction = array(direction, dtype=GLfloat, order='C')

        self.ambient   = array(ambient,   dtype=GLfloat, order='C')
        self.diffuse   = array(diffuse,   dtype=GLfloat, order='C')
        self.specular  = array(specular,  dtype=GLfloat, order='C')


class PointLight(Struct):

    __slots__ = ('position', 'ambient', 'diffuse', 'specular', 'constant', 'linear', 'quadratic')

    def __init__(self, ambient, diffuse, specular, position, constant, linear, quadratic):
        self.position = array(position, dtype=GLfloat, order='C')

        self.ambient  = array(ambient,  dtype=GLfloat, order='C')
        self.diffuse  = array(diffuse,  dtype=GLfloat, order='C')
        self.specular = array(specular, dtype=GLfloat, order='C')

        self.constant  = array((constant,),  dtype=GLfloat)
        self.linear    = array((linear,),    dtype=GLfloat)
        self.quadratic = array((quadratic,), dtype=GLfloat)


class SpotLight(Struct):

    __slots__ = ('position', 'direction', 'ambient', 'diffuse', 'specular', 'inner_angle', 'outer_angle', 'constant', 'linear', 'quadratic')

    def __init__(self, position, direction, ambient, diffuse, specular, inner_angle, outer_angle, constant, linear, quadratic):
        self.position  = array(position,  dtype=GLfloat, order='C')
        self.direction = array(direction, dtype=GLfloat, order='C')

        self.ambient  = array(ambient,  dtype=GLfloat, order='C')
        self.diffuse  = array(diffuse,  dtype=GLfloat, order='C')
        self.specular = array(specular, dtype=GLfloat, order='C')

        self.inner_angle = array((inner_angle,), dtype=GLfloat)  # Should be cos of angle!
        self.outer_angle = array((outer_angle,), dtype=GLfloat)  # Should be cos of angle!

        self.constant  = array((constant,),  dtype=GLfloat)
        self.linear    = array((linear,),    dtype=GLfloat)
        self.quadratic = array((quadratic,), dtype=GLfloat)


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




def struct(name, fields, print_class=False):
    """
    Creates a struct class which can be sent in the shader program.

    Examples:
        >>> PointLight = struct('PointLight', fields=['vec3 position', 'vec3 ambient', 'vec3 diffuse', 'vec3 specular'])
        >>> light = PointLight()
        >>> light.position = 0, -50, 0
        >>> light.position
        array([  0., -50.,   0.], dtype=float32)


    Args:
        name: 
        fields: 
        print_class: Prints the class definition. Could be useful if you want to copy and modify it yourself and/or not
                     create the class at runtime.

    Returns:

    """
    # TODO Make these two global?
    data_type_mapping = {'bool'  : 'GLboolean', 'int': 'GLint', 'uint': 'GLuint', 'float': 'GLfloat',
                         'double': 'GLdouble'}
    prefix_mapping = {'b': 'GLboolean', 'i': 'GLint', 'u': 'GLuint', '': 'GLfloat', 'd': 'GLdouble'}

    field_types = []
    field_names = []
    for field in fields:
        field_type, field_name = field.split()

        array_length = ''
        if '[' in field_name:
            field_name, length = field_name.split('[')
            array_length = length[:-1]

        if field_type in GLSL_SCALARS:
            shape = '1' if not array_length else array_length
            dtype = data_type_mapping.get(field_type)
        elif field_type in GLSL_VECTORS:
            shape = field_type[-1] if not array_length else array_length + ', ' + field_type[-1]
            dtype = prefix_mapping.get(field_type[0], 'GLfloat')  # Since absence of prefix means float.
        elif field_type in GLSL_MATRICES:
            if 'x' in field_type:
                shape = field_type[-3] + ', ' + field_type[-1]
            else:
                shape = field_type[-1] + ', ' + field_type[-1]
            dtype = prefix_mapping.get(field_type[0], 'GLfloat')  # Since absence of prefix means float.
        elif field_type in GLSL_SAMPLERS:
            shape = '1' if not array_length else array_length
            dtype = 'GLuint'
        else:
            raise NotImplemented(field_type + ' is not yet supported!')

        temp = 'empty(shape=({}), dtype={}, order="C")'.format(shape, dtype)
        field_types.append(temp)
        field_names.append(field_name)

    # TODO Make theses lines in a function in a different module?
    slots = ', '.join(['"_{}"'.format(field_name) for field_name in field_names])
    attributes = '\n        '.join(
        ('self._' + field_name + ' = ' + field_type) for field_name, field_type in zip(field_names, field_types))

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

    def __init__(self):
        {attributes}

    def __repr__(self):
        attributes = '\\n'.join('    %s = %s' % (field, getattr(self, name)) for field, name in zip({fields}, self.__slots__))
        return '{name}:\\n' + attributes
    {properties}
""".format(name=name.title(), slots=slots, attributes=attributes, properties=properties, fields=fields)

    if print_class:
        print(class_template)

    namespace = {
        'empty': empty, 'GLboolean': GLboolean, 'GLint': GLint,
        'GLuint': GLuint, 'GLfloat': GLfloat, 'GLdouble': GLdouble
    }
    exec(class_template, namespace)
    return namespace[name]


# a = Material((1, 2, 3), (1, 2, 3), (1, 2, 3), 4)
# a.diffuse = (4, 4, 4)
# print(a.diffuse)