#version 120

attribute vec3 position;
attribute vec3 normal;
attribute vec3 texture_coordinate;


varying vec3 pass_world_position;
varying vec3 pass_normal;
varying vec3 pass_texture_coordinate;


uniform mat4 transform;
uniform mat4 view;
uniform mat4 projection;


void main()
{
    vec4 world_position = transform * vec4(position, 1.0);

    pass_world_position = world_position;
    pass_normal = normal;
    pass_texture_coordinate = texture_coordinate;

    gl_Position = projection * view * world_position;
}