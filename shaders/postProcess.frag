#version 330 core

in vec2 texcoord;
out vec4 fragColor;

uniform sampler2D color_tex;
uniform sampler2D depth_tex;
uniform sampler2D normal_tex;

uniform vec2 VIEWPORT_SIZE;

uniform mat4 INV_VIEW_MATRIX;

uniform float depth_threshold = 0.05;           //  hint_range(0, 1)
uniform float reverse_depth_threshold = 0.25;   //  hint_range(0, 1)
uniform float normal_threshold = 0.6;           //  hint_range(0, 1)

uniform float darken_amount = 0.3;     //hint_range(0, 1, 0.01)
uniform float lighten_amount = 1.5;   //hint_range(0, 10, 0.01)

uniform vec3 normal_edge_bias = vec3(1, 1, 1);
uniform vec3 light_direction = vec3(-0.96, -0.18, 0.2);

const float zNear = 0.1;
const float zFar = 1000;

float fogDistanceEnd = 90;
float fogDistanceStart = 80;

float u_VignetteRadius = 0.7;
float u_VignetteStrength = 0.01;

float pixelSize = 4;

float getZDistance(vec2 uv) {
    return (zNear * zFar) / (zFar - texture(depth_tex, uv).r * (zFar - zNear));
}

vec3 fragment(vec2 SCREEN_UV) {
	float depth = getZDistance(SCREEN_UV);
	vec3 normal = texture(normal_tex, SCREEN_UV).xyz * 2.0 - 1.0;
	vec2 texel_size = (pixelSize + 3) / VIEWPORT_SIZE.xy;
	
	vec2 uvs[4];
	uvs[0] = vec2(SCREEN_UV.x, min(1.0 - 0.001, SCREEN_UV.y + texel_size.y));
	uvs[1] = vec2(SCREEN_UV.x, max(0.0, SCREEN_UV.y - texel_size.y));
	uvs[2] = vec2(min(1.0 - 0.001, SCREEN_UV.x + texel_size.x), SCREEN_UV.y);
	uvs[3] = vec2(max(0.0, SCREEN_UV.x - texel_size.x), SCREEN_UV.y);
	
	float depth_diff = 0.0;
	float depth_diff_reversed = 0.0;
	float nearest_depth = depth;
	vec2 nearest_uv = SCREEN_UV;
	
	float normal_sum = 0.0;
	for (int i = 0; i < 4; i++) {
		float d = getZDistance(uvs[i]);
		depth_diff += depth - d;
		depth_diff_reversed += d - depth;
		
		if (d < nearest_depth) {
			nearest_depth = d;
			nearest_uv = uvs[i];
		}
		
		vec3 n = texture(normal_tex, uvs[i]).xyz * 2.0 - 1.0;
		vec3 normal_diff = normal - n;
		
		// Edge pixels should yield to the normal closest to the bias direction
		float normal_bias_diff = dot(normal_diff, normal_edge_bias);
		float normal_indicator = smoothstep(-0.01, 0.01, normal_bias_diff);
		
		normal_sum += dot(normal_diff, normal_diff) * normal_indicator;
	}
	float depth_edge = step(depth_threshold, depth_diff);
	
	// The reverse depth sum produces depth lines inside of the object, but they don't look as nice as the normal depth_diff
	// Instead, we can use this value to mask the normal edge along the outside of the object
	float reverse_depth_edge = step(reverse_depth_threshold, depth_diff_reversed); 
	
	float indicator = sqrt(normal_sum);
	float normal_edge = step(normal_threshold, indicator - reverse_depth_edge);
	
	vec3 original = texture(color_tex, SCREEN_UV).rgb;
	vec3 nearest = texture(color_tex, nearest_uv).rgb;
	
	mat3 view_to_world_normal_mat = mat3(
            INV_VIEW_MATRIX[0].xyz, 
            INV_VIEW_MATRIX[1].xyz,
            INV_VIEW_MATRIX[2].xyz
	);
	float ld = dot((view_to_world_normal_mat * normal), normalize(light_direction));
	
	vec3 depth_col = nearest * darken_amount;
	vec3 normal_col = original * (ld > 0.0 ? darken_amount : lighten_amount);
	vec3 edge_mix = mix(normal_col, depth_col, depth_edge);
    
    // return edge_mix;
	return mix(original, edge_mix, (depth_edge > 0.0 ? depth_edge : normal_edge));
}

void main() {

    // Sample the color texture
    // vec4 color = texture(color_tex, texcoord);

    // Sample the depth texture (values typically range from 0 to 1)

    //float quadDepth = pow(linearDepth, 2.0);



    // Effet Ecran Incurvé CRT deformations

    
    vec2 center = vec2(0.5, 0.5);
    vec2 off_center = texcoord - center;

    off_center *= 1.0 + 0.9 * pow(abs(off_center.yx), vec2(4));

    vec2 texcoord2 = center+off_center;

    texcoord2 = texcoord; // test

    // ----------------------------------------------------------------


    // PIXELISATION

    texcoord2.y *= VIEWPORT_SIZE[1] / pixelSize;
    texcoord2.x *= VIEWPORT_SIZE[0] / pixelSize;
    texcoord2.xy = floor(texcoord2.xy);
    texcoord2.x /= VIEWPORT_SIZE[0] / pixelSize;
    texcoord2.y /= VIEWPORT_SIZE[1] / pixelSize;

    // ------------------

    // CHROMATIC ABERATION

    // float u_strength = 0.004 * (0.5 - texcoord2.x) / 0.5 + 0.001;
    float u_strength = 0;

    vec2 offsetR = vec2(-u_strength, 0.0);
    vec2 offsetB = vec2(u_strength, 0.0);
    
    // Sample each color channel separately with the calculated offsets
    float red = texture(color_tex, texcoord2 + offsetR).r; // Red channel
    float green = texture(color_tex, texcoord2).g; // Green channel (no offset)
    float blue = texture(color_tex, texcoord2 + offsetB).b; // Blue channel
    
    // Combine the color channels to form the final color
    vec4 color = vec4(red, green, blue, 1.0);

    // --------------------------




    // fog

    float zDistance = getZDistance(texcoord);

    float fog = (1 - (max(min(fogDistanceEnd, zDistance),fogDistanceStart) - fogDistanceStart) / (fogDistanceEnd - fogDistanceStart) );

    vec4 fogColor = vec4(0.2,0.2,0.2,1);

    // if (zDistance > fogDistanceStart) color = color * fog + fogColor * ( 1 - fog );

    // if (texture(depth_tex, texcoord).r == 1) color = vec4(0.08, 0.16, 0.18,1);
    
    // --------------------------



    // Vignette 

    // Calculate the distance from the center of the screen
    float distanceFromCenter = max(distance(texcoord, vec2(0.5, 0.5)) - 0.2, 0 );

    // Calculate the vignette effect
    float vignette = smoothstep(u_VignetteRadius, u_VignetteStrength, distanceFromCenter);

    vignette = 1;

    //----


    // float depth = 1- ((zFar / 10) - getZDistance(texcoord2)) / (zFar / 10);

    fragColor = vec4(fragment(texcoord2),1);

    fragColor = color * vignette;

    if (texcoord2.x > 1.0 || texcoord2.x < 0.0 ||
        texcoord2.y > 1.0 || texcoord2.y < 0.0){
        fragColor=vec4(0.0, 0.0, 0.0, 1.0);
    }

}