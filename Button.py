import pygame
import os

from Settings import Settings
from TextObject import TextObject

# todo: add a built in delay that stops the button from being spammed

pygame.mixer.init()

sets = Settings()

button_images = [pygame.image.load(os.path.join("images", "Button_inf1.png")),
                 pygame.image.load(os.path.join("images", "Button_inf2.png"))]

button_sounds = [pygame.mixer.Sound(os.path.join("sounds", "sound.wav"))]

button_sounds[0].set_volume(0.01)
button_sounds[0].play()

for x in range(0, len(button_images)):
    button_images[x] = pygame.transform.scale(button_images[x], (200, 100))


class Button:
    def __init__(self, x, y, w, h, screen, text=None, imaged=False, textcolor=sets.black, text_size=25):
        self.x, self.y, self.w, self.h, self.screen = x, y, w, h, screen
        self.whf = self.w / self.h  # width-to-height factor
        self.color = sets.green

        self.imaged = imaged
        if self.imaged:
            self.image_inf = button_images[1]
            self.image_def = button_images[0]
            self.w, self.h = self.image_def.get_size()
            print(str(self.w) + ", " + str(self.h))

        self.rect = pygame.Rect(self.x, self.h, self.w, self.h)

        # correcting rect boundaries
        if self.imaged:
            self.rect.w -= self.w * 20 / 100
            self.rect.h -= self.h * 40 / 100

        self.rect.center = (self.x, self.y)

        if not self.imaged:
            self.infl_factor = sets.infl_factor

        self.clicked = False
        self.collided = False
        self.is_being_clicked = False

        self.click_delay1 = 0
        self.click_delay2 = 0

        if text is not None:
            self.text = TextObject(self.screen, text=text, size=text_size, color=textcolor)
            self.text.rect.center = self.rect.center

    def check_collision(self):
        """ checks to see if mouse pointer is within button bounds """
        mpos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mpos[0], mpos[1]):
            self.collided = True
        # else:
        #     self.collide = False

    def select(self):
        if not self.imaged:
            """ Inflates the button all over """
            self.rect.width = self.w + self.infl_factor
            self.rect.height = self.h + self.infl_factor / self.whf
            self.color = sets.blue
            # Recenter rect:
            self.rect.centerx = self.x
            self.rect.centery = self.y
        else:
            # temp_rect segment is to keep button centered
            temp_rect = self.image_def.get_rect()
            temp_rect.center = self.rect.center
            self.screen.blit(self.image_inf, temp_rect)

    def deselect(self):
        if not self.imaged:
            """ Inverts what the select() method does """
            self.rect.width = self.w
            self.rect.height = self.h
            self.rect.center = (self.x, self.y)
            self.color = sets.green
        else:
            # temp_rect segment is to keep button centered
            temp_rect = self.image_def.get_rect()
            temp_rect.center = self.rect.center
            self.screen.blit(self.image_def, temp_rect)

    def draw(self):
        if not self.imaged:
            pygame.draw.rect(self.screen, self.color, self.rect)
            pygame.draw.rect(self.screen, sets.black, self.rect, 3)  # Outline

        self.text.rect.center = self.rect.center

    def check_click(self):
        if self.collided and pygame.mouse.get_pressed() == sets.mouse1 and not self.is_being_clicked:
            self.is_being_clicked = True
            self.clicked = True

    def check_mouse_state(self):
        """
        helper function to check if mouse was pressed on the switch the previous frame
        :return: None
        """
        if pygame.mouse.get_pressed() != sets.mouse1:
            self.is_being_clicked = False

        if pygame.mouse.get_pressed() == sets.mouse1 and not self.collided:
            self.is_being_clicked = True

    def update(self):

        self.clicked = False
        self.collided = False

        self.draw()
        self.check_collision()
        self.check_mouse_state()
        self.check_click()

        if self.collided:
            self.select()
        else:
            self.deselect()

        # text
        if self.text is not None:
            self.text.update()
