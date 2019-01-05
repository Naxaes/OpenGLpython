from collections import OrderedDict, namedtuple
from itertools import combinations, chain
from source.linear_algebra import *


# class Component:
#     def __repr__(self):
#         title = "\n{}:\n".format(self.__class__.__name__)
#         attribute_template = "\t{:<10} = {}"
#
#         return title + "\n".join(
#             [attribute_template.format(name, value) for name, value in self.__dict__.items()]
#         )


class Transform:
    def __init__(self, location, rotation, scale):
        self.location = Vector3(*location)
        self.rotation = Vector3(*rotation)
        self.scale    = Vector3(*scale)

    def matrix(self):
        return transformation_matrix(*self.location, *self.rotation, *self.scale)


class Renderable:
    def __init__(self, shader, model, *textures):
        self.shader   = shader
        self.model    = model
        self.textures = textures


class PointLight:
    def __init__(self, color, attenuation):
        self.color = color
        self.attenuation = attenuation


class Physics:
    def __init__(self, velocity, acceleration, max_speed):
        self.velocity = velocity
        self.acceleration = acceleration
        self.max_speed = max_speed


class Collidable:
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

class IComponentSetStorage:
    def create(self, *components):
        raise NotImplemented("Sorry...")

    def get(self, index, *Components):
        raise NotImplemented("Sorry...")

    def set(self, index, *components):
        raise NotImplemented("Sorry...")

    def destroy(self, index):
        raise NotImplemented("Sorry...")


class SwitchArray:

    def __init__(self, ConstructorClass):
        self.ConstructorClass = ConstructorClass
        self.data = [None]       # Making sure to always have one free slot.
        self.last_occupied = -1  # Index of first free slot

    def __iter__(self):
        return (self.data[i] for i in range(self.last_occupied + 1))

    def create(self, *elements):
        for element in elements:
            if 0 <= self.last_occupied < len(self.data)-2:
                index = self.last_occupied
                self.data[index] = element
                self.last_occupied += 1
            else:
                self.data.append(None)
                index = self.last_occupied + 1  # Making sure to always have one free slot at the end.
                self.data[index] = element
                self.last_occupied = index

        return index

    def get(self, index):
        return self.data[index]

    def set(self, index, data):
        self.data[index] = data

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



class SortedGroupComponentSetStorage(IComponentSetStorage):
    def __init__(self):
        pass

    def create(self, *components):
        raise NotImplemented("Sorry...")

    def get(self, index, *Components):
        raise NotImplemented("Sorry...")

    def set(self, index, *components):
        raise NotImplemented("Sorry...")

    def destroy(self, index):
        raise NotImplemented("Sorry...")


class GeneralComponentSetStorage(IComponentSetStorage):

    def __init__(self, *component_classes):
        self.mapping = {}           # When switching in destroy we need to map the last index to its new index.
        self.component_array = {
            component_class : SwitchArray(component_class) for component_class in component_classes
        }

    def create(self, *components):
        assert len(components) == len(self.component_array), "BAD! All must be initialized"
        previous_index = -1
        index = -1
        for component in components:
            array = self.component_array[component.__class__]
            index = array.create(component)
            assert index == previous_index or previous_index == -1, "All indices must be the same!"
            previous_index = index
        return index

    def get(self, index, *Components):
        components = []
        if not Components:
            for name, array in self.component_array.items():
                components.append(array.get(index))
            return components
        else:
            for Component in Components:
                components.append(self.component_array[Component])
            return components

    def set(self, index, *components):
        for component in components:
            component_array = self.component_array[component.__class__]
            component_array.modify(index, component)

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
        self.component_set = component_set  # TODO(ted): Should be bitmask instead.
        self.index = index


class World:

    def __init__(self):
        self.registered_components = [Transform, Renderable, PointLight, Physics]
        # TODO(ted): Should be dynamic and using a bitmask.
        # TODO(ted): Make it possible for user to set ComponentSetStorage.
        # TODO(ted): Don't create an entry for every possible combination. Use an hash table and create one when
        # necessary. Delete entries that are not used.
        self.component_sets = {
            # frozenset((Transform,)):                                 ComponentSetStorage(Transform),
            # frozenset((Transform, Renderable)):                      ComponentSetStorage(Transform, Renderable),
            # frozenset((Transform, PointLight)):                      ComponentSetStorage(Transform, PointLight),
            # frozenset((Transform, Physics)):                         ComponentSetStorage(Transform, Physics),
            # frozenset((Transform, Renderable, PointLight)):          ComponentSetStorage(Transform, Renderable, PointLight),
            # frozenset((Transform, Renderable, Physics)):             ComponentSetStorage(Transform, Renderable, Physics),
            # frozenset((Transform, PointLight, Physics)):             ComponentSetStorage(Transform, PointLight, Physics),
            # frozenset((Transform, Renderable, PointLight, Physics)): ComponentSetStorage(Transform, Renderable, PointLight, Physics),
        }

    def _get_or_create_set_array(self, entity):
        if entity.component_set not in self.component_sets:
            self.component_sets[entity.component_set] = GeneralComponentSetStorage(*entity.component_set)
        return self.component_sets[entity.component_set]

    def register_component(self, Component, Storage=GeneralComponentSetStorage):
        pass

    def get_component_arrays_of(self, *Components):
        component_set_arrays = []

        component_target = frozenset(Components)
        for component_set, component_set_array in self.component_sets.items():
            if component_target.intersection(component_set) == component_target:
                component_set_arrays.append(component_set_array)


        def temp(sequences):
            for sequence in sequences:
                for element in sequence:
                    yield element

        result = []
        for Component in Components:
            arrays = [component_set_array.component_array[Component] for component_set_array in component_set_arrays]
            result.append(temp(arrays))
        return zip(*result)



    def create_entity(self, *components):
        entity = Entity(frozenset(), 0)
        if components:
            self.add_components(entity, *components)
        return entity

    def destroy_entity(self, entity):
        if entity.component_set:
            set_array = self.component_sets[entity.component_set]
            set_array.destroy(entity.index)

    def add_components(self, entity, *components):
        # Remove
        previous_components = []
        if entity.component_set:
            set_array = self.component_sets[entity.component_set]
            previous_components = set_array.get(entity.index)
            set_array.destroy(entity.index)

        # Create
        component_set_to_add = frozenset(type(component) for component in components)
        entity.component_set = entity.component_set.union(component_set_to_add)  # Union

        set_array = self._get_or_create_set_array(entity)
        entity.index = set_array.create(*chain(previous_components, components))

    def remove_components(self, entity, *Components):
        # Remove
        previous_components = []
        if entity.component_set:
            set_array = self.component_sets[entity.component_set]
            previous_components = set_array.get(entity.index)
            set_array.destroy(entity.index)

        # Filter
        previous_components = [component for component in previous_components if type(component) not in Components]

        # Create
        component_set_to_remove = frozenset(Components)
        entity.component_set = entity.component_set.difference(component_set_to_remove)   # Difference

        set_array = self._get_or_create_set_array(entity)
        entity.index = set_array.create(*previous_components)




def main():
    world = World()

    a = world.create_entity()
    b = world.create_entity()
    c = world.create_entity(
        Transform(location=(5, 4, 22), rotation=(13, 2, 33), scale=(52, 1, 2)),
        PointLight(color=(2, 43, 5), attenuation=12)
    )

    world.add_components(b, Transform(location=(1, 1, 1), rotation=(1, 1, 1), scale=(2, 2, 2)))
    arrays = world.get_component_arrays_of(Transform)

    world.add_components(a, Transform(location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)))
    arrays = world.get_component_arrays_of(Transform)

    world.add_components(a, PointLight(color=(1, 2, 3), attenuation=25))
    entities = world.get_component_arrays_of(Transform, PointLight)

    print('---- START ----')
    for x in entities:
        print(x)
    print('----- END -----')

    world.add_components(b, PointLight(color=(4, 5, 6), attenuation=11))
    entities = world.get_component_arrays_of(Transform, PointLight)

    print('---- START ----')
    for x in entities:
        print(x)
    print('----- END -----')

    world.remove_components(b, PointLight)
    entities = world.get_component_arrays_of(Transform, PointLight)

    print('---- START ----')
    for x in entities:
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

