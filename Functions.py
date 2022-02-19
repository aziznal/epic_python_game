import pygame
import random
import sys
import os

from Enemy import Enemy, Jumper
from Settings import Settings
from TextObject import TextObject
from Button import Button
from toggle_switch import ToggleSwitch
from PowerUp import PowerUp

sets = Settings()
pygame.font.init()

button_click_sfx = pygame.mixer.Sound(os.path.join("sounds", "button_click.wav"))
button_click_sfx.set_volume(0.2)


def get_settings():
    """
    Helper function to give updated settings to different parts of program
    :return: updated Settings
    """
    return sets


def file_editor(filename, data=None, read=False, write=False):
    """
    Makes it easier to read/write/append data from/to a file
    :param data: Data to be added to file (in this case it's text)
    :param filename: path to file
    :param read: Bool
    :param write: Bool (if selected then overwrites, otherwise appends)
    :return: if read is selected then it returns a list of the string data
    """
    if read:
        opened_file = open(filename, "r")
        temp_data = opened_file.readlines()
        opened_file.close()
        return temp_data

    elif data is not None:
        if not write:
            opened_file = open(filename, "a+")
            opened_file.write(data)
            opened_file.close()

        elif write:
            opened_file = open(filename, "w+")
            opened_file.write(data)
            opened_file.close()
    else:
        return


def spawn(screen, enemys, max_=sets.max_enemy, enemy_type="Normal"):
    """
    Continuously spawns enemies from out of screen bounds (left and right)
    :param enemy_type: Normal, Jumper, etc..
    :param screen: current display
    :param enemys: list of enemies to be appended
    :param max_: max amount of enemies to be onscreen at the same time
    :return: None
    """
    if enemy_type == "Normal":
        if len(enemys) <= max_:

            # enemy is either spawned to the left between (-300, -50) OR
            # enemy is spawned from the right between (res + 50, res + 250)

            temp_enemy = Enemy(screen,
                               x=random.choice((random.randint(-300, -50),
                                               random.randint(sets.screen_width + 50,
                                                              sets.screen_width + 250))))
            enemys.append(temp_enemy)
            del temp_enemy

    elif enemy_type == "Jumper":
        if len(enemys) <= max_:
            temp_enemy = Jumper(screen,
                               x=random.choice((random.randint(-300, -50),
                                                random.randint(sets.screen_width + 50,
                                                               sets.screen_width + 250))))
            enemys.append(temp_enemy)
            del temp_enemy


def swap_list_elements(list_, elm1, elm2):
    temp = list_[elm1]
    list_[elm1] = list_[elm2]
    list_[elm2] = temp


def sort_me_scores(score_names, score_nums):
    """
    Sorts scores numbers and their respective names using bubble sort
    :param score_names: names list
    :param score_nums: numbers list
    :return: None
    """
    laps = len(score_names)
    for lap in range(laps):
        for item in range(0, laps - lap - 1):
            if int(score_nums[item]) > int(score_nums[item + 1]):
                swap_list_elements(score_nums, item, item + 1)
                swap_list_elements(score_names, item, item + 1)

    score_nums.reverse()
    score_names.reverse()


def score_screen(screen):
    """Shows the highscore list"""
    # region Setup
    back_button = Button(500, 500, 1, 1, screen, "Back", text_size=25, imaged=True, textcolor=sets.white)
    back_button.rect.center = screen.get_rect().center
    back_button.rect.y += 300

    title = TextObject(screen, bold=True, text="Top Scores")
    title.rect.center = screen.get_rect().center
    title.rect.y = screen.get_rect().centery - 150

    reset_button = Button(1, 1, 1, 1, screen, "CLEAR", imaged=True, textcolor=sets.red)
    reset_button.rect.midbottom = title.rect.midtop
    reset_button.rect.y -= 10

    # region Data Processing
    # get the data from the text file
    score = file_editor("scores.txt", read=True)

    empty_string = "Empty"
    is_empty = False

    if len(score) == 0:
        is_empty = True

    # each individual score is separated by a dash
    if not is_empty:
        score_list_pre = str(score[0]).split("-")
    else:
        score_list_pre = None

    # then, each line has a name and a number separated by a dot
    if not is_empty:
        score_list_pre_name = []    # list to save names
        score_list_pre_num = []     # list to save numerical values
        for line in range(0, len(score_list_pre) - 1):
            to_append_ = score_list_pre[line].split(".")
            score_list_pre_name.append(to_append_[0])
            score_list_pre_num.append(to_append_[1])

        print(score_list_pre_num)

        sort_me_scores(score_list_pre_name, score_list_pre_num)

    # Text Objects go to these lists
    score_list_name = []
    score_list_num = []

    # make list of text objects
    if not is_empty:
        if len(score_list_pre_name) > sets.score_show_limit:
            for x in range(sets.score_show_limit):
                score_list_name.append(TextObject(screen, text=score_list_pre_name[x]))
                score_list_num.append(TextObject(screen, text=score_list_pre_num[x]))
        else:
            for x in range(len(score_list_pre_name)):
                score_list_name.append(TextObject(screen, text=score_list_pre_name[x]))
                score_list_num.append(TextObject(screen, text=score_list_pre_num[x]))

        # place them properly
        score_list_name[0].rect.left = sets.score_menu_left_margins
        score_list_name[0].rect.y = title.rect.bottom + 20

        score_list_num[0].rect.right = sets.score_menu_right_margins
        score_list_num[0].rect.y = title.rect.bottom + 20

        for x in range(1, len(score_list_name)):
            score_list_name[x].rect.left = sets.score_menu_left_margins
            score_list_name[x].rect.y = score_list_name[x - 1].rect.bottom

            score_list_num[x].rect.right = sets.score_menu_right_margins
            score_list_num[x].rect.y = score_list_num[x - 1].rect.bottom
    else:
        score_list_name.append(TextObject(screen, text=empty_string))
        score_list_name[0].rect.center = screen.get_rect().center
        score_list_name[0].rect.y -= 100
    # endregion Data Processing

    # endregion Setup

    loop = True
    while loop:
        screen.fill(sets.white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        back_button.update()
        reset_button.update()
        title.update()

        if back_button.clicked:
            loop = False
            button_click_sfx.play()

        if reset_button.clicked:
            file_editor("scores.txt", data="", write=True)
            loop = False
            button_click_sfx.play()

        for score in score_list_name:
            score.update()

        for score in score_list_num:
            score.update()

        pygame.display.update()


def save_score(player, player_name):
    current_scores = file_editor("scores.txt", read=True)

    # Format is: Score 'index num'(8 spaces).'Score' (for now)
    if len(current_scores) != 0:
        index_num = len(current_scores[0].split("-"))
    else:
        index_num = 1

    # no more than 15 scores
    if index_num >= sets.score_show_limit:
        print("Score Limit Reached")
        return

    score = player_name + "." + str(player.game_score) + "-"

    # Clear the current file of everything ...
    file_editor("scores.txt", write=True, data="")

    current_scores.append(score)

    # ... then re-write everything with the new score appended to it
    for bit in current_scores:
        file_editor("scores.txt", data=bit)


def settings_screen(screen):
    """
    screen displayed when player clicks settings button
    :param screen: Game Display
    :return: None
    """

    # region Setup
    clock = pygame.time.Clock()

    screen_title = TextObject(screen, x=400, y=50,
                              size=60, text="Game Settings")

    screen_title.rect.center = screen.get_rect().center
    screen_title.rect.y = 50

    back_button = Button(500, 500, 1, 1, screen, "Back", text_size=25, imaged=True, textcolor=sets.white)
    back_button.rect.center = screen.get_rect().center
    back_button.rect.y += 300

    # region Switches
    # region difficulty settings
    switch_difficulty_easy = ToggleSwitch(screen, 600, 200, toggled=True)

    switch_difficulty_easy_text = TextObject(screen, text="Easy", size=30)
    switch_difficulty_easy_text.rect.midleft = switch_difficulty_easy.rect.midright
    switch_difficulty_easy_text.rect.x += 15

    difficulty_text = TextObject(screen, text="Choose a difficulty", size=35)
    difficulty_text.rect.bottom = switch_difficulty_easy.rect.top
    difficulty_text.rect.left = switch_difficulty_easy.rect.left

    switch_difficulty_hard = ToggleSwitch(screen)
    switch_difficulty_hard.rect.midtop = switch_difficulty_easy.rect.midbottom

    switch_difficulty_hard_text = TextObject(screen, text="Hard", size=30)
    switch_difficulty_hard_text.rect.midleft = switch_difficulty_hard.rect.midright
    switch_difficulty_hard_text.rect.x += 15
    # endregion
    # endregion

    loop = True
    # endregion Setup

    while loop:
        screen.fill(sets.white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        screen_title.update()

        back_button.update()

        # region Difficulty Runtime Settings
        switch_difficulty_easy.update()
        switch_difficulty_easy_text.update()

        if switch_difficulty_easy.toggled:
            switch_difficulty_hard.toggled = False
            sets.chosen_difficulty = "EASY"

        difficulty_text.update()

        switch_difficulty_hard.update()
        switch_difficulty_hard_text.update()

        if switch_difficulty_hard.toggled:
            switch_difficulty_easy.toggled = False
            sets.chosen_difficulty = "HARD"

        if not switch_difficulty_hard.toggled and not switch_difficulty_easy.toggled:
            switch_difficulty_easy.toggled = True
        # endregion

        if back_button.clicked:
            loop = False
            button_click_sfx.play()

        pygame.display.update()
        clock.tick(sets.fps)


def about_screen(screen):
    """
    screen displayed when player clicks the about button
    :param screen: Game Display
    :return: None
    """

    # region Setup
    clock = pygame.time.Clock()

    screen_title = TextObject(screen, x=550, y=50,
                              size=60, text="About")

    screen_title.rect.center = screen.get_rect().center
    screen_title.rect.y = 50

    text1 = TextObject(screen, x=550, y=250, text="I maked this", size=25, bold=True)

    text1.rect.center = screen.get_rect().center

    back_button = Button(500, 500, 1, 1, screen, "Back", text_size=25, imaged=True, textcolor=sets.white)
    back_button.rect.center = screen.get_rect().center
    back_button.rect.y += 300

    loop = True
    # endregion Setup

    while loop:
        screen.fill(sets.white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        screen_title.update()
        text1.update()

        back_button.update()

        if back_button.clicked:
            loop = False
            button_click_sfx.play()

        pygame.display.update()
        clock.tick(sets.fps)


def start_screen(screen, game_music):
    """
    Screen displayed when game is launched
    :param game_music:
    :param screen: game screen
    :return: None
    """
    # region Setup
    clock = pygame.time.Clock()

    # region Text Objects
    game_title = TextObject(screen=screen,
                            text="Epic_game Beta phase",
                            size=80,
                            bold=True)

    rule1 = TextObject(screen,
                       text="Move around with left and right arrows",
                       size=15)
    rule2 = TextObject(screen,
                       text="Press up arrow to jump",
                       size=15)
    rule3 = TextObject(screen,
                       text="Press X to shoot",
                       size=15)
    rule4 = TextObject(screen,
                       text="Don't let enemies shoot or run into you",
                       size=15)

    rule5 = TextObject(screen,
                       text="When you destroy an enemy, their shots disappear. It's a feature, not a bug!",
                       size=15)
    # endregion

    # region Buttons
    start_button = Button(screen.get_rect().centerx,
                          screen.get_rect().centery,
                          120, 50, screen,
                          "Start",
                          imaged=True,
                          textcolor=sets.white)

    settings_button = Button(1, 1, 1, 1,
                             screen,
                             "Settings",
                             imaged=True,
                             textcolor=sets.white)

    about_button = Button(1, 1, 1, 1,
                          screen,
                          "About",
                          imaged=True,
                          textcolor=sets.white)

    score_button = Button(1, 1, 1, 1,
                          screen,
                          "Highscores",
                          textcolor=sets.red,
                          imaged=True)

    exit_button = Button(1, 1, 1, 1,
                         screen,
                         "Exit",
                         imaged=True,
                         textcolor=sets.white)

    temp_button = Button(1, 1, 1, 1,
                         screen,
                         "temp_button",
                         imaged=True,
                         textcolor=sets.white)

    already_clicked = False
    music_button = Button(1, 1, 1, 1,
                          screen,
                          "mute",
                          imaged=True,
                          textcolor=sets.white)

    # endregion

    # region Positions
    settings_button.rect.topright = start_button.rect.bottomright
    settings_button.rect.y += 20

    about_button.rect.topright = settings_button.rect.bottomright
    about_button.rect.y += 20

    exit_button.rect.topright = about_button.rect.bottomright
    exit_button.rect.y += 20

    game_title.rect.center = screen.get_rect().center
    game_title.rect.y -= 100

    rule1.rect.center = screen.get_rect().center
    rule1.rect.y -= 300
    rule2.rect.midtop = rule1.rect.midbottom
    rule3.rect.midtop = rule2.rect.midbottom
    rule4.rect.midtop = rule3.rect.midbottom
    rule5.rect.midtop = rule4.rect.midbottom

    score_button.rect.midbottom = rule1.rect.midtop
    score_button.rect.y -= 150

    music_button.rect.topright = screen.get_rect().topright
    music_button.rect.x -= 30
    music_button.rect.y = score_button.rect.y

    temp_button.rect.midleft = screen.get_rect().midleft
    temp_button_num = 0
    # endregion

    loop = True
    # endregion
    while loop:
        screen.fill(sets.white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        # region Updates
        game_title.update()
        rule1.update()
        rule2.update()
        rule3.update()
        rule4.update()
        rule5.update()

        start_button.update()
        settings_button.update()
        about_button.update()
        score_button.update()
        exit_button.update()
        music_button.update()
        temp_button.update()
        # endregion

        # region button clicks
        if start_button.clicked:
            loop = False
            button_click_sfx.play()

        if settings_button.clicked:
            button_click_sfx.play()
            settings_screen(screen)

        if about_button.clicked:
            button_click_sfx.play()
            about_screen(screen)

        if score_button.clicked:
            button_click_sfx.play()
            score_screen(screen)

        if exit_button.clicked:
            button_click_sfx.play()
            pygame.quit()
            sys.exit()

        # allow a click only after at least a second has passed from the former click
        if music_button.clicked:
            if not already_clicked:
                already_clicked = True
                button_click_sfx.play()
                game_music.stop()
                print("Music Button Play")
            else:
                already_clicked = False
                game_music.play()
                print("Music Button Stop")

        if temp_button.clicked:
            temp_button_num += 1
            print("clicked" + str(temp_button_num))
        # endregion

        pygame.display.update()
        clock.tick(sets.fps)

    print("Returning correct value as " + sets.chosen_difficulty)
    return sets.chosen_difficulty


def gameover(screen, player):
    """
    Shown when player is dead; gives access to score screen and replay/exit buttons
    :return: None
    """
    # region setup

    # region gameover text
    gameover_text = TextObject(screen=screen, text="Game Over!", size=180,
                               color=sets.white, font="microsoftyibaiti")

    gameover_text.rect.center = screen.get_rect().center
    gameover_text.rect.y -= 75
    # endregion

    # region Buttons
    replay_button = Button(1, 1, 1, 1,
                           screen,
                           "Main Menu",
                           textcolor=sets.white,
                           imaged=True)

    score_button = Button(1, 1, 1, 1,
                          screen,
                          "Highscores",
                          textcolor=sets.red,
                          imaged=True)

    exit_button = Button(1, 1, 1, 1,
                         screen,
                         "Exit",
                         imaged=True,
                         textcolor=sets.white)

    score_button.rect.center = screen.get_rect().center
    score_button.rect.y -= 250

    replay_button.rect.center = score_button.rect.center
    replay_button.rect.y -= score_button.rect.height + 50

    exit_button.rect.center = screen.get_rect().center
    exit_button.rect.y += 380
    # endregion

    # region score text
    score_text = TextObject(screen=screen, text="Your Final Score: ",
                            size=70, color=sets.white, font="microsoftyibaiti")

    score_text_num = TextObject(screen=screen, text=str(player.game_score),
                                size=70, color=sets.white, font="microsoftyibaiti")

    score_text.rect.midtop = gameover_text.rect.midbottom
    score_text.rect.x -= 20

    score_text_num.rect.midleft = score_text.rect.midright

    # endregion

    # region low score texts

    # region text1
    text1 = TextObject(screen=screen, text="you are a failure", size=45,
                       color=sets.white, font="microsoftyibaiti")

    text1.rect.midtop = score_text.rect.midbottom
    text1.rect.y += 10
    text1.rect.x += 30
    # endregion

    # region text2
    text2 = TextObject(screen=screen, text="don't come back", size=30,
                       color=sets.white, font="microsoftyibaiti")

    text2.rect.midtop = text1.rect.midbottom
    text2.rect.y += 10
    # endregion

    # endregion

    # region average score texts

    # region text3
    text3 = TextObject(screen=screen, text="You have performed as expected", size=45,
                       color=sets.white, font="microsoftyibaiti")

    text3.rect.midtop = score_text.rect.midbottom
    text3.rect.y += 10
    text3.rect.x += 30
    # endregion

    # region text4
    text4 = TextObject(screen=screen, text="you're not special", size=30,
                       color=sets.white, font="microsoftyibaiti")

    text4.rect.midtop = text3.rect.midbottom
    text4.rect.y += 10
    # endregion

    # endregion

    # region high score texts

    # region text5
    text5 = TextObject(screen=screen, text="you're just a showoff", size=45,
                       color=sets.white, font="microsoftyibaiti")

    text5.rect.midtop = score_text.rect.midbottom
    text5.rect.y += 10
    text5.rect.x += 30

    # endregion

    # region text6
    text6 = TextObject(screen=screen, text="get a life, loser", size=30,
                       color=sets.white, font="microsoftyibaiti")

    text6.rect.midtop = text5.rect.midbottom
    text6.rect.y += 10
    # endregion

    # endregion

    # endregion setup

    loop = True
    while loop:
        screen.fill(sets.black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        gameover_text.update()
        score_text.update()
        score_text_num.update()

        score_button.update()
        replay_button.update()
        exit_button.update()

        if player.game_score < sets.min_player_score:
            text1.update()
            text2.update()
        elif sets.min_player_score <= player.game_score < sets.high_player_score:
            text3.update()
            text4.update()
        elif player.game_score >= sets.high_player_score:
            text5.update()
            text6.update()

        if score_button.clicked:
            button_click_sfx.play()
            score_screen(screen)

        if replay_button.clicked:
            button_click_sfx.play()
            return True

        if exit_button.clicked:
            button_click_sfx.play()
            pygame.quit()
            sys.exit()

        # screen.fill(sets.white)
        # screen.blit(g_over_low, screen.get_rect())

        pygame.display.update()


def pause(screen):
    """
    Self Explanatory
    :param screen: game display
    :return: None
    """
    pause_text = TextObject(screen=screen, text="Game Paused", size=80, font="Calibri")

    pause_text.rect.center = screen.get_rect().center
    loop = True
    while loop:
        screen.fill(sets.white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_p:
                    loop = False

        pause_text.update()

        pygame.display.update()


def update_score(player, factor_=1):
    """ makes it easier to use around program """
    player.update_score(factor=factor_)


def manage_powerups(powerups, screen):
    if len(powerups) < sets.powerup_limit:
        pup = PowerUp(1, 1, screen)
        powerups.append(pup)

    for pup in powerups:
        pup.update()

        if pup.kill_me:
            powerups.remove(pup)
