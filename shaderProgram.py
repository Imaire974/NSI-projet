class ShaderProgram:
    def __init__(self, ctx):
        self.ctx = ctx
        self.programs = {}
        self.programs['default'] = self.get_program('default')
        self.programs['src'] = self.get_program('src')
        self.programs['postProcess'] = self.get_program('postProcess')
        self.programs['skybox'] = self.get_program('skybox')
        # self.programs['text'] = self.get_program('text')
        
    def get_program(self, shader_name):

        with open (f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()
        with open (f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program
    
    def destroy(self):
        [program.release() for program in self.programs.values()]