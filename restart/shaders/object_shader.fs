#version 120

/*
Naming conventions:
    * vector    - A vector that might not be normalized.
    * direction - A vector that must be normalized.

    All vectors/directions are in relation to the object vertex if nothing else is specified.
    For example:
        'normal' is the normal of the vertex.
        'vector_to_light' is a non-normalized vector pointing from the vertex to the light.
        'direction_camera_to_light' is a normalized vector pointing from the camera to the light.
*/

struct Light {
    vec3  position;
    vec3  color;

    float constant;
    float linear;
    float quadratic;
};

const int NUM_LIGHTS = 4;

uniform sampler2D diffuse_texture;
uniform sampler2D specular_texture;

uniform Light light[NUM_LIGHTS];
uniform mat4  view;

varying vec3 out_position;
varying vec3 out_normal;
varying vec2 out_texture_coordinate;

void main()
{
    vec3 camera_position = -view[3].xyz;
    vec3 direction_to_camera = normalize(camera_position - out_position);

    vec3 diffuse_color = texture2D(diffuse_texture, out_texture_coordinate).xyz;
    vec3 specular_color = texture2D(specular_texture, out_texture_coordinate).xyz;

    vec3 ambient  = vec3(diffuse_color.xyz) * 0.2;
    vec3 diffuse  = vec3(0.0);
    vec3 specular = vec3(0.0);

    for (int i = 0; i < NUM_LIGHTS; i++) {

        vec3  vector_to_light = light[i].position - out_position;
        vec3  direction_to_light = normalize(vector_to_light);
        float distance_to_light  = length(vector_to_light);

        float attenuation = 1.0 / (light[i].constant + light[i].linear * distance_to_light + light[i].quadratic * distance_to_light * distance_to_light);

        vec3 light_color = light[i].color * attenuation;

        float angle_normal_and_light = dot(out_normal, direction_to_light);
        float diffuse_factor = clamp(angle_normal_and_light, 0.0, 1.0);        // or max(angle_normal_and_light, 1.0)
        diffuse += light_color * diffuse_color * diffuse_factor;

        vec3 light_reflection = reflect(-direction_to_light, out_normal);
        float specular_factor = clamp(dot(direction_to_camera, light_reflection), 0, 1);
        specular += light_color * specular_color * specular_factor;
    }

    gl_FragColor = vec4(ambient + diffuse + specular, 1.0);
}
