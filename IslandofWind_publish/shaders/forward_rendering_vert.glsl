#version 330 core

in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;

out vec4 fPos;
out vec2 fTexCoord0;

uniform mat4 p3d_ModelViewProjectionMatrix;

void main()
{
    fPos = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    fTexCoord0 = p3d_MultiTexCoord0;
    gl_Position = fPos;
}
