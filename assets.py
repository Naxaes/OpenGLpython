import os
import pyglet
from vbo import load_model, create_square

join_path = os.path.join


RESOURCE_PATH = join_path(os.getcwd(),   'resources')
MODEL_PATH    = join_path(RESOURCE_PATH, 'models')
SOUND_PATH    = join_path(RESOURCE_PATH, 'sounds')
MUSIC_PATH    = join_path(RESOURCE_PATH, 'music')
TEXTURE_PATH  = join_path(RESOURCE_PATH, 'textures')


default_model   = load_model(join_path(MODEL_PATH, 'cube.obj'))
default_texture = pyglet.image.load(join_path(TEXTURE_PATH, 'NoTexture.png')).get_texture()

models   = [default_model]
textures = [default_texture]

models.extend(
    load_model(join_path(MODEL_PATH, path)) for path in os.listdir(MODEL_PATH) if path != 'cube.obj'
)

textures.extend(
    pyglet.image.load(join_path(TEXTURE_PATH, path)).get_texture() for path in os.listdir(TEXTURE_PATH) if path != 'NoTexture.png'
)


sounds = [

]


models.append(create_square((-10, -10, -10), (-10, -10, 10), (10, -10, -10), (10, -10, 10), (0, 1, 0)))