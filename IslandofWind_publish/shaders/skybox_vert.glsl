#version 330 core

in vec4 p3d_Vertex;

out vec3 fTexCoord;
out vec4 fPos;

uniform mat4 p3d_ViewMatrix;
uniform mat4 p3d_ProjectionMatrix;

void main()
{
    fTexCoord = vec3(p3d_Vertex);

    mat4 View = mat4(mat3(p3d_ViewMatrix));
    vec4 pos = p3d_ProjectionMatrix * View * p3d_Vertex;
    fPos = pos;

    gl_Position = pos.xyww;
}
