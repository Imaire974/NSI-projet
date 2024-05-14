#version 330 core

layout (location = 0) out vec4 fragColor;
layout (location = 1) out vec3 fragNormal;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;


struct DirLight {
    vec3 direction;
    vec3 color;
  
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};  

struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform DirLight dirLight;
// uniform Light light;
uniform sampler2D u_texture_0;
uniform vec3 camPos;


vec3 CalcDirLight(DirLight light, vec3 normal, vec3 viewDir)
{
    vec3 lightDir = normalize(-light.direction);
    vec3 lightColor = normalize(light.color);

    // diffuse shading
    float diff = max(dot(normal, lightDir), 0.0);
    // specular shading
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 16);
    // combine results
    vec3 ambient  = light.ambient;
    vec3 diffuse  = light.diffuse  * diff ;
    vec3 specular = light.specular * spec ;
    return (ambient + diffuse + specular) * lightColor;
}  

// vec3 getLight(vec3 color) {
    // vec3 Normal = normalize(normal);

    // // ambient light
    // vec3 ambient = light.Ia;

    // // diffuse light
    // vec3 lightDir = normalize(light.position - fragPos);
    // float diff = max(0, dot(lightDir, Normal));
    // vec3 diffuse = diff * light.Id;

    // // specular light
    // vec3 reflectDir = reflect(-lightDir, Normal);
    // float spec = pow(max(dot(viewDir, reflectDir), 0), 32);
    // vec3 specular = spec * light.Is;

    // return color * (ambient + (diffuse + specular));
// }


void main() {
    float gamma = 2.2;

    vec3 color = texture(u_texture_0, uv_0).rgb;
    vec3 viewDir = normalize(camPos - fragPos);
    vec3 Normal = normalize(normal);
    
    // color = pow(color, vec3(gamma));

    // color = getLight(color);

    // color = pow(color, 1 / vec3(gamma));

    vec3 mapped_normal = (normalize(normal) + 1.0) / 2.0;

    fragNormal = mapped_normal;

    fragColor = vec4(CalcDirLight(dirLight,Normal,viewDir)*color, 1.0);
}