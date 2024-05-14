from model import *

class Scene:
    def __init__(self, app) :
        self.app = app
        self.objects = []
        self.load()
        # skybox
        self.skybox = SkyBox(app)
    
    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object

        n,s = 30,2
        for X in range(-n,n,s):
            for Z in range (-n,n,s):
                add(Cube(app,pos=(X,-3,Z)))

        # add(Cat(app,pos=(0,5,0)))

    def render(self):
        for obj in self.objects:
            obj.render()
        self.skybox.render()

            