#version 330 core

out vec4 fragColor;

in vec4 clipCoords;

uniform samplerCube u_texture_skybox;
uniform mat4 m_invProjView;
uniform mat4 m_invProjViewWorld;
uniform vec3 lightDir;


void main() {

    vec4 skyBoxRelativeCoords = m_invProjView * clipCoords;

    vec4 worldCoord = normalize(m_invProjViewWorld * clipCoords);

    vec3 texCubeCoords =  normalize(skyBoxRelativeCoords.xyz / skyBoxRelativeCoords.w);

    vec4 color = texture(u_texture_skybox,texCubeCoords);

    fragColor = color;
}

