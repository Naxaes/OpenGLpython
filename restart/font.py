from restart.texture import Texture
import os

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
        self.texture = Texture(os.path.join(folder_path, texture_path))

    def create_text_quad(self, text, anchor_center=False):

        positions = []
        texture_coordinates = []
        indices = []

        cursor_x, cursor_y = 0, 0
        index = 0

        height = self.texture.height
        print(height)

        for character in text:
            info = self.characters[ord(character)]
            tx, ty = info['x'], info['y']
            tw, th = info['width'], info['height']
            x, y = cursor_x + info['xoffset'], cursor_y - info['yoffset']

            v = [
                x     , y,        # topleft
                x     , y - th,   # bottomleft
                x + tw, y - th,   # bottomright
                x + tw, y,        # topright
            ]
            t = [
                tx     , height - ty,        # topleft
                tx     , height - (ty + th), # bottomleft
                tx + tw, height - (ty + th), # bottomright
                tx + tw, height - ty         # topright
            ]
            i = [index, index + 1, index + 3, index + 3, index + 1, index + 2]

            positions.extend(v)
            texture_coordinates.extend(t)
            indices.extend(i)

            index += 4

            cursor_x += info['xadvance']

        # quad = Quad2D(
        #     [-1.0, 0.0, -1.0, -1.0, 0.0, -1.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 1.0, 0.0, 1.0, -1.0],
        #     [-1.0, 0.0, -1.0, -1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0],
        #     [0, 1, 3, 3, 1, 2, 4, 5, 7, 7, 5, 6]
        # )


        # Normalize
        max_value = max((self.texture.height, self.texture.width))
        print(max_value)

        if anchor_center:
            width = cursor_x
            offset = (width / 2) / max_value

            positions = [i / max_value - offset for i in positions]
        else:
            positions = [i / max_value for i in positions]

        texture_coordinates = [i / max_value for i in texture_coordinates]

        return positions, texture_coordinates, indices


# Font('../resources/fonts/arial.fnt')