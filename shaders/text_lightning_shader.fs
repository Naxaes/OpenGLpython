#version 120

# define NUM_LIGHTS 5


struct Light {

    uint mask[NUM_LIGHTS];

    vec3 position[NUM_LIGHTS];

    vec3 ambient[NUM_LIGHTS];
    vec3 diffuse[NUM_LIGHTS];
    vec3 specular[NUM_LIGHTS];

    float constant[NUM_LIGHTS];
    float linear[NUM_LIGHTS];
    float quadratic[NUM_LIGHTS];

    vec3 direction[NUM_LIGHTS];
    float inner_angle[NUM_LIGHTS];
    float outer_angle[NUM_LIGHTS];
};


struct Material {
    sampler2D diffuse;
    sampler2D specular;
    sampler2D emission;
    float shininess;
};


// IN
varying vec3 pass_world_position;
varying vec3 pass_normal;
varying vec2 pass_texture_coordinate;


// UPLOADED
uniform mat4 view;                          // For extracting camera position.
uniform Light light;
uniform Material material;
uniform float time;


// FUNCTIONS
float angle_attenuation(Light light, uint index, vec3 position, float distance);
float attenuation(Light light, uint index, float distance);
vec3 ambient(float ambient, Material material, vec2 coordinate);
vec3 diffuse(vec3 light_position, float diffuse, Material material, vec2 coordinate, vec3 normal, vec3 position);
vec3 specular(vec3 light_position, float specular, Material material, vec2 coordinate, vec3 normal, vec3 position, vec3 camera_position);


void main()
{
    vec3 normal_unit = normalize(pass_normal);
    vec3 camera_position = -view[3].xyz;         // Camera is the inverted view location.


    vec3 ambient  = vec3(0.0);
    vec3 diffuse  = vec3(0.0);
    vec3 specular = vec3(0.0);

    for (int i = 0; i < NUM_LIGHTS; i++)
    {
        float distance = length(light.position[i] - pass_world_position);
        if (light.mask[i] == 0)
        {
            float attenuation = attenuation(light, i, distance);
        }
        else
        {
            float angle_attenuation(light, i, pass_world_position, distance);
        }

        ambient += ambient(light.ambient[i], material, pass_texture_coordinate) * attenuation;
        diffuse += diffuse(light.position[i], light.diffuse[i], material, pass_texture_coordinate, normal_unit, pass_world_position) * attenuation;
        specular += specular(light.position[i], light.specular[i], material, pass_texture_coordinate, normal_unit, pass_world_position, camera_position) * attenuation;
    }

    gl_FragColor =  vec4(specular + diffuse + ambient, 1.0);

}


float angle_attenuation(Light light, uint index, vec3 position, float distance)
{
    vec3 direction_to_vertex = normalize(position - light.position[index]));
    float angle = acos(dot(direction_to_vertex, light.direction[index]));

    if (angle < light.inner_angle[index])
    {
        return 1.0 / (light.constant[index] + light.linear[index] * distance + light.quadratic[index] * distance * distance);
    }
    else if (angle >= light.outer_angle[index])
    {
        return 0;
    }
    else
    {
        return 1.0 / (light.constant[index] + light.linear[index] * distance + light.quadratic[index] * distance * distance);
        float factor = 1 - (angle - light.inner_angle[index]) / (light.outer_angle[index] - light.inner_angle[index]);
        return attenuation * factor;
    }

}


float attenuation(Light light, uint index, float distance)
{
    return 1.0 / (light.constant[index] + light.linear[index] * distance + light.quadratic[index] * distance * distance);
}

vec3 ambient(float ambient, Material material, vec2 coordinate)
{
    return ambient * vec3(texture2D(material.diffuse, coordinate));
}

vec3 diffuse(vec3 light_position, float diffuse, Material material, vec2 coordinate, vec3 normal, vec3 position)
{
    vec3 light_direction = normalize(light_position - position);
    float diffuse_factor = max(dot(normal, light_direction), 0.0);
    return diffuse * diffuse_factor * vec3(texture2D(material.diffuse, coordinate));
}

vec3 specular(vec3 light_position, float specular, Material material, vec2 coordinate, vec3 normal, vec3 position, vec3 camera_position)
{
    vec3 light_direction = normalize(light_position - position);
    vec3 camera_direction = normalize(camera_position - position);
    vec3 reflection_direction = reflect(-light_direction, normal);
    float specular_factor = pow(max(dot(camera_direction, reflection_direction), 0.0), material.shininess);
    return specular * specular_factor * vec3(texture2D(material.specular, pass_texture_coordinate));
}