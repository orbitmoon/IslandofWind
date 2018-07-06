#version 330 core

in vec3 fTexCoord;
in vec4 fPos;

out vec4 fColor;

uniform samplerCube TexSkybox;

uniform sampler2D TexDepthStencil;
uniform sampler2D TexDeferred;

void main()
{
	vec3 fPos_clip = fPos.xyz / fPos.w;
    vec2 fTexCoord1 = fPos_clip.xy * 0.5 + 0.5;

    vec4 Forward = texture(TexSkybox, fTexCoord);
    vec4 Deferred = texture(TexDeferred, fTexCoord1);
    float fDepth = texture(TexDepthStencil, fTexCoord1).r;

    fColor = (fDepth >= 1.0)? Forward : Deferred;
}
