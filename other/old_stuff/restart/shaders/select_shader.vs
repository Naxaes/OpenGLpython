#version 120

uniform mat4 transformation;
uniform mat4 perspective;
uniform mat4 view;

attribute vec3 position;

void main()
{
    gl_Position =  perspective * view * transformation * vec4(position, 1.0);
}