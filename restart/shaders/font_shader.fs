#version 120

varying vec2 out_texture_coordinate;

uniform vec3 color;
uniform sampler2D font_atlas;

void main()
{
    float font_value = texture2D(font_atlas, out_texture_coordinate).a;

    gl_FragColor = vec4(color, font_value);
}