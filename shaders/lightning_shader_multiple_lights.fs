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

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;

    float inner_radius;
    float outer_radius;

    float constant;
    float linear;
    float quadratic;
};


struct Material {
    sampler2D diffuse;
    sampler2D specular;
    sampler2D emission;
    float shininess;
};


# define NUM_LIGHTS 4


// IN
varying vec3 pass_world_position;
varying vec3 pass_normal;
varying vec2 pass_texture_coordinate;


// UPLOADED
uniform mat4 view;                          // For extracting camera position.
uniform PointLight light[NUM_LIGHTS];
uniform Material material;
uniform float time;


// FUNCTIONS
float attenuation(PointLight light, float distance);
vec3 ambient(PointLight light, Material material, vec2 coordinate);
vec3 diffuse(PointLight light, Material material, vec2 coordinate, vec3 normal, vec3 position);
vec3 specular(PointLight light, Material material, vec2 coordinate, vec3 normal, vec3 position, vec3 camera_position);


void main()
{
    vec3 normal_unit = normalize(pass_normal);
    vec3 camera_position = -view[3].xyz;         // Camera is the inverted view location.


    float distance[NUM_LIGHTS];
    float attenuation[NUM_LIGHTS];
    for (int i = 0; i < NUM_LIGHTS; i++)
    {
        distance[i] = length(light[i].position - pass_world_position);
        attenuation[i] = attenuation(light[i], distance[i]);
    }


    vec3 ambient = vec3(0.0);
    vec3 diffuse = vec3(0.0);
    vec3 specular = vec3(0.0);
    for (int i = 0; i < NUM_LIGHTS; i++)
    {
        ambient += ambient(light[i], material, pass_texture_coordinate);
        ambient *= attenuation[i];

        diffuse += diffuse(light[i], material, pass_texture_coordinate, normal_unit, pass_world_position);
        diffuse *= attenuation[i];

        specular += specular(light[i], material, pass_texture_coordinate, normal_unit, pass_world_position, camera_position);
        specular *= attenuation[i];
    }


    // Emission.
    vec3 emission = vec3(0.0);
    if (texture2D(material.specular, pass_texture_coordinate).x == 0.0)
    {
        emission = texture2D(material.emission, pass_texture_coordinate).xyz * max(sin(time), 0.0);
    }

    gl_FragColor =  vec4(emission + specular + diffuse + ambient, 1.0);

}




float attenuation(PointLight light, float distance)
{
    return 1.0 / (light.constant + light.linear * distance + light.quadratic * distance * distance);
}

vec3 ambient(PointLight light, Material material, vec2 coordinate)
{
    return light.ambient * vec3(texture2D(material.diffuse, coordinate));
}

vec3 diffuse(PointLight light, Material material, vec2 coordinate, vec3 normal, vec3 position)
{
    vec3 light_direction = normalize(light.position - position);
    float diffuse_factor = max(dot(normal, light_direction), 0.0);
    return light.diffuse * diffuse_factor * vec3(texture2D(material.diffuse, coordinate));
}

vec3 specular(PointLight light, Material material, vec2 coordinate, vec3 normal, vec3 position, vec3 camera_position)
{
    vec3 light_direction = normalize(light.position - position);
    vec3 camera_direction = normalize(camera_position - position);
    vec3 reflection_direction = reflect(-light_direction, normal);
    float specular_factor = pow(max(dot(camera_direction, reflection_direction), 0.0), material.shininess);
    return light.specular * specular_factor * vec3(texture2D(material.specular, pass_texture_coordinate));
}