import sys
import pygame
import os

import Functions as fn

from Settings import Settings
from Player import Player
from TextObject import TextObject

# todo: add a hierarchical powerup class system. (health, ammo, shield, nuke, ?...)
# todo: implement a shield powerup
# todo: add more enemy classes (derived from the main one) like 'Tank' and\or 'Special'
# todo: make background of start -> gameover screens a video of a burning fire? (use pygame.movie)
# todo: add a rickroll link in the about section
# todo: hardmode needs full planning:
# scores are doubled. enemies' health is doubled. enemy spawn speed is doubled. more higher class enemies spawn.
# difficulty is printed next to player's name in the score menu.

# region setup

# region game music
game_theme = pygame.mixer.Sound(os.path.join("sounds", "game_song.wav"))
game_theme.set_volume(0.75)
#game_theme.play()
# https://youtu.be/Dboi1bja6M8?list=RDXmkFqSQ7n1I
# endregion

sets = Settings()
screen = pygame.display.set_mode((sets.screen_width, sets.screen_height))
# screen = pygame.display.set_mode((sets.screen_width, sets.screen_height), flags=pygame.FULLSCREEN)
screen_rect = screen.get_rect()
pygame.display.set_caption("Epic_Game")
clock = pygame.time.Clock()

title = TextObject(screen, text="Epic_Game Beta Phase", color=sets.white)

# region loading game background
game_background = pygame.image.load(os.path.join("images", "game_background.png")).convert()
game_background = pygame.transform.scale(game_background, (sets.screen_width, sets.screen_height))
# endregion


# region temp_function_for_text
# todo: move this function to TextObject class
temp_timer = 0
temp_timer_delay = 2
temp_increment = 1


def temp_text_move(text_object):
    global temp_timer, temp_timer_delay, temp_increment
    temp_timer += 1
    if temp_timer % temp_timer_delay == 0:
        text_object.rect.x += temp_increment

    if temp_timer % 100 * temp_timer_delay == 0:
        temp_increment *= -1
# endregion

# endregion


pygame.init()

replay = True


def main_game():

    # region Setup
    player = Player(screen)

    # region some score settings
    score = TextObject(screen, text="Score: ", size=40)
    score.rect.midtop = screen_rect.midtop
    score.rect.x -= 15
    score_num = TextObject(screen, text=str(player.game_score), changing=True, size=40)
    score_num.rect.midleft = score.rect.midright
    # endregion

    enemy_spawn_delay = 0
    # endregion

    while True:
        screen.blit(game_background, screen.get_rect())

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_p:
                    fn.pause(screen)

        player.update(enemys)

        for enemy in enemys:
            enemy.update(player, enemys)

        # after the player has spawned
        if player.spawned:
            # spawn normal enemies
            if enemy_spawn_delay % sets.enemy_spawn_delay == 0:
                fn.spawn(screen, enemys, enemy_type="Normal")

            # spawn jumper enemies
            if enemy_spawn_delay % sets.j_enemy_spawn_delay == 0:
                fn.spawn(screen, enemys, enemy_type="Jumper")

        enemy_spawn_delay += 1

        # text objects
        title.update()
        score.update()
        score_num.update(str(player.game_score))

        # spawn and update powerups
        # fn.manage_powerups(powerUps, screen)

        if player.dead:
            game_theme.stop()
            fn.save_score(player, "player_name")
            global replay
            replay = fn.gameover(screen, player)
            return

        clock.tick(sets.fps)
        pygame.display.update()


while replay:
    enemys = []     # resets all enemys on screen for when the game is reset
    powerUps = []
    # player_name = InputText().return_name()
    sets.chosen_difficulty = fn.start_screen(screen, game_theme)
    print(sets.chosen_difficulty)
    sets = fn.get_settings()
    main_game()

pygame.quit()
sys.exit()
