#version 120


// IN
attribute vec3 position;
attribute vec3 normal;
attribute vec2 texture_coordinate;


// UPLOADED
uniform mat4 transform;
uniform mat4 view;
uniform mat4 projection;


// OUT
varying vec3 pass_world_position;
varying vec3 pass_normal;
varying vec2 pass_texture_coordinate;


void main()
{
    pass_world_position = vec3(transform * vec4(position, 1.0));
    pass_normal = vec3(transform * vec4(normal, 0.0));  // Since normal is a direction, it should have 0.0.
    pass_texture_coordinate = texture_coordinate;

    gl_Position = projection * view * vec4(pass_world_position, 1.0);
}
