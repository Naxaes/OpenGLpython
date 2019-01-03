#version 120

uniform mat4 transformation;
uniform mat4 perspective;
uniform mat4 view;
uniform vec3 color;

void main()
{
    gl_FragColor = vec4(color, 1.0);
}