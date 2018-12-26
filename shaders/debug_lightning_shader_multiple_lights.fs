#version 120

# define NUM_POINT_LIGHTS 4


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


// IN
varying vec3 pass_world_position;
varying vec3 pass_normal;
varying vec2 pass_texture_coordinate;


// UPLOADED
uniform mat4 view;                          // For extracting camera position.
uniform PointLight light[NUM_POINT_LIGHTS];
uniform SpotLight spotlight;
uniform SunLight sunlight;
uniform Material material;
uniform float time;


// FUNCTIONS
float spotlight_attenuation(SpotLight light, vec3 position, float distance);
float pointlight_attenuation(PointLight light, float distance);
vec3 ambient(vec3 ambient, Material material, vec2 coordinate);
vec3 diffuse(vec3 light_position, vec3 light_diffuse, Material material, vec2 coordinate, vec3 normal, vec3 position);
vec3 specular(vec3 light_position, vec3 light_specular, Material material, vec2 coordinate, vec3 normal, vec3 position, vec3 camera_position);

vec3 calculate_pointlight(PointLight light, Material material, vec3 position, vec3 normal, vec2 texture_coordinate);
vec3 calculate_spotlight(SpotLight light, Material material, vec3 position, vec3 normal, vec2 texture_coordinate);
vec3 calculate_sunlight(SunLight light, Material material, vec3 normal, vec2 texture_coordinate);


void main()
{
    vec3 normal_unit = normalize(pass_normal);
    vec3 camera_position = -view[3].xyz;         // Camera is the inverted view location.


    float attenuation;
    float distance;

    vec3 ambient  = vec3(0.0);
    vec3 diffuse  = vec3(0.0);
    vec3 specular = vec3(0.0);
    vec3 total_light = vec3(0.0);


    // Pointlight calculations.
    for (int i = 0; i < NUM_POINT_LIGHTS; i++)
    {
        total_light += calculate_pointlight(light[i], material, pass_world_position, pass_normal, pass_texture_coordinate);
    }


    // Spotlight calculations.
    total_light += calculate_spotlight(spotlight, material, pass_world_position, pass_normal, pass_texture_coordinate);


    // Sunlight calculations
    total_light += calculate_sunlight(sunlight, material, pass_normal, pass_texture_coordinate);


    gl_FragColor =  vec4(total_light, 1.0);


}



vec3 calculate_pointlight(PointLight light, Material material, vec3 position, vec3 normal, vec2 texture_coordinate)
{

    vec3  light_direction = normalize(light.position - position);
    vec3  camera_position = -view[3].xyz;

    // Attenuation
    float distance = length(light.position - position);
    float attenuation = 1.0 / (light.constant + light.linear * distance + light.quadratic * distance * distance);

    // Ambient
    vec3 ambient = light.ambient * vec3(texture2D(material.diffuse, texture_coordinate));

    // Diffuse
    float diffuse_factor = max(dot(normal, light_direction), 0.0);
    vec3  diffuse = light.diffuse * diffuse_factor * vec3(texture2D(material.diffuse, texture_coordinate));

    // Specular
    vec3  camera_direction = normalize(camera_position - position);
    vec3  reflection_direction = reflect(-light_direction, normal);
    float specular_factor = pow(max(dot(camera_direction, reflection_direction), 0.0), material.shininess);
    vec3  specular = light.specular * specular_factor * vec3(texture2D(material.specular, texture_coordinate));

    return (ambient + diffuse + specular) * attenuation;
}


vec3 calculate_spotlight(SpotLight light, Material material, vec3 position, vec3 normal, vec2 texture_coordinate)
{

    // This function assumes the presence of a uniform named 'view' that's the view matrix.


    // 'angle' is the cosine of the angle between the vector from the light to the vertex position and the direction
    // of the spotlight.
    float angle = dot(normalize(position - light.position), normalize(light.direction));
    float outer_angle = cos(light.outer_angle);
    float inner_angle = cos(light.inner_angle);

    // The cosine of an angle in range 0 to 90 will have a value of 1 to 0, hence the 'greater than' operator instead of
    // 'lesser than' operator.
    if (angle > outer_angle)
    {
        vec3 vector_to_light = light.position - position;
        vec3 direction_to_light = normalize(vector_to_light);
        vec3 diffuse_color = vec3(texture2D(material.diffuse, texture_coordinate));
        vec3 specular_color = vec3(texture2D(material.specular, texture_coordinate));

        // If 'angle' is equal to 'inner_angle' then the numerator and denominator is equal, resulting to 1.
        // If 'angle' is grater than 'inner_angle' then the numerator is bigger and denominator smaller, resulting in
        // values greater than 1.
        // If 'angle' is less than 'inner_angle' then the numerator is smaller and denominator is greater, resulting
        // in values less than 1.
        float intensity = clamp((angle - outer_angle) / (inner_angle - outer_angle), 0.0, 1.0);
        float distance = length(vector_to_light);
        float attenuation = 1.0 / (light.constant + light.linear * distance + light.quadratic * distance * distance);

        // Ambient
        vec3 ambient = light.ambient * diffuse_color;

        // Diffuse
        float diffuse_factor = max(dot(normal, direction_to_light), 0.0);
        vec3 diffuse = light.diffuse * diffuse_color * diffuse_factor;

        // Specular
        vec3 camera_position = -view[3].xyz;
        vec3 camera_direction = normalize(camera_position - position);
        vec3 reflection_direction = reflect(-direction_to_light, normal);
        float specular_factor = pow(max(dot(camera_direction, reflection_direction), 0.0), material.shininess);
        vec3 specular = light.specular * specular_color * specular_factor;

        return (ambient + diffuse + specular) * attenuation * intensity;
    }
    else
    {
        return vec3(0.0);
    }

}



vec3 calculate_sunlight(SunLight light, Material material, vec3 normal, vec2 texture_coordinate)
{
    float attenuation = max(dot(normalize(-light.direction), normal), 0.0);
    vec3  ambient     = sunlight.ambient  * vec3(texture2D(material.diffuse,  texture_coordinate));
    vec3  diffuse     = sunlight.diffuse  * vec3(texture2D(material.diffuse,  texture_coordinate));
    vec3  specular    = sunlight.specular * vec3(texture2D(material.specular, texture_coordinate));

    return (ambient + diffuse + specular) * attenuation;
}


