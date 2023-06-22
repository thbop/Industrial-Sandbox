#version 330 core

uniform sampler2D tex;

in vec2 uvs;
out vec4 f_color;



void main() {
    vec3 texel = texture(tex, uvs).rgb;
    vec2 new_uvs = vec2(
        uvs.x,
        uvs.y
    );
    texel += vec3(texture(tex, new_uvs).r*0.5, 0.089, 0.09);
    f_color = vec4(texel*0.5, 1.0);
}