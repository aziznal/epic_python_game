import pygame

# stops latency in sound fx
pygame.mixer.pre_init(44100, -16, 2, 2048)  # specifically fixes latency
pygame.mixer.init()


class Settings:
    def __init__(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self.screen_rect = pygame.Rect((0, 0),
                                       (self.screen_width, self.screen_height))
        self.fps = 60

        self.score_increment = 1

        self.score_show_limit = 15

        self.spawn_location_x = self.screen_width / 2
        self.spawn_location_y = self.screen_height / 2 - 300

        self.walking_plane_y = int(930 * (self.screen_height / 1080))  # auto adjusts to screen res

        self.chosen_difficulty = "EASY"

        # region Defining some Colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.yellow = (235, 235, 0)
        self.dark_green = (0, 175, 0)
        self.grey = (100, 100, 100)
        self.health_color = self.dark_green
        self.stamina_color = self.yellow
        self.ammo_color = self.red
        self.enemy_health_color = self.red
        # endregion

        # Font Settings
        self.font = 'Consolas'
        self.font_size = 18
        self.font_color = self.black

        # Button Settings
        self.infl_factor = 10
        self.mouse1 = (True, False, False)

        # region Player related settings

        # Animation Settings
        self.player_animation_speed = 3    # less is more here
        self.enemy_animation_speed = 3     # less is more here
        self.player_falling_speed = 15

        # Sound Settings
        self.walk_sfx_timer = self.fps / 4

        # Controls
        self.up = pygame.K_UP
        self.down = pygame.K_DOWN
        self.left = pygame.K_LEFT
        self.right = pygame.K_RIGHT
        self.jump = pygame.K_UP
        self.shoot = pygame.K_x

        self.player_speed = 13

        # Player Health Settings
        self.player_health = 100
        self.health_regen_rate = 1
        self.health_regen_timer = self.fps

        # Player Stamina Settings
        self.player_stamina = 120
        self.stamina_drop = self.player_stamina / 6
        self.stamina_regen_rate = 0.15

        # Player Ammo Settings
        self.player_ammo = 100
        self.ammo_drop = self.player_ammo / 30
        self.ammo_regen_rate = self.ammo_drop
        self.player_reload_timer = self.fps
        self.player_shoot_delay = 10

        # Player Health Bar Settings:
        self.pbar1_x = self.screen_rect.right - 260
        self.pbar1_y = 20
        self.pbar1_w = 250
        self.pbar1_h = 30

        # Player Jump Bar Settings:
        self.pbar2_x = self.screen_rect.right - 260
        self.pbar2_y = 50
        self.pbar2_w = 250
        self.pbar2_h = 20

        # Player Ammo Bar Settings:
        self.pbar3_x = self.screen_rect.right - 260
        self.pbar3_y = 70
        self.pbar3_w = 250
        self.pbar3_h = 20

        # Jump Settings
        self.jump_height = 16

        # Misc Settings
        self.min_player_score = 8
        self.high_player_score = 30
        self.score_menu_left_margins = int(self.screen_width * 2 / 5)
        self.score_menu_right_margins = self.score_menu_left_margins + 400
        self.score_menu_height_start = 300
        # endregion

        # region Enemy related settings
        self.enemy_speed = 8
        self.enemy_reaction_delay = 50
        self.enemy_health = 50

        self.max_enemy = 15

        self.enemy_spawn_delay = int(self.fps * 1.2)
        self.enemy_death_ammo = self.ammo_drop * 3
        self.enemy_shoot_delay = self.fps * 90/100
        self.enemy_death_animation = self.fps * 2

        # Enemy Health Bar Settings
        self.ebar1_x = 1000
        self.ebar1_y = 50
        self.ebar1_w = 75
        self.ebar1_h = 15

        # Jumper Enemy Settings
        self.jumper_delay = int(self.fps)
        self.j_enemy_health = int(self.enemy_health / 2)
        self.j_enemy_spawn_delay = self.fps * 5  # enemy spawns once every 7 seconds
        self.j_enemy_score = 2

        # endregion

        # Bullet Settings
        self.bullet_width, self.bullet_height = 15 * 5, 9 * 5
        self.bullet_speed = 25
        self.bullet_damage = 15

        # region toggle switch settings
        self.t_switch_def_size = 90
        self.t_switch_w = 10
        self.t_switch_h = 10
        # endregion

        # region PowerUp Settings
        self.powerup_w, self.powerup_h = 50, 50
        self.powerup_types = ["HEALTH", "AMMO", "SHIELD", "NUKE"]
        self.powerup_fall_speed = 1
        self.powerup_limit = 3
        # endregion
