#version 330 core

in vec4 fPos;
in vec2 fTexCoord0;

layout (location = 0) out vec4 fColor;

uniform sampler2D TexDepthStencil;
uniform sampler2D TexDeferred;

uniform sampler2D p3d_Texture0;

void main()
{
    vec3 fPos_clip = fPos.xyz / fPos.w;
    vec2 fTexCoord1 = fPos_clip.xy * 0.5 + 0.5;

    vec4 Forward = texture(p3d_Texture0, fTexCoord0);
    vec4 Deferred = texture(TexDeferred, fTexCoord1);
    float fDepth = texture(TexDepthStencil, fTexCoord1).r;

    fColor = (fPos_clip.z * 0.5 + 0.5 < fDepth)? Forward : Deferred;
}
