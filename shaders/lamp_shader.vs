#version 120

// IN
attribute vec3 position;


// UPLOADED
uniform mat4 transform;
uniform mat4 view;
uniform mat4 projection;


void main()
{
    gl_Position = projection * view * transform * vec4(position, 1.0);
}