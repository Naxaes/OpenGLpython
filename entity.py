from mathematics import create_transformation_matrix
import numpy
from pyglet.gl import (
    glBindBuffer, GL_ELEMENT_ARRAY_BUFFER, GL_ARRAY_BUFFER, glEnableVertexAttribArray, glVertexAttribPointer,
    GL_FLOAT, GL_FALSE, glDrawElements, GL_TRIANGLES, glDisableVertexAttribArray, GL_UNSIGNED_INT, glActiveTexture,
    GL_TEXTURE0, glBindTexture, GL_TEXTURE_2D, GL_LINES,
)


# from collections import namedtuple
# component_list = ['VOID', 'DISPLACEMENT', 'MODEL', 'TEXTURE']
# ComponentClass = namedtuple('Component', component_list)
# component = ComponentClass(*(numpy.uint(1 << i) if i > 0 else numpy.uint(0) for i in range(len(component_list))))



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

        self.mask     = numpy.zeros(shape=max_entities, dtype=numpy.uint, order='C')

        self.location = numpy.zeros(shape=(max_entities, 3), dtype=numpy.float32, order='C')
        self.rotation = numpy.zeros(shape=(max_entities, 3), dtype=numpy.float32, order='C')
        self.scale    = numpy.zeros(shape=(max_entities, 3), dtype=numpy.float32, order='C')

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
        for handle, entity in enumerate(self.mask):
            if entity == 0:
                return handle
        raise ValueError('Maximum entity count of %i reached!' % self.max_entities)


    def remove_entity(self, entity):
        self.mask[entity] = World.COMPONENT_VOID


    def create_object(self, mask, location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), model=0, diffuse=0, specular=0, emission=0):
        entity = self.create_entity()

        self.mask[entity] = mask
        self.location[entity] = location
        self.rotation[entity] = rotation
        self.scale[entity] = scale
        self.model[entity] = model
        self.diffuse[entity] = diffuse
        self.specular[entity] = specular
        self.emission[entity] = emission

        return entity


    def move(self, entity, dx, dy, dz):
        self.location[entity] += dx, dy, dz


    def rotate(self, entity, dx, dy, dz):
        self.rotation[entity] += dx, dy, dz


    def scale(self, entity, dx, dy, dz):
        self.scale[entity] += dx, dy, dz


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
        position_location = attribute_location['position']
        texture_location = attribute_location['texture_coordinate']
        normal_location = attribute_location['normal']

        for entity in numpy.where((self.mask & World.COMPONENT_SPRITE) == World.COMPONENT_SPRITE)[0]:
            model = models[self.model[entity]]

            shader.load_uniform_matrix(
                create_transformation_matrix(*self.location[entity], *self.rotation[entity], *self.scale[entity]),
                name='transform'
            )

            glActiveTexture(GL_TEXTURE0)
            texture = textures[self.diffuse[entity]]
            glBindTexture(GL_TEXTURE_2D, texture.id)
            glActiveTexture(GL_TEXTURE0 + 1)
            texture = textures[self.specular[entity]]
            glBindTexture(GL_TEXTURE_2D, texture.id)
            glActiveTexture(GL_TEXTURE0 + 2)
            texture = textures[self.emission[entity]]
            glBindTexture(GL_TEXTURE_2D, texture.id)

            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, model.indexed_vbo)

            glBindBuffer(GL_ARRAY_BUFFER, model.vbo_array['position'])
            glEnableVertexAttribArray(position_location)
            glVertexAttribPointer(position_location, 3, GL_FLOAT, GL_FALSE, 0, 0)

            glBindBuffer(GL_ARRAY_BUFFER, model.vbo_array['texture_coordinate'])
            glEnableVertexAttribArray(texture_location)
            glVertexAttribPointer(texture_location, 2, GL_FLOAT, GL_FALSE, 0, 0)

            glBindBuffer(GL_ARRAY_BUFFER, model.vbo_array['normal'])
            glEnableVertexAttribArray(normal_location)
            glVertexAttribPointer(normal_location, 3, GL_FLOAT, GL_FALSE, 0, 0)

            glDrawElements(GL_TRIANGLES, model.indexed_vbo.count, GL_UNSIGNED_INT, 0)


        glDisableVertexAttribArray(position_location)
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
        position_location = attribute_location['position']

        for entity in numpy.where(self.mask == World.COMPONENT_LIGHT)[0]:

            shader.load_uniform_matrix(
                create_transformation_matrix(*self.location[entity], *self.rotation[entity], *self.scale[entity]),
                name='transform'
            )

            model = models[self.model[entity]]

            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, model.indexed_vbo)

            glBindBuffer(GL_ARRAY_BUFFER, model.vbo_array['position'])
            glEnableVertexAttribArray(position_location)
            glVertexAttribPointer(position_location, 3, GL_FLOAT, GL_FALSE, 0, 0)

            glDrawElements(GL_TRIANGLES, model.indexed_vbo.count, GL_UNSIGNED_INT, 0)

        glDisableVertexAttribArray(position_location)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)