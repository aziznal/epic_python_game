import pygame
import os
import random

from Settings import Settings
from Bar import Bar
from Bullet import Bullet
import Functions as fn

sets = Settings()

# region Player Images Loading
images = []
img_max_ = 12
for x in range(1, img_max_ + 1):
    try:
        f = pygame.image.load(os.path.join("images",
                                           "dem" + str(x) + ".png"))
    except FileNotFoundError:
        f = None
    if f is not None:
        images.append(f)
# endregion

# region Player Sound Effects Loading

shooting_sfx = []  # since shooting has multiple sfx alone
for x in range(1, 4):
    shooting_sfx.append(pygame.mixer.Sound(os.path.join("sounds", "player_shoot"
                                                        + str(x) + ".wav")))

walking_sfx = pygame.mixer.Sound(os.path.join("sounds", "player_step.wav"))
dead_sfx = pygame.mixer.Sound(os.path.join("sounds", "player_dead.wav"))
jump_sfx = pygame.mixer.Sound(os.path.join("sounds", "player_jump.wav"))
hit_sfx = pygame.mixer.Sound(os.path.join("sounds", "player_hit.wav"))
stomp_sfx = pygame.mixer.Sound(os.path.join("sounds", "player_stomp.wav"))
crash_sfx = pygame.mixer.Sound(os.path.join("sounds", "player_crash.wav"))
# endregion


class Player:
    def __init__(self, screen, x=sets.spawn_location_x,
                 y=sets.spawn_location_y):
        self.id = "Player"
        self.spawned = False
        self.x, self.y, self.screen = x, y, screen

        global sets
        sets = fn.get_settings()

        # region animation and images
        self.images = images[2:]
        # scaling images to be same size as player hitbox
        if True:
            for image in range(0, len(self.images)):
                self.images[image] = pygame.transform.scale(self.images[image],
                                                            (120, 169))

        self.animation_timer = 0
        self.current_image = 0

        # image for when player is just standing
        self.default_image = images[0]
        self.default_image = pygame.transform.scale(self.default_image,
                                                    (120, 169))
        # image for when player is crouched
        self.jumping_image = images[1]
        self.jumping_image = pygame.transform.scale(self.jumping_image,
                                                    (120, 169))

        # endregion

        # region technical init stuff
        self.width, self.height = (120, 169)
        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))
        self.rect.bottom = self.y
        self.speed = sets.player_speed
        self.dir = 1
        self.game_score = 0
        self.dead = False
        # endregion

        # region motion related stuff
        self.moving = False

        self.jumping = False
        self.jump_height = sets.jump_height
        self.jump_counter = self.jump_height
        self.stamina = sets.player_stamina
        self.jump_bar = Bar(self, self.screen, id="Jump")
        # endregion

        # region health related stuff
        self.health = sets.player_health
        self.health_bar = Bar(self, self.screen)
        self.health_regen_timer = 0
        # endregion

        # region shooting related stuff
        self.ammo = sets.player_ammo
        self.ammo_bar = Bar(self, self.screen, id="Ammo")
        self.shooting = False
        self.shoot_delay = 0
        self.bullets = []  # List to hold shot bullets
        self.reload_timer = 0
        # endregion

        # region sound effects
        self.shooting_sfx = shooting_sfx[:]
        for sound in self.shooting_sfx:
            sound.set_volume(0.2)

        self.walking_sfx = walking_sfx
        self.walk_timer = 0

        self.dead_sfx = dead_sfx

        self.jump_sfx = jump_sfx
        self.jump_sfx.set_volume(0.05)

        self.hit_sfx = hit_sfx
        self.hit_sfx.set_volume(0.3)

        self.stomp_sfx = stomp_sfx
        self.stomp_sfx.set_volume(0.2)

        self.crash_sfx = crash_sfx
        self.crash_sfx.set_volume(0.2)
        # endregion

    def spawn(self):
        """
        Make player gracefully fall out of the sky as they spawn in
        :return:
        """
        if not self.spawned:
            if self.rect.bottom <= sets.walking_plane_y:
                self.rect.y += sets.player_falling_speed
                self.jumping = False
                self.stamina = sets.player_stamina
                self.health = sets.player_health
            else:
                self.spawned = True
                self.rect.bottom = sets.walking_plane_y

    def update_score(self, factor=1):
        """
        Increment Score
        :return: None
        """
        if sets.chosen_difficulty == "EASY":
            self.game_score += sets.score_increment * factor
            print(sets.chosen_difficulty)
        elif sets.chosen_difficulty == "HARD":
            self.game_score += sets.score_increment * factor * 2
            print(sets.chosen_difficulty)

    def move(self):
        keypress = pygame.key.get_pressed()

        # LEFT
        if keypress[sets.left] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.dir = -1
            self.moving = True

        # RIGHT
        if keypress[sets.right] and self.rect.right < sets.screen_width:
            self.rect.x += self.speed
            self.dir = 1
            self.moving = True

        # JUMP
        if keypress[sets.jump]:
            if not self.jumping and self.stamina >= sets.stamina_drop:
                self.jump_sfx.play()
                self.jumping = True
                self.stamina -= sets.stamina_drop

        # SHOOT
        if keypress[sets.shoot] and self.ammo >= sets.ammo_drop:
            self.shooting = True
        else:
            self.shooting = False

    def check_shooting(self):
        """
        Shoots a bullet if condition is valid
        :return: None
        """
        if self.shooting:
            self.shoot_delay += 1
            if self.shoot_delay % sets.player_shoot_delay == 0:
                self.bullets.append(Bullet(self.screen, self, self.rect.centerx, self.rect.centery - 20))
                self.ammo -= sets.ammo_drop
        else:
            self.shooting = False
            # making shoot_delay = bla makes it so that first press fires a bullet always
            self.shoot_delay = sets.player_shoot_delay - 1

    def check_jumping(self):
        """
        makes player jump if condition is valid
        :return: None
        """
        if self.jumping:
            if self.jump_counter >= -self.jump_height:
                neg = 1
                if self.jump_counter < 0:
                    neg = -1
                # Conversion to int removes inaccuracies
                self.rect.y -= int((self.jump_counter ** 2) * neg * 0.15)
                self.jump_counter -= 1
            else:
                self.jumping = False
                self.jump_counter = self.jump_height

    def draw(self):
        # Drawing and animating the player
        if self.moving:
            if not self.jumping:
                self.animation_timer += 1
                if self.animation_timer % sets.player_animation_speed == 0:
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
            else:
                self.current_image = 0

                to_blit = self.jumping_image

                if self.dir == -1:
                    to_blit = pygame.transform.flip(self.jumping_image, True, False)

                temp_rect = to_blit.get_rect()
                temp_rect.center = self.rect.center
                self.screen.blit(to_blit, temp_rect)

        elif not self.moving:
            if not self.jumping:
                self.current_image = 0

                to_blit = self.default_image

                if self.dir == -1:
                    to_blit = pygame.transform.flip(self.default_image, True, False)

                temp_rect = to_blit.get_rect()
                temp_rect.center = self.rect.center
                self.screen.blit(to_blit, temp_rect)
            else:
                self.current_image = 0

                to_blit = self.jumping_image

                if self.dir == -1:
                    to_blit = pygame.transform.flip(self.jumping_image, True, False)

                temp_rect = to_blit.get_rect()
                temp_rect.center = self.rect.center
                self.screen.blit(to_blit, temp_rect)

    def regen(self):
        """
        regenerates player's stamina, ammo, etc..
        :return:
        """

        # HEALTH
        self.health_regen_timer += 1
        if self.health <= sets.player_health - sets.health_regen_rate:
            if self.health_regen_timer % sets.health_regen_timer == 0:
                self.health += sets.health_regen_rate

        # STAMINA
        if self.stamina <= sets.player_stamina - sets.stamina_regen_rate:
            self.stamina += sets.stamina_regen_rate

        # AMMO
        self.reload_timer += 1
        if self.ammo <= sets.player_ammo - sets.ammo_regen_rate:
            if self.reload_timer % sets.player_reload_timer == 0:
                self.ammo += sets.ammo_regen_rate

    def normalize_health(self):
        """
        Makes sure player's health is within its bounds
        :return: None
        """
        if self.health < 0:
            self.health = 0
        elif self.health > sets.player_health:
            self.health = sets.player_health

    def normalize_ammo(self):
        """
        to stop ammo bar from going out of bounds
        :return: None
        """
        if self.ammo > sets.player_ammo:
            self.ammo = sets.player_ammo
        elif self.ammo < 0:
            self.ammo = 0

    def normalize_stamina(self):
        """
        to stop stamina bar from going out of bounds
        :return: None
        """
        if self.stamina > sets.player_stamina:
            self.stamina = sets.player_stamina
        elif self.stamina < 0:
            self.stamina = 0

    def collide(self, enemys):
        """
        Controls what happens in player-enemy collisions
        :param enemys: List of enemies to check
        :return: None
        """
        for enemy in enemys:
            # player is either dealing with a normal
            if enemy.sub_id == "Normal":
                # player might have ran into normal
                if self.rect.colliderect(enemy.rect) and not self.jumping:
                    enemys.remove(enemy)
                    self.health -= enemy.health
                    # play getting hit sfx
                    self.crash_sfx.play()
                # or player is stomping on a normal
                if self.rect.colliderect(enemy.rect) and self.jumping:
                    enemys.remove(enemy)
                    self.ammo += sets.enemy_death_ammo
                    self.health += enemy.health / 2
                    self.stamina += sets.stamina_regen_rate * 20
                    self.update_score()
                    # play stomp sfx
                    self.stomp_sfx.play()

            # or player is dealing with a jumper
            elif enemy.sub_id == "Jumper":
                # player may have crashed into normal in mid-air
                if self.rect.colliderect(enemy.rect) and self.jumping and enemy.jumping:
                    enemys.remove(enemy)
                    self.health -= enemy.health
                    self.crash_sfx.play()

                # or jumper stomped on player or crashed into them walking
                if self.rect.colliderect(enemy.rect) and not self.jumping:
                    enemys.remove(enemy)
                    self.health -= enemy.health
                    self.crash_sfx.play()

                # or player may have stomped on jumper which is on floor
                elif self.rect.colliderect(enemy.rect) and self.jumping and not enemy.jumping:
                    enemys.remove(enemy)
                    self.ammo += sets.enemy_death_ammo
                    self.health += enemy.health / 2
                    # Fully Restore player's stamina when they stomp a jumper
                    self.stamina = sets.player_stamina
                    self.update_score()
                    # play stomp sfx
                    self.stomp_sfx.play()

    def check_health(self):
        """
        Goes gameover when player's health is zero
        :return:
        """
        if self.health <= 0:
            self.health = 0
            self.dead = True
            self.dead_sfx.play()

    def sounds(self):
        """
        makes it easier (theoretically) to manage sound fx being played
        :return: None
        """
        # playing walking sounds
        self.walk_timer += 1
        if self.moving and not self.jumping and self.walk_timer % sets.walk_sfx_timer == 0:
            self.walking_sfx.play()
        # Jumping sfx is placed in move function for convenience
        # player hit_sfx is in bullet class
        # Shooting Sounds (randomly plays one of three available sounds)
        if self.shooting and self.shoot_delay % sets.player_shoot_delay == 0:
            random.choice(self.shooting_sfx).play()

    def update(self, enemys):
        self.moving = False  # Cuz I'm a fucking genius or maybe extremely retarded possibly
        self.spawn()
        self.check_jumping()
        self.move()
        self.sounds()
        self.draw()
        self.regen()
        self.collide(enemys)
        self.check_shooting()
        self.check_health()

        self.normalize_health()
        self.normalize_ammo()
        self.normalize_stamina()

        self.health_bar.update()
        self.jump_bar.update()
        self.ammo_bar.update()

        # Update bullets fired by the player
        for bullet in self.bullets:
            bullet.update(objects=enemys, bullets=self.bullets)
