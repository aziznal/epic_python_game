import pygame
import os
import random

import Functions as fn

from Settings import Settings
from Bar import Bar
from Bullet import Bullet

sets = Settings()

# region sound fx
walking_sfx = pygame.mixer.Sound(os.path.join("Sounds", "enemy_step.wav"))
hit_sfx = pygame.mixer.Sound(os.path.join("Sounds", "enemy_hit.wav"))
shooting_sfx = pygame.mixer.Sound(os.path.join("Sounds", "enemy_shoot.wav"))

dying_sfx = []
for x in range(1, 4):
    dying_sfx.append(pygame.mixer.Sound(os.path.join("Sounds",
                                                     "enemy_death" + str(x) + ".wav")))

# endregion

# region enemy images loading

# region main enemy images
main_images = []
img_max_ = 10
for x in range(3, img_max_ + 3):
    try:
        f = pygame.image.load(os.path.join("images",
                                           "enm" + str(x) + ".png"))
    except FileNotFoundError:
        f = None
    if f is not None:
        main_images.append(f)

# resizing images to correct size (aspect ratio = 0.632)
if True:
    for image in range(0, len(main_images)):
        main_images[image] = pygame.transform.scale(main_images[image],
                                                    (107, 169))
# endregion

# region jumper enemy images
jumper_images = []
for x in range(1, 11):
    temp_image = pygame.transform.scale(pygame.image.load(os.path.join("images", "j_enm" + str(x) + ".png")),
                                        (107, 169))
    jumper_images.append(temp_image)
# endregion

# endregion


class Enemy:
    def __init__(self, screen, x=450, y=sets.walking_plane_y):
        self.id = "Enemy"
        self.sub_id = "Normal"

        self.x, self.y, self.screen = x, y, screen

        self.images = main_images[:]

        self.current_image = 0
        self.animation_timer = 0

        self.dead = False
        self.death_animation_timer = 0

        self.width, self.height = self.images[0].get_rect().size
        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))
        self.rect.bottom = self.y

        self.speed = sets.enemy_speed
        self.reaction_delay = 0

        self.dir = 1

        self.health = sets.enemy_health
        self.health_bar = Bar(self, self.screen)

        self.bullets = []
        self.shooting_delay = sets.enemy_shoot_delay

        # region Sound fx
        self.walking_sfx = walking_sfx
        self.walking_sfx.set_volume(0.06)
        self.walk_sfx_timer = 0

        self.hit_sfx = hit_sfx

        self.shooting_sfx = shooting_sfx
        self.shooting_sfx.set_volume(0.5)

        self.dying_sfx = dying_sfx[:]
        # endregion

    def move(self, player):
        """
        Move towards the player
        :return: None
        """
        self.reaction_delay += 1

        # Delay exists when enemy is turning to make it easier on the player to dodge
        if player.rect.x < self.rect.x and self.reaction_delay % sets.enemy_reaction_delay == 0:
            self.dir = -1
        elif player.rect.x >= self.rect.x and self.reaction_delay % sets.enemy_reaction_delay == 0:
            self.dir = 1

        self.rect.x += self.speed * self.dir

    def draw(self):
        # animating the enemies
        self.animation_timer += 1
        if self.animation_timer % sets.enemy_animation_speed == 0:
            if self.current_image != len(self.images) - 1:
                self.current_image += 1
            else:
                self.current_image = 0

        to_blit = self.images[self.current_image]

        if self.dir == -1:
            to_blit = pygame.transform.flip(to_blit, True, False)

        temp_rect = to_blit.get_rect()
        temp_rect.center = self.rect.center
        self.screen.blit(to_blit, temp_rect)

    def check_health(self, enemys, player):
        """
        remove and delete self if health is zero, adds ammo to player if condition is valid
        :param enemys: list of enemies to remove self from
        :param player: to give ammo to
        :return: None
        """
        if self.health <= 0:
            try:
                self.dead = True
                random.choice(self.dying_sfx).play()
                enemys.remove(self)
            except ValueError:
                print("Can't remove enemy from list. Unknown effect")

            # Add ammo to player when enemy is killed
            if player.ammo <= sets.enemy_death_ammo:  # so bar doesn't overflow
                player.ammo += sets.enemy_death_ammo

            factor = 1
            if self.sub_id == "Jumper":
                factor = 2
            elif self.sub_id == "Tank":
                factor = 4

            fn.update_score(player, factor)

    def shoot(self, player):
        """
        Shoot at player
        :param player: player to shoot at
        :return: None
        """

        # shoot only when within screen bounds
        self.shooting_delay += 1
        if 0 < self.rect.x < sets.screen_width:
            if self.shooting_delay % sets.enemy_shoot_delay == 0:
                self.bullets.append(Bullet(self.screen, self,
                                           self.rect.centerx,
                                           self.rect.centery - 20))
                # play shooting sfx
                self.shooting_sfx.play()

    def normalize_health(self):
        """ Stop enemy health from going all funky """
        if self.health > 100:
            self.health = 100
        elif self.health < 0:
            self.health = 0

    def die(self, enemys):
        """
        experimental function to make enemy death a bit more aesthetic
        :param enemys: Global List of enemys
        :return: None
        """
        self.death_animation_timer += 1
        if self.death_animation_timer <= sets.enemy_death_animation:
            to_blit = pygame.transform.rotate(self.images[self.current_image], -90)
            temp_rect = to_blit.get_rect()
            temp_rect.center = self.rect.center
            temp_rect.bottom = self.y
            self.screen.blit(to_blit, temp_rect)
        else:
            enemys.remove(self)

    def sounds(self):
        """
        plays enemy sfx (theoretically) easier than other ways
        :return: None
        """

        self.walk_sfx_timer += 1

        # play walking sound effect:
        if self.walk_sfx_timer % int(sets.fps / 4) == 0:
            self.walking_sfx.play()

        # shooting is in shoot function
        # hit sfx is in bullet class

    def update(self, player, enemys):

        self.normalize_health()
        if not self.dead:
            self.check_health(enemys, player)
            self.draw()
            self.move(player)
            self.shoot(player)
            self.sounds()
            self.health_bar.update()
            # remove bullets out of bound
            for bullet in self.bullets:
                bullet.update(player=player, bullets=self.bullets)

        # if self.dead:
        #     self.die(enemys)


class Jumper(Enemy):
    def __init__(self, screen, x, y=sets.walking_plane_y):
        self.jump_counter = sets.jump_height
        self.jump_height = sets.jump_height
        self.jump_delay = 0
        self.jumping = False

        super().__init__(screen, x, y)

        self.speed = sets.enemy_speed * 1.5
        self.images = jumper_images[:]
        self.sub_id = "Jumper"
        self.health = sets.j_enemy_health

    def jump(self):
        self.jump_delay += 1

        if self.jump_delay % sets.jumper_delay == 0:
            self.jumping = True

        if self.jumping:
            if self.jump_counter >= -self.jump_height:
                neg = 1
                if self.jump_counter < 0:
                    neg = -1
                # Conversion to int removes inaccuracies
                self.rect.y -= int((self.jump_counter ** 2) * neg * 0.15)
                self.jump_counter -= 1
            else:
                self.jump_counter = self.jump_height
                self.jumping = False

    def update(self, player, enemys):
        if not self.dead:
            self.jump()

        super().update(player, enemys)
