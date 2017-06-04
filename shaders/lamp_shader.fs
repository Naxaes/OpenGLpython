#version 120

// UPLOADED
uniform vec3 color;

void main()
{
    float addition = 1 - max(max(color.x, color.y), color.z);
    gl_FragColor = vec4(color + addition, 1.0);
}