#version 120

uniform mat4 transformation;
uniform mat4 perspective;
uniform mat4 view;

attribute vec3 position;
attribute vec3 normal;
attribute vec2 texture_coordinate;

varying vec3 out_position;
varying vec3 out_normal;
varying vec2 out_texture_coordinate;

void main()
{
    // Vector should have 1.0 as w-component so the transformation matrix affects it properly, while directions
    // should have 0.0 as w-component so the transformation matrix doesn't affect it's location.
    // Since position is a vector, it should have 1.0 as w-component.
    // Since normal is a direction, it should have 0.0 as w-component.

    vec4 full_position = vec4(position, 1.0);
    vec4 full_normal   = vec4(normal, 0.0);

    vec4 world_position = transformation * full_position;
    vec4 world_normal   = transformation * full_normal;

    out_position = vec3(world_position);
    out_normal   = normalize(vec3(world_normal));
    out_texture_coordinate = texture_coordinate;

    gl_Position =  perspective * view * world_position;
}
