#version 330 core
in vec3 in_position;
in vec2 in_texcoord;
out vec2 texcoord;
void main() {
    gl_Position = vec4(in_position, 1.0);
    texcoord = in_texcoord;
}