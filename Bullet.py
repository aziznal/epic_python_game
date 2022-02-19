import pygame
import os

from Settings import Settings

sets = Settings()

try:
    image = pygame.image.load(os.path.join("images",
                                           "fireball.png"))
    image = pygame.transform.scale(image, (sets.bullet_width,
                                   sets.bullet_height))
    print("fireball.png loaded successfully")
except FileNotFoundError:
    print("File Not Found")


class Bullet:
    def __init__(self, screen, shooter, x=0, y=0):
        self.x, self.y, self.screen, self.shooter = x, y, screen, shooter
        self.rect = pygame.Rect((self.x, self.y), (sets.bullet_width, sets.bullet_height))
        self.speed = sets.bullet_speed
        self.dir = self.shooter.dir
        if self.dir == 1:
            self.image = pygame.transform.flip(image, True, False)
        else:
            self.image = image
        self.image_rect = self.image.get_rect()

    def draw(self):
        self.image_rect.center = self.rect.center
        self.screen.blit(self.image, self.image_rect)

    def move(self):
        """
        Move bullet throughout the screen
        :return: None
        """
        self.rect.x += self.dir * self.speed

    def collide(self, player=None, objects=None, bullets=None):
        """
        Takes in objects or a player to collide with. Triggers other functions
        :param bullets: Objects bullet group
        :param objects: List of objects to collide with
        :param player: Player to collide with
        :return: None
        """

        # when it's an enemy collision
        if objects is not None:
            for obj in objects:
                if self.rect.colliderect(obj.rect):
                    try:
                        obj.health -= sets.bullet_damage
                        # play getting sfx
                        obj.hit_sfx.play()
                        bullets.remove(self)
                    except ValueError:
                        print("Double Enemy Bug")

        # when it's a player collision
        if player is not None:
            if self.rect.colliderect(player.rect):
                try:
                    player.health -= sets.bullet_damage
                    player.hit_sfx.play()
                    bullets.remove(self)
                except ValueError:
                    print("Bullet Player Collision Bug.")

    def check_bounds(self, bullets):
        """
        remove if self is out of bounds
        :param bullets: list of bullets
        :return: None
        """
        if self.rect.right < 0 or self.rect.left > sets.screen_width:
            try:
                bullets.remove(self)
                del self
            except ValueError:
                print("Bug: ValueError in bullet.check_bounds. Effect unknown")

    def update(self, player=None, objects=None, bullets=None):
        """
        pass the object(s) to be affected by the bullet ie: take damage
        :param player: pass if player is to take damage
        :param objects: pass as list if meant to take damage
        :param bullets: to remove bullets if collided
        :return: None
        """
        self.check_bounds(bullets)
        self.draw()
        self.collide(player, objects, bullets)
        self.move()
