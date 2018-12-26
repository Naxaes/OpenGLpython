#version 120

uniform mat3 transformation;

attribute vec2 position;
attribute vec2 texture_coordinate;

varying vec2 out_texture_coordinate;


void main()
{
    out_texture_coordinate = texture_coordinate;
    gl_Position =  vec4(position, 0.0, 1.0);
}