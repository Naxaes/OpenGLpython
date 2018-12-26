from mathematics import create_transformation_matrix
from glsl import *
import numpy
from pyglet.gl import (
    glBindBuffer, glEnableVertexAttribArray, glVertexAttribPointer, glDrawElements, glDisableVertexAttribArray,
    glActiveTexture, glBindTexture,
    
    GL_ELEMENT_ARRAY_BUFFER, GL_ARRAY_BUFFER, GL_TEXTURE0, GL_TEXTURE_2D,
    GL_FLOAT, GL_FALSE, GL_TRIANGLES, GL_UNSIGNED_INT,

    GLfloat, GLuint, GLint, GLboolean,
)


# from collections import namedtuple
# component_list = ['VOID', 'DISPLACEMENT', 'MODEL', 'TEXTURE']
# ComponentClass = namedtuple('Component', component_list)
# component = ComponentClass(*(numpy.uint(1 << i) if i > 0 else numpy.uint(0) for i in range(len(component_list))))


class Entity:

    needs_update = set()

    def __init__(self, location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
        self._location = Vec3(location)
        self._rotation = Vec3(rotation)
        self._scale = Vec3(scale)

        self.model = 0

        self.transformation = Mat4(*create_transformation_matrix(*location, *rotation, *scale).flatten())

    def update(self, *args, **kwargs):
        self.transformation = create_transformation_matrix(*self._location, *self._rotation, *self._scale)

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        Entity.needs_update.add(self)
        self._location = numpy.array(value, dtype=numpy.float)

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        Entity.needs_update.add(self)
        self._rotation = numpy.array(value, dtype=numpy.float)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        Entity.needs_update.add(self)
        self._scale = numpy.array(value, dtype=numpy.float)


class Light(Entity):

    needs_update = set()

    def __init__(self, struct, *args, **kwargs):
        super(Light, self).__init__(*args, **kwargs)
        self._struct = struct

    @property
    def struct(self):
        return self._struct

    @struct.setter
    def struct(self, value):
        self._struct = value
        Light.needs_update.add(self)


def update_entities():
    for entity in Entity.needs_update:
        entity.update()
    Entity.needs_update.clear()

    for light in Light.needs_update:
        light.update()
    Light.needs_update.clear()

def draw_entities(entities, shader, models):
    """


    Dependencies are location, rotation, scale, and model (optionally texture).

    Args:
        shader:
        models:

    Returns:

    """
    attribute_location = shader.attribute_location
    location_location = attribute_location['location']
    texture_location = attribute_location['texture_coordinate']
    normal_location = attribute_location['normal']

    for entity in entities:
        model = models[entity.model]

        shader.set_uniform_matrix('transform', entity.transformation)

        # glActiveTexture(GL_TEXTURE0)
        # texture = textures[entity.diffuse]
        # glBindTexture(GL_TEXTURE_2D, texture.id)
        # glActiveTexture(GL_TEXTURE0 + 1)
        # texture = textures[entity.specular]
        # glBindTexture(GL_TEXTURE_2D, texture.id)
        # glActiveTexture(GL_TEXTURE0 + 2)
        # texture = textures[entity.emission]
        # glBindTexture(GL_TEXTURE_2D, texture.id)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, model.indexed_vbo)

        glBindBuffer(GL_ARRAY_BUFFER, model.vbo_array['location'])
        glEnableVertexAttribArray(location_location)
        glVertexAttribPointer(location_location, 3, GL_FLOAT, GL_FALSE, 0, 0)

        glBindBuffer(GL_ARRAY_BUFFER, model.vbo_array['texture_coordinate'])
        glEnableVertexAttribArray(texture_location)
        glVertexAttribPointer(texture_location, 2, GL_FLOAT, GL_FALSE, 0, 0)

        glBindBuffer(GL_ARRAY_BUFFER, model.vbo_array['normal'])
        glEnableVertexAttribArray(normal_location)
        glVertexAttribPointer(normal_location, 3, GL_FLOAT, GL_FALSE, 0, 0)

        glDrawElements(GL_TRIANGLES, model.indexed_vbo.count, GL_UNSIGNED_INT, 0)

    Entity.needs_update.clear()

    glDisableVertexAttribArray(location_location)
    glDisableVertexAttribArray(texture_location)
    glDisableVertexAttribArray(normal_location)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)


def draw_lights(lights, shader, models):
    """


    Dependencies are location, rotation, scale, and model (optionally texture).

    Args:
        lights:
        shader:
        models:

    Returns:

    """
    attribute_location = shader.attribute_location
    location_location = attribute_location['location']

    for entity in lights:

        shader.load_uniform_matrix(entity.transformation, name='transform')

        model = models[entity.model]

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, model.indexed_vbo)

        glBindBuffer(GL_ARRAY_BUFFER, model.vbo_array['location'])
        glEnableVertexAttribArray(location_location)
        glVertexAttribPointer(location_location, 3, GL_FLOAT, GL_FALSE, 0, 0)

        glDrawElements(GL_TRIANGLES, model.indexed_vbo.count, GL_UNSIGNED_INT, 0)

    glDisableVertexAttribArray(location_location)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)



class World:

    # Must be of same data type as 'mask' array.
    COMPONENT_VOID = numpy.uint(0)
    COMPONENT_DISPLACEMENT = numpy.uint(1 << 0)
    COMPONENT_MODEL = numpy.uint(1 << 1)
    COMPONENT_TEXTURE = numpy.uint(1 << 2)

    COMPONENT_LIGHT =  COMPONENT_DISPLACEMENT | COMPONENT_MODEL
    COMPONENT_SPRITE = COMPONENT_DISPLACEMENT | COMPONENT_MODEL | COMPONENT_TEXTURE

    def __init__(self, max_entities):
        self.max_entities = max_entities
        self.entity_count = 0

        self.mask     = numpy.zeros(shape=max_entities, dtype=numpy.uint, order='C')

        self.location = numpy.zeros(shape=(max_entities, 3), dtype=numpy.float32, order='C')
        self.rotation = numpy.zeros(shape=(max_entities, 3), dtype=numpy.float32, order='C')
        self.scale    = numpy.zeros(shape=(max_entities, 3), dtype=numpy.float32, order='C')

        self.transformation = numpy.zeros(shape=(max_entities, 4, 4), dtype=numpy.float32, order='C')

        self.model    = numpy.zeros(shape=max_entities, dtype=numpy.uint, order='C')

        self.diffuse  = numpy.zeros(shape=max_entities, dtype=numpy.uint, order='C')
        self.specular = numpy.zeros(shape=max_entities, dtype=numpy.uint, order='C')
        self.emission = numpy.zeros(shape=max_entities, dtype=numpy.uint, order='C')


    def create_entity(self) -> int:
        """
        Generates a handle for an entity.

        Returns:
            int
        """
        handle = self.entity_count
        self.entity_count += 1
        if self.entity_count > self.max_entities:
            raise ValueError('Maximum entity count of %i reached!' % self.max_entities)
        else:
            return handle


    def remove_entity(self, entity):
        self.mask[entity] = World.COMPONENT_VOID


    def create_object(self, mask, location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), model=0, diffuse=0, specular=0, emission=0):
        entity = self.create_entity()

        self.mask[entity] = mask
        self.location[entity] = location
        self.rotation[entity] = rotation
        self.scale[entity] = scale
        self.transformation[entity] = create_transformation_matrix(*location, *rotation, *scale)
        self.model[entity] = model
        self.diffuse[entity] = diffuse
        self.specular[entity] = specular
        self.emission[entity] = emission

        return entity


    def move(self, entity, dx, dy, dz):
        self.location[entity] += dx, dy, dz
        self.transformation[entity] = create_transformation_matrix(
            *self.location[entity], *self.rotation[entity], *self.scale[entity]
        )


    def rotate(self, entity, dx, dy, dz):
        self.rotation[entity] += dx, dy, dz
        self.transformation[entity] = create_transformation_matrix(
            *self.location[entity], *self.rotation[entity], *self.scale[entity]
        )


    def scale(self, entity, dx, dy, dz):
        self.scale[entity] += dx, dy, dz
        self.transformation[entity] = create_transformation_matrix(
            *self.location[entity], *self.rotation[entity], *self.scale[entity]
        )


    def draw(self, shader, models, textures):
        """


        Dependencies are location, rotation, scale, and model (optionally texture).

        Args:
            shader:
            models:
            textures:

        Returns:

        """
        attribute_location = shader.attribute_location
        location_location = attribute_location['position']
        texture_location = attribute_location['texture_coordinate']
        normal_location = attribute_location['normal']

        transformation = self.transformation

        diffuse = self.diffuse
        specular = self.specular
        emission = self.emission

        for entity in numpy.where((self.mask & World.COMPONENT_SPRITE) == World.COMPONENT_SPRITE)[0]:
            model = models[self.model[entity]]

            shader.load_uniform_matrix(transformation[entity], name='transform')

            glActiveTexture(GL_TEXTURE0)
            texture = textures[diffuse[entity]]
            glBindTexture(GL_TEXTURE_2D, texture.id)
            glActiveTexture(GL_TEXTURE0 + 1)
            texture = textures[specular[entity]]
            glBindTexture(GL_TEXTURE_2D, texture.id)
            glActiveTexture(GL_TEXTURE0 + 2)
            texture = textures[emission[entity]]
            glBindTexture(GL_TEXTURE_2D, texture.id)

            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, model.indexed_vbo)

            glBindBuffer(GL_ARRAY_BUFFER, model.vbo_array['location'])
            glEnableVertexAttribArray(location_location)
            glVertexAttribPointer(location_location, 3, GL_FLOAT, GL_FALSE, 0, 0)

            glBindBuffer(GL_ARRAY_BUFFER, model.vbo_array['texture_coordinate'])
            glEnableVertexAttribArray(texture_location)
            glVertexAttribPointer(texture_location, 2, GL_FLOAT, GL_FALSE, 0, 0)

            glBindBuffer(GL_ARRAY_BUFFER, model.vbo_array['normal'])
            glEnableVertexAttribArray(normal_location)
            glVertexAttribPointer(normal_location, 3, GL_FLOAT, GL_FALSE, 0, 0)

            glDrawElements(GL_TRIANGLES, model.indexed_vbo.count, GL_UNSIGNED_INT, 0)


        glDisableVertexAttribArray(location_location)
        glDisableVertexAttribArray(texture_location)
        glDisableVertexAttribArray(normal_location)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def draw_light(self, shader, models):
        """


        Dependencies are location, rotation, scale, and model (optionally texture).

        Args:
            shader:
            models:

        Returns:

        """
        attribute_location = shader.attribute_location
        location_location = attribute_location['position']

        for entity in numpy.where(self.mask == World.COMPONENT_LIGHT)[0]:

            shader.load_uniform_matrix(
                create_transformation_matrix(*self.location[entity], *self.rotation[entity], *self.scale[entity]),
                name='transform'
            )

            model = models[self.model[entity]]

            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, model.indexed_vbo)

            glBindBuffer(GL_ARRAY_BUFFER, model.vbo_array['location'])
            glEnableVertexAttribArray(location_location)
            glVertexAttribPointer(location_location, 3, GL_FLOAT, GL_FALSE, 0, 0)

            glDrawElements(GL_TRIANGLES, model.indexed_vbo.count, GL_UNSIGNED_INT, 0)

        glDisableVertexAttribArray(location_location)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)


























#
#
#
#
# class World:
#     # Must be of same data type as 'mask' array.
#     COMPONENT_VOID = numpy.uint(0)
#     COMPONENT_DISPLACEMENT = numpy.uint(1 << 0)
#     COMPONENT_MODEL = numpy.uint(1 << 1)
#     COMPONENT_TEXTURE = numpy.uint(1 << 2)
#
#     COMPONENT_LIGHT = COMPONENT_DISPLACEMENT | COMPONENT_MODEL
#     COMPONENT_SPRITE = COMPONENT_DISPLACEMENT | COMPONENT_MODEL | COMPONENT_TEXTURE
#
#     def __init__(self, max_entities):
#         self.max_entities = max_entities
#         self.entity_count = 0
#
#         self.mask = numpy.zeros(shape=max_entities, dtype=numpy.uint, order='C')
#
#         # Displacement.
#         self.location = numpy.zeros(shape=(max_entities, 3), dtype=numpy.float32, order='C')
#         self.rotation = numpy.zeros(shape=(max_entities, 3), dtype=numpy.float32, order='C')
#         self.scale = numpy.zeros(shape=(max_entities, 3), dtype=numpy.float32, order='C')
#         self.transformation = numpy.zeros(shape=(max_entities, 4, 4), dtype=numpy.float32, order='C')
#
#         # Model.
#         self.model = numpy.zeros(shape=max_entities, dtype=numpy.uint, order='C')
#
#         # Texture.
#         self.diffuse = numpy.zeros(shape=max_entities, dtype=numpy.uint, order='C')
#         self.specular = numpy.zeros(shape=max_entities, dtype=numpy.uint, order='C')
#         self.emission = numpy.zeros(shape=max_entities, dtype=numpy.uint, order='C')
#
#
# def create_entity(world, **attributes) -> int:
#     """
#     Generates a handle for an entity.
#
#     Returns:
#         int
#     """
#     handle = world.entity_count
#     world.entity_count += 1
#
#     if world.entity_count > world.max_entities:
#         raise ValueError('Maximum entity count of %i reached!' % world.max_entities)
#
#     for key, value in attributes.items():
#         attribute_array = getattr(world, key)
#         attribute_array[handle][:] = value
#
#     return handle
#
#
# def remove_entity(world, entity):
#     world.mask[entity] = World.COMPONENT_VOID
#
#
# def draw(world, mask, shader, models, textures):
#     """
#
#
#     Dependencies are location, rotation, scale, and model (optionally texture).
#
#     Args:
#         world:
#         mask:
#         shader:
#         models:
#         textures:
#
#     Returns:
#
#     """
#     attribute_location = shader.attribute_location
#     location_location = attribute_location['location']
#     texture_location = attribute_location['texture_coordinate']
#     normal_location = attribute_location['normal']
#
#     for entity in numpy.where((world.mask & mask) == mask)[0]:
#         model = models[world.model[entity]]
#
#         shader.load_uniform_matrix(world.transformation[entity], name='transform')
#
#         glActiveTexture(GL_TEXTURE0)
#         texture = textures[world.diffuse[entity]]
#         glBindTexture(GL_TEXTURE_2D, texture.id)
#         glActiveTexture(GL_TEXTURE0 + 1)
#         texture = textures[world.specular[entity]]
#         glBindTexture(GL_TEXTURE_2D, texture.id)
#         glActiveTexture(GL_TEXTURE0 + 2)
#         texture = textures[world.emission[entity]]
#         glBindTexture(GL_TEXTURE_2D, texture.id)
#
#         glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, model.indexed_vbo)
#
#         glBindBuffer(GL_ARRAY_BUFFER, model.vbo_array['location'])
#         glEnableVertexAttribArray(location_location)
#         glVertexAttribPointer(location_location, 3, GL_FLOAT, GL_FALSE, 0, 0)
#
#         glBindBuffer(GL_ARRAY_BUFFER, model.vbo_array['texture_coordinate'])
#         glEnableVertexAttribArray(texture_location)
#         glVertexAttribPointer(texture_location, 2, GL_FLOAT, GL_FALSE, 0, 0)
#
#         glBindBuffer(GL_ARRAY_BUFFER, model.vbo_array['normal'])
#         glEnableVertexAttribArray(normal_location)
#         glVertexAttribPointer(normal_location, 3, GL_FLOAT, GL_FALSE, 0, 0)
#
#         glDrawElements(GL_TRIANGLES, model.indexed_vbo.count, GL_UNSIGNED_INT, 0)
#
#     glDisableVertexAttribArray(location_location)
#     glDisableVertexAttribArray(texture_location)
#     glDisableVertexAttribArray(normal_location)
#     glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
#     glBindBuffer(GL_ARRAY_BUFFER, 0)
#
#
# def draw_light(world, shader, models):
#     """
#
#
#     Dependencies are location, rotation, scale, and model (optionally texture).
#
#     Args:
#         world:
#         shader:
#         models:
#
#     Returns:
#
#     """
#     attribute_location = shader.attribute_location
#     location_location = attribute_location['location']
#
#     for entity in numpy.where(world.mask == World.COMPONENT_LIGHT)[0]:
#         shader.load_uniform_matrix(world.transformation[entity], name='transform')
#
#         model = models[world.model[entity]]
#
#         glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, model.indexed_vbo)
#
#         glBindBuffer(GL_ARRAY_BUFFER, model.vbo_array['location'])
#         glEnableVertexAttribArray(location_location)
#         glVertexAttribPointer(location_location, 3, GL_FLOAT, GL_FALSE, 0, 0)
#
#         glDrawElements(GL_TRIANGLES, model.indexed_vbo.count, GL_UNSIGNED_INT, 0)
#
#     glDisableVertexAttribArray(location_location)
#     glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
#     glBindBuffer(GL_ARRAY_BUFFER, 0)