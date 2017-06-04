#version 120


struct Light {
    vec3 position;

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;

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
float attenuation(Light light, float distance);
vec3 ambient(Light light, Material material, vec2 coordinate);
vec3 diffuse(Light light, Material material, vec2 coordinate, vec3 normal, vec3 position);
vec3 specular(Light light, Material material, vec2 coordinate, vec3 normal, vec3 position, vec3 camera_position);


void main()
{
    vec3 normal_unit = normalize(pass_normal);
    vec3 camera_position = view[3].xyz;
    float distance = length(pass_world_position - light.position);
    float attenuation = attenuation(light, distance);


    // Ambient.
    vec3 ambient = ambient(light, material, pass_texture_coordinate);


    // Diffuse.
    vec3 diffuse = diffuse(light, material, pass_texture_coordinate, normal_unit, pass_world_position);


    // Specular.
    vec3 specular = specular(light, material, pass_texture_coordinate, normal_unit, pass_world_position, camera_position);


    // Emission.
    vec3 emission = vec3(0.0);
    if (texture2D(material.specular, pass_texture_coordinate).x == 0.0)
    {
        emission = texture2D(material.emission, pass_texture_coordinate).xyz * max(sin(time), 0.0);
    }

    specular *= attenuation;
    diffuse *= attenuation;
    ambient *= attenuation;

    gl_FragColor =  vec4(emission + specular + diffuse + ambient, 1.0);

}




float attenuation(Light light, float distance)
{
    return 1.0 / (light.constant + light.linear * distance + light.quadratic * distance * distance);
}

vec3 ambient(Light light, Material material, vec2 coordinate)
{
    return light.ambient * vec3(texture2D(material.diffuse, coordinate));
}

vec3 diffuse(Light light, Material material, vec2 coordinate, vec3 normal, vec3 position)
{
    vec3 light_direction = normalize(light.position - position);
    float diffuse_factor = max(dot(normal, light_direction), 0.0);
    return light.diffuse * diffuse_factor * vec3(texture2D(material.diffuse, coordinate));
}

vec3 specular(Light light, Material material, vec2 coordinate, vec3 normal, vec3 position, vec3 camera_position)
{
    vec3 light_direction = normalize(light.position - position);
    vec3 camera_direction = normalize(camera_position - position);
    vec3 reflection_direction = reflect(-light_direction, normal);
    float specular_factor = pow(max(dot(camera_direction, reflection_direction), 0.0), material.shininess);
    return light.specular * specular_factor * vec3(texture2D(material.specular, pass_texture_coordinate));
}