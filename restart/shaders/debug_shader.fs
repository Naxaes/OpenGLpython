#version 120

varying vec2 out_texture_coordinate;

uniform vec3 color;

void main()
{
    gl_FragColor = vec4(color, 1.0);
}