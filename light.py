import glm

class Light:
    def __init__(self, position=(3,3,-3),color=(1,1,1),intensite=1):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)

        #intensités
        self.Ia = 0.2
        self.Id = 0.8 * self.color * intensite #diffuse
        self.Is = 0.7 * self.color * intensite #specular

        self.dirLightDirection = glm.vec3(1,-1,0)
        self.dirLightColot = glm.vec3(255, 245, 181)