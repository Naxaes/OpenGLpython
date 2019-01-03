from pyglet.gl import (
    glGenTextures, glBindTexture, glTexParameteri, glTexParameterfv, glTexImage2D, glActiveTexture,

    GL_TEXTURE_2D, GL_LINEAR, GL_CLAMP_TO_EDGE, GL_TEXTURE_BASE_LEVEL, GL_TEXTURE_MAX_LEVEL, GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_MAG_FILTER, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_RGB, GL_UNSIGNED_BYTE, GL_TEXTURE0, GL_RGBA,

    GLuint, GLubyte,
)
import pyglet
import pyglet.extlibs.png as pypng
from pyglet.image.codecs import ImageDecodeException

from array import array
from itertools import chain
from ctypes import create_string_buffer

class Texture(GLuint):

    __slots__ = 'texture'

    FORMATS = {
        'RGBA': GL_RGBA,
        'RGB': GL_RGB
    }

    def __init__(self, path, format=None,
                 min_filter=GL_LINEAR, max_filter=GL_LINEAR,
                 wrap_s=GL_CLAMP_TO_EDGE, wrap_t=GL_CLAMP_TO_EDGE
                 ):
        #
        # try:
        #     reader = pypng.Reader(file=open(path, 'rb'))
        #     width, height, pixels, metadata = reader.asDirect()
        # except Exception as e:
        #     raise ImageDecodeException(
        #         'PyPNG cannot read %s: %s' % (path, e))
        #
        # if metadata['greyscale']:
        #     if metadata['alpha']:
        #         internal_format = 'LA'
        #     else:
        #         internal_format = 'L'
        # else:
        #     if metadata['alpha']:
        #         internal_format = 'RGBA'
        #     else:
        #         internal_format = 'RGB'
        #
        # pitch = len(internal_format) * width
        #
        # pixels = array('BH'[metadata['bitdepth']>8], chain(*pixels))

        self.texture = pyglet.image.load(path).get_texture()
        super().__init__(self.texture.id)
        # glGenTextures(1, self)
        glBindTexture(GL_TEXTURE_2D, self)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, min_filter)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, max_filter)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap_s)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap_t)

        #
        # DataClass = GLubyte * (width * height * len(internal_format))
        # data = DataClass(*pixels)
        #
        #
        # internal_format = Texture.FORMATS[internal_format]
        #
        # glTexImage2D(GL_TEXTURE_2D, 0,
        #              internal_format,
        #              width, height, 0, format or internal_format,
        #              GL_UNSIGNED_BYTE, data
        #              )

        glBindTexture(GL_TEXTURE_2D, 0)


        self.height = self.texture.height
        self.width = self.texture.width
        self.path = path



    def enable(self, slot=0):
        glBindTexture(GL_TEXTURE_2D, self)
        glActiveTexture(GL_TEXTURE0 + slot)

    @staticmethod
    def disable():
        glBindTexture(GL_TEXTURE_2D, 0)

