import pygame


class Cloud:
    def __init__(self, x, y, screen):
        self.image = None
        self.screen = screen
        self.rect = pygame.Rect((x, y), (1, 1)) # w & h changed later

    def draw(self):
        pass

    def update(self):
        pass
