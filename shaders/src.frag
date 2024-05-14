#version 330

in vec2 texcoord;

out vec4 fragColor;

uniform sampler2D color_texture;

void main() {
    vec4 color = texture(color_texture, texcoord);
    fragColor = color;
}