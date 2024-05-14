from vbo import VBO
from shaderProgram import ShaderProgram

class VAO:
    def __init__(self, ctx) :
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}

        #cube VAO
        self.vaos['cube'] = self.get_vao(program = self.program.programs['default'],
                                         vbo     = self.vbo.vbos['cube']           )
        
        #cat VAO
        self.vaos['cat'] = self.get_vao(program = self.program.programs['default'],
                                         vbo     = self.vbo.vbos['cat']           )
        #skybox VAO
        self.vaos['skybox'] = self.get_vao(program = self.program.programs['skybox'],
                                         vbo     = self.vbo.vbos['skybox']           )

    def get_vao(self, program,vbo):
        vao = self.ctx.vertex_array(program,[(vbo.vbo,vbo.format, *vbo.attribs)])
        return vao
    
    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()