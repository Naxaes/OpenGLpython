from collections import OrderedDict, namedtuple
from itertools import combinations
from source.linear_algebra import *


class Component:
    def __repr__(self):
        title = "\n{}:\n".format(self.__class__.__name__)
        attribute_template = "\t{:<10} = {}"

        return title + "\n".join(
            [attribute_template.format(name, value) for name, value in self.__dict__.items()]
        )


class Transform(Component):
    def __init__(self, location, rotation, scale):
        self.location = Vector3(*location)
        self.rotation = Vector3(*rotation)
        self.scale    = Vector3(*scale)

    def matrix(self):
        return transformation_matrix(*self.location, *self.rotation, *self.scale)


class Renderable(Component):
    def __init__(self, shader, model, *textures):
        self.shader   = shader
        self.model    = model
        self.textures = textures


class PointLight(Component):
    def __init__(self, color, attenuation):
        self.color = color
        self.attenuation = attenuation


class Physics(Component):
    def __init__(self, velocity, acceleration, max_speed):
        self.velocity = velocity
        self.acceleration = acceleration
        self.max_speed = max_speed


class Collidable(Component):
    def __init__(self, hitbox):
        self.hitbox = hitbox

#
# transformations = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# point_lights    = [                        8, 9]
# physics         = [0, 1, 2, 3,                9]
# collidables     = [      2, 3, 4, 5,       8, 9]
#
#

"""
Plan for cache-friendliness. Each set of components will have it's own contiguous array of SOA data. The * represents
an array.

Index: 0
* Transform

Index: 1
* Transform
* Renderable

Index: 2
* Transform
* Physics

Index: 3
* Transform
* Renderable
* Physics

"""

class SwitchArray:

    def __init__(self, ConstructorClass):
        self.ConstructorClass = ConstructorClass
        self.data = [None]       # Making sure to always have one free slot.
        self.last_occupied = -1  # Index of first free slot

    def __iter__(self):
        return (self.data[i] for i in range(self.last_occupied + 1))

    def create(self):
        if 0 <= self.last_occupied < len(self.data)-2:
            index = self.last_occupied
            self.data[index] = None
            self.last_occupied += 1
        else:
            self.data.append(None)
            index = len(self.data) - 2  # Making sure to always have one free slot at the end.
            self.last_occupied += 1

        return index

    def get(self, index):
        return self.data[index]

    def modify(self, index, *args, **kwargs):
        self.data[index] = self.ConstructorClass(*args, **kwargs)

    def copy(self, index, component):
        self.data[index] = component

    def destroy(self, index):
        if not 0 <= index < self.last_occupied:
            if index == self.last_occupied:
                self.last_occupied -= 1
                return
            else:
                raise ValueError("Invalid index {}! Last occupied is {}.".format(index, self.last_occupied))

        last_occupied = self.last_occupied

        self.data[index], self.data[last_occupied] = self.data[last_occupied], self.data[index]
        self.last_occupied -= 1

        return last_occupied


class ComponentSetStorage:

    def __init__(self, *component_classes):
        self.mapping = {}           # For destruction
        self.component_array = {
            component_class.__name__ : SwitchArray(component_class) for component_class in component_classes
        }

    def create(self):
        previous_index = -1
        index = -1
        for name, array in self.component_array.items():
            index = array.create()
            assert index == previous_index or previous_index == -1, "All indices must be the same!"
            previous_index = index
        return index

    def get(self, index, Components=None):
        components = []
        if Components is None:
            for name, array in self.component_array.items():
                components.append(array.get(index))
            return components
        else:
            raise NotImplemented('Sorry')

    def modify(self, index, Component, *args, **kwargs):
        component_array = self.component_array[Component.__name__]
        component_array.modify(index, *args, **kwargs)

    def copy(self, index, Component, component):
        component_array = self.component_array[Component.__name__]
        component_array.copy(index, component)

    def destroy(self, index):
        indices = []
        for name, array in self.component_array.items():
            mapped_index = array.destroy(index)
            indices.append(mapped_index)

        for i in range(len(indices) - 1):
            assert indices[i] == indices[i+1], "Destruction not synchronized!"

        self.mapping[mapped_index] = index  # As it has now taken 'index' in the array.


class Entity:
    def __init__(self, component_set, index):
        self.component_set = component_set
        self.index = index


class World:

    def __init__(self):
        self.registered_components = [Transform, Renderable, PointLight, Physics]
        # TODO(ted): Should be dynamic and using a bitmask.
        self.component_sets = [
            frozenset((Transform,)), frozenset((Transform, Renderable)), frozenset((Transform, PointLight)),
            frozenset((Transform, Physics)), frozenset((Transform, Renderable, PointLight)),
            frozenset((Transform, Renderable, Physics)), frozenset((Transform, PointLight, Physics)),
            frozenset((Transform, Renderable, PointLight, Physics))
        ]

        # TODO(ted): Make it possible for user to set ComponentSetStorage.
        # TODO(ted): Don't create an entry for every possible combination. Use an hash table and create one when
        # necessary. Delete entries that are not used.
        self.data = [ComponentSetStorage(*component_set) for component_set in self.component_sets]

    def register_component(self, Component, Storage=ComponentSetStorage):
        self.registered_components.append(Component)
        self.data.append(Storage(Component))

    def create_entity(self):
        entity = Entity(frozenset(), 0)
        return entity

    def get_component_arrays_of(self, *Components):
        component_set_arrays = []

        component_target = frozenset(Components)
        for index, component_set in enumerate(self.component_sets):
            if component_target.intersection(component_set) == component_target:
                component_set_arrays.append(self.data[index])


        def temp(arrays):
            for array in arrays:
                for element in array:
                    yield element

        result = []
        for Component in Components:
            arrays = [component_set_array.component_array[Component.__name__] for component_set_array in component_set_arrays]
            result.append(temp(arrays))
        return result

    def add_component(self, entity, Component, *args, **kwargs):
        # Remove
        previous_components = []
        if entity.component_set:
            set_array_index = self.component_sets.index(entity.component_set)
            set_array = self.data[set_array_index]
            previous_components = set_array.get(entity.index)
            set_array.destroy(entity.index)

        # Create
        entity.component_set = entity.component_set.union(frozenset((Component,)))  # Union
        set_array_index = self.component_sets.index(entity.component_set)
        set_array = self.data[set_array_index]
        entity.index = set_array.create()
        for component in previous_components:
            set_array.copy(entity.index, component.__class__, component)

        set_array.modify(entity.index, Component, *args, **kwargs)

    def remove_component(self, entity, Component):
        # Remove
        previous_components = []
        if entity.component_set:
            set_array_index = self.component_sets.index(entity.component_set)
            set_array = self.data[set_array_index]
            previous_components = set_array.get(entity.index)
            set_array.destroy(entity.index)

        # Filter
        previous_components = [component for component in previous_components if type(component) != Component]

        # Create
        entity.component_set = entity.component_set.difference(frozenset((Component, )))  # Difference, not union.
        set_array_index = self.component_sets.index(entity.component_set)
        set_array = self.data[set_array_index]
        entity.index = set_array.create()
        for component in previous_components:
            set_array.copy(entity.index, component.__class__, component)




def main():
    world = World()

    a = world.create_entity()
    b = world.create_entity()
    c = world.create_entity()
    d = world.create_entity()

    world.add_component(b, Transform, location=(1, 1, 1), rotation=(1, 1, 1), scale=(2, 2, 2))
    arrays = world.get_component_arrays_of(Transform)

    world.add_component(a, Transform, location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1))
    arrays = world.get_component_arrays_of(Transform)

    world.add_component(a, PointLight, color=(1, 2, 3), attenuation=25)
    transforms, point_lights = world.get_component_arrays_of(Transform, PointLight)

    print('---- START ----')
    for x in zip(transforms, point_lights):
        print(x)
    print('----- END -----')

    world.add_component(b, PointLight, color=(4, 5, 6), attenuation=11)
    transforms, point_lights = world.get_component_arrays_of(Transform, PointLight)

    print('---- START ----')
    for x in zip(transforms, point_lights):
        print(x)
    print('----- END -----')

    world.remove_component(b, PointLight)
    transforms, point_lights = world.get_component_arrays_of(Transform, PointLight)

    print('---- START ----')
    for x in zip(transforms, point_lights):
        print(x)
    print('----- END -----')


if __name__ == '__main__':
    main()



"""
Plan for cache-friendliness. Each component will have it's own contiguous array of data. The * represents
an array.

Index: 0
* Transform, Transform, Transform, Transform, Transform, Transform, Transform, Transform, 

Index: 1
* Renderable, Renderable, Renderable, Renderable, Renderable, Renderable, Renderable, Renderable, 

Index: 2
* Physics, Physics, Physics, Physics, Physics, Physics, Physics, Physics, Physics, Physics, Physics,




"""
#
# from collections import namedtuple
#
# class ComponentArray:
#
#     def __init__(self, ComponentClass):
#         self.ComponentClass = ComponentClass
#         self.data = []
#         self.free = []
#
#     def create(self, *args, **kwargs):
#         component = self.ComponentClass(*args, **kwargs)
#
#         if self.free:
#             index = self.free.pop(0)
#             self.data[index] = component
#         else:
#             self.data.append(component)
#             index = len(self.data) - 1
#
#         return index
#
#     def destroy(self, index):
#         self.free.append(index)
#
#
# Entity     = namedtuple('Entity', 'id, indices')
# Transform  = namedtuple('Transforms', 'location, rotation, scale')
# Renderable = namedtuple('Renderable', 'program, model, textures')
#
#
# class World:
#
#     def __init__(self, *classes):
#         self.mapping = {type(class_): index for index, class_ in enumerate(classes)}
#         self.data = [ComponentArray(class_) for class_ in classes]
#         self.guid = 0
#
#
#     def get_component_arrays_of(self, *component_classes):
#         pass
#
#
#     def create_entity(self, mode='dynamic'):
#         self.guid += 1
#         entity = Entity(self.guid, [])
#         return entity
#
#     def destroy_entity(self, entity):
#         for array_index, component_index in entity.indices:
#             component_array = self.data[array_index]
#             component_array.destroy(component_index)
#
#     def add_component(self, entity, component_class, *args, **kwargs):
#         array_index = self.mapping[component_class]
#
#         component_array = self.data[array_index]
#         component_index = component_array.create(*args, **kwargs)
#
#         entity.indices.append((array_index, component_index))
#
#     def remove_component(self, entity, component_class):
#         target = self.mapping[type(component_class)]
#         for array_index, component_index in entity.indices:
#             if array_index == target:
#                 component_array = self.data[array_index]
#                 component_array.destroy(component_index)
#                 entity.indices.remove((array_index, component_index))
#                 return
#
#
#

