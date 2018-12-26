#version 120


struct PointLight {
    vec3 position;

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;

    float constant;
    float linear;
    float quadratic;
};


struct SpotLight {
    vec3 position;
    vec3 direction;

    float inner_angle;
    float outer_angle;

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;

    float constant;
    float linear;
    float quadratic;
};


struct SunLight {
    vec3 direction;

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};


struct Material {
    sampler2D diffuse;
    sampler2D specular;
    sampler2D emission;
    float shininess;
};


# define NUM_POINT_LIGHTS 4


varying vec3 pass_world_position;
varying vec3 pass_normal;
varying vec2 pass_texture_coordinate;


uniform mat4 view;                                  // For extracting camera position.
uniform PointLight pointlight[NUM_POINT_LIGHTS];
uniform SpotLight spotlight;
uniform SunLight sunlight;
uniform Material material;


void main()
{


    gl_FragColor = texture2D(texture, texture_coordinate);
}