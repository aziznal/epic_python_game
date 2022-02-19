import pygame
from Settings import Settings

sets = Settings()

pygame.font.init()
font = pygame.font.SysFont(sets.font, sets.font_size)


class Bar:
    def __init__(self, obj, screen, x=1000, y=50, id="Health"):
        self.x, self.y, self.screen, self.obj, self.id = x, y, screen, obj, id
        self.font = font
        self.text = None

        if self.id == "Health":
            # Since Player's and Enemies' Bars are different:
            if self.obj.id == "Player":
                self.color = sets.health_color
                self.text = "Health"    # Only the player gets text on their bar
                self.rect = pygame.Rect((sets.pbar1_x, sets.pbar1_y), (sets.pbar1_w, sets.pbar1_h))
                self.rect_outline = pygame.Rect((sets.pbar1_x, sets.pbar1_y), (sets.pbar1_w, sets.pbar1_h))

            elif self.obj.id == "Enemy":
                self.color = sets.enemy_health_color
                self.rect = pygame.Rect((sets.ebar1_x, self.obj.rect.y - 20), (sets.ebar1_w, sets.ebar1_h))
                self.rect_outline = pygame.Rect((sets.ebar1_x, self.obj.rect.y - 20), (sets.ebar1_w, sets.ebar1_h))

        elif self.id == "Jump":
            self.text = "Stamina"
            self.color = sets.stamina_color
            self.rect = pygame.Rect((sets.pbar2_x, sets.pbar2_y), (sets.pbar2_w, sets.pbar2_h))
            self.rect_outline = pygame.Rect((sets.pbar2_x, sets.pbar2_y), (sets.pbar2_w, sets.pbar2_h))

        elif self.id == "Ammo":
            self.text = "Ammo"
            self.color = sets.red
            self.rect = pygame.Rect((sets.pbar3_x, sets.pbar3_y), (sets.pbar3_w, sets.pbar3_h))
            self.rect_outline = pygame.Rect((sets.pbar3_x, sets.pbar3_y), (sets.pbar3_w, sets.pbar3_h))

        if self.text is not None:
            self.rendered_text = self.font.render(self.text, True, sets.font_color)
            font_rect_size = pygame.font.Font.size(self.font, self.text)    # returns (width, height)
            self.rendered_text_rect = pygame.Rect((0, 0), (font_rect_size[0], font_rect_size[1]))

    def draw(self):
        # Since Enemies Move, bar moves with them
        if self.obj.id == "Enemy":
            # Adjusting x
            self.rect.centerx = self.obj.rect.centerx
            self.rect_outline.centerx = self.obj.rect.centerx
            self.rect.left = self.rect_outline.left
            # Adjusting y
            self.rect.y = self.obj.rect.y
            self.rect_outline.midleft = self.rect.midleft

        # Temp Code to draw things on screen
        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, sets.black, self.rect_outline, 2)

        # Blitting Out Text
        if self.text is not None:
            self.rendered_text_rect.center = self.rect_outline.center
            self.screen.blit(self.rendered_text, self.rendered_text_rect)

    def adjust(self):
        """
        Increase or Decrease bar's width depending
        on related value
        :return: None
        """
        if self.id == "Health":
            if self.obj.id == "Player":
                self.rect.width = sets.pbar1_w * self.obj.health / sets.player_health
            elif self.obj.id == "Enemy":
                if self.obj.sub_id == "Normal":
                    self.rect.width = sets.ebar1_w * self.obj.health / sets.enemy_health
                elif self.obj.sub_id == "Jumper":
                    self.rect.width = sets.ebar1_w * self.obj.health / sets.j_enemy_health

        elif self.id == "Jump":
            self.rect.width = sets.pbar2_w * self.obj.stamina / sets.player_stamina
            # Color the bar black when insufficient to jump
            if self.obj.stamina / sets.player_stamina < sets.stamina_drop / sets.player_stamina:
                self.color = sets.black
            else:
                self.color = sets.stamina_color

        elif self.id == "Ammo":
            self.rect.width = sets.pbar3_w * self.obj.ammo / sets.player_ammo

            # Color the bar black when insufficient to shoot
            if self.obj.ammo / sets.player_ammo <= sets.ammo_drop / sets.player_ammo:
                self.color = sets.black
            else:
                self.color = sets.ammo_color

    def update(self):
        self.adjust()
        self.draw()
