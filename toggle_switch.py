import pygame
import os

from Settings import Settings

sets = Settings()

# region loading images/sounds
image_on = pygame.image.load(os.path.join("images", "toggle_switch_on.png"))
image_off = pygame.image.load(os.path.join("images", "toggle_switch_off.png"))

img_ratio = image_on.get_rect().h / image_on.get_rect().w

image_on = pygame.transform.scale(image_on, (int(sets.t_switch_def_size),
                                             int(sets.t_switch_def_size * img_ratio)))

image_off = pygame.transform.scale(image_off, (int(sets.t_switch_def_size),
                                               int(sets.t_switch_def_size * img_ratio)))


# todo: add sound effects to switch toggling on or off
# endregion


class ToggleSwitch:
    def __init__(self, screen, x=sets.screen_width / 2, y=sets.screen_height / 2, toggled=False):
        """
        :param screen: screen to output image to
        :param x: x pos of switch
        :param y: y pos of switch
        :param toggled: True if on by default and vice-versa
        """
        self.screen, self.x, self.y = screen, x, y
        self.width, self.height = image_on.get_size()
        self.img_on = image_on
        self.img_off = image_off
        self.toggled = toggled
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # self.rect = self.rect.inflate(-int(self.width*0.25), -int(self.height*0.25))
        self.collided = False
        self.is_being_clicked = False

    def draw(self):
        if self.toggled:

            self.screen.blit(self.img_on, self.rect)
        else:
            self.screen.blit(self.img_off, self.rect)

        # pygame.draw.rect(self.screen, sets.black, self.rect, 3)

    def check_collision(self):
        mpos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mpos[0], mpos[1]):
            self.collided = True

    def check_click(self):
        if self.collided and pygame.mouse.get_pressed() == sets.mouse1 and not self.is_being_clicked:
            self.is_being_clicked = True
            self.toggled = not self.toggled

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
        self.collided = False
        self.draw()
        self.check_collision()
        self.check_mouse_state()
        self.check_click()
