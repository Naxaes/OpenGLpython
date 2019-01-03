import os
from source.texture import load_texture
from source.model import Model, VBO, IBO


def load_font(path):
    raise NotImplemented('Sorry...')


class Font:

    def __init__(self, path):
        self.characters = {}
        texture_path = None

        for line in open(path):
            if line.startswith('page '):
                for statement in line.split(' '):
                    if statement.startswith('file'):
                        texture_path = statement.split('=')[-1].replace('"', '', 2).replace('\n', '')
            elif line.startswith('common '):
                pass
            elif line.startswith('char '):
                character_attributes = {}
                for statement in line.split(' '):
                    if '=' in statement:
                        attribute, value = statement.split('=')
                        character_attributes[attribute] = int(value)

                        if 'id=' in statement:
                            self.characters[int(value)] = character_attributes

        assert texture_path, 'Could not find the texture!'
        folder_path = os.path.split(path)[0]
        self.texture = load_texture(os.path.join(folder_path, texture_path))


    def text_model(self, text, anchor_center=False):

        positions = []
        texture_coordinates = []
        indices = []

        cursor_x, cursor_y = 0, 0
        index = 0

        height = self.texture.height

        for character in text:
            info = self.characters[ord(character)]
            tx, ty = info['x'], info['y']
            tw, th = info['width'], info['height']
            x, y = cursor_x + info['xoffset'], cursor_y - info['yoffset']

            v = [
                x, y,  # topleft
                x, y - th,  # bottomleft
                   x + tw, y - th,  # bottomright
                   x + tw, y,  # topright
            ]
            t = [
                tx, height - ty,  # topleft
                tx, height - (ty + th),  # bottomleft
                    tx + tw, height - (ty + th),  # bottomright
                    tx + tw, height - ty  # topright
            ]
            i = [index, index + 1, index + 3, index + 3, index + 1, index + 2]

            positions.extend(v)
            texture_coordinates.extend(t)
            indices.extend(i)

            index += 4

            cursor_x += info['xadvance']

        # Normalize
        max_value = max((self.texture.height, self.texture.width))

        if anchor_center:
            width = cursor_x
            offset = (width / 2) / max_value
            positions = [i / max_value - offset for i in positions]
        else:
            positions = [i / max_value for i in positions]

        texture_coordinates = [i / max_value for i in texture_coordinates]


        positions = VBO.create(positions, dimension=2)
        texture_coordinates = VBO.create(texture_coordinates, dimension=2)
        indices = IBO.create(indices)

        return Model.create(vbos=(positions, texture_coordinates), ibo=indices)

