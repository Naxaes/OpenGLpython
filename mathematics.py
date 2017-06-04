import numpy
from math import cos, sin, tan, pi


def create_transformation_matrix(x, y, z, rx, ry, rz, sx, sy, sz):
    
    cos_rx = cos(rx)
    sin_rx = sin(rx)
    cos_ry = cos(ry)
    sin_ry = sin(ry)
    cos_rz = cos(rz)
    sin_rz = sin(rz)
    
    
    translation = numpy.array(
        ((1, 0, 0, x),
         (0, 1, 0, y),
         (0, 0, 1, z),
         (0, 0, 0, 1)), dtype=numpy.float32
    )

    rotation_x = numpy.array(
        ((1, 0, 0, 0),
         (0, cos_rx, -sin_rx, 0),
         (0, sin_rx,  cos_rx, 0),
         (0, 0, 0, 1)), dtype=numpy.float32
    )

    rotation_y = numpy.array(
        ((cos_ry, 0, sin_ry, 0),
         (0, 1, 0, 0),
         (-sin_ry, 0, cos_ry, 0),
         (0, 0, 0, 1)), dtype=numpy.float32
    )

    rotation_z = numpy.array(
        ((cos_rz, -sin_rz, 0, 0),
         (sin_rz,  cos_rz, 0, 0),
         (0, 0, 1, 0),
         (0, 0, 0, 1)), dtype=numpy.float32
    )

    scale = numpy.array(
        ((sx, 0, 0, 0),
         (0, sy, 0, 0),
         (0, 0, sz, 0),
         (0, 0, 0, 1)), dtype=numpy.float32
    )

    return translation @ rotation_x @ rotation_y @ rotation_z @ scale


def create_orthographic_matrix(left, right, bottom, top, near, far):
    a = 2 * near
    b = right - left
    c = top - bottom
    d = far - near

    return numpy.array(
        (
            (a / b, 0, (right + left) / b, 0),
            (0, a / c, (top + bottom) / c, 0),
            (0, 0, -(far + near) / d, -(2 * d) / d),
            (0, 0, -1, 0)
        ), dtype=numpy.float32
    )


def create_perspective_matrix(fov, aspect_ratio, near, far):
    top = near * tan((pi / 180) * (fov / 2))
    bottom = -top
    right = top * aspect_ratio
    left = -right

    return create_orthographic_matrix(left, right, bottom, top, near, far)
