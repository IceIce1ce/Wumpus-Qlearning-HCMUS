import pygame
class Images:
    def __init__(self):
        self.images = dict()
        self.dir = "resources/images/"

    def get(self, path):
        image = self.images.get(path)
        if (image == None):
            image = pygame.image.load(self.dir + path)
            self.images[path] = image
        return image
