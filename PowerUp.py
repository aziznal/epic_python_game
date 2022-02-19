import pygame
import random

from Settings import Settings
import Functions as fn

sets = Settings()
# todo: create multiple classes inheriting from this main one depending on their type


class PowerUp:
    def __init__(self, x, y, screen, type="RANDOM", spawn="RANDOM"):
        if spawn == "RANDOM":
            self.x = random.randint(100, sets.screen_width - 100)
        else:
            self.x = x

        if type == "RANDOM":
            self.type = random.choice(sets.powerup_types)

        self.y = -100

        self.screen, self.type, self.y = screen, type, y
        self.kill_me = False

        self.width, self.height = sets.powerup_w, sets.powerup_h
        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))

    def drop(self):
        if self.rect.top > sets.walking_plane_y:
            self.rect.y += sets.powerup_fall_speed
        else:
            self.kill_me = True

    def draw(self):
        pygame.draw.rect(self.screen, sets.black, self.rect)

    def update(self):
        print(self.rect.y)
        self.drop()
        self.draw()
