import pygame
from json import load, dump
from random import randint, choice
from math import sqrt, sin, cos, radians, floor, pi
from objects import *

pygame.mixer.pre_init(44100,-16,2,512)
pygame.mixer.init()
pygame.init()

FPS = 60
resolution = (750, 800)
Screen = pygame.display.set_mode(resolution)
text_font_s = pygame.font.SysFont('Consolas', 30)
text_font = pygame.font.SysFont('Consolas', 50)
text_font_l = pygame.font.SysFont('Consolas', 70)
text_font_xl = pygame.font.SysFont('Consolas', 140)
pygame.display.set_caption('Speis\' Ship')

Switch = 0
''' Switch cases:
0 = set up all of the variables
1 = main menu
2 = gameplay
3 = game over
4 = level summary
5 = settings
6 = credits
7 = pause menu
8 = shop level
9 = shop GUI
'''

switch_settings = 0
''' switch_settings cases:
0 = settings main menu
1 = audio settings
2 = key bind settings
'''

# Loading & Setting up some things ---------------------------------------------------------------------------------------- #
# settings
with open("data/settings.json") as f:
    settings = load(f)
with open("data/keybinds.json") as f:
    keybinds = load(f)
with open("data/enemies.json") as f:
    enemies_data = load(f)
with open("data/levels.json") as f:
    levels = load(f)

sfx_volume = settings['sfx_volume']
music_volume = settings['music_volume']

key_binds = {
    "up": eval(settings["key_binds"]["up"]),
    "left": eval(settings["key_binds"]["left"]),
    "down": eval(settings["key_binds"]["down"]),
    "right": eval(settings["key_binds"]["right"]),
    "shoot": eval(settings["key_binds"]["shoot"]),
    "pause": eval(settings["key_binds"]["pause"])
}

# sprites
player_s = pygame.image.load("sprites/player.png").convert_alpha()

enemy_s1_s = pygame.image.load("sprites/enemies/enemy_s1.png").convert_alpha()
enemy_s2_s = pygame.image.load("sprites/enemies/enemy_s2.png").convert_alpha()
enemy_s3_s = pygame.image.load("sprites/enemies/enemy_s3.png").convert_alpha()
enemy_s4_s = pygame.image.load("sprites/enemies/enemy_s4.png").convert_alpha()
enemy_s5_s = pygame.image.load("sprites/enemies/enemy_s5.png").convert_alpha()
enemy_b1_s = pygame.image.load("sprites/enemies/enemy_b1.png").convert_alpha()
enemy_b2_s = pygame.image.load("sprites/enemies/enemy_b2.png").convert_alpha()

martin_s = pygame.image.load("sprites/characters/Martin.png").convert_alpha()

bullet_s = pygame.image.load("sprites/bullets/bullet_1.png").convert_alpha()
enemy_bullet_1_s = pygame.image.load("sprites/bullets/enemy_bullet_1.png").convert_alpha()
enemy_bullet_2_s = pygame.image.load("sprites/bullets/enemy_bullet_2.png").convert_alpha()

friendly_station_s = [pygame.image.load("sprites/friendly_station/friendly_station_1.png").convert_alpha(), pygame.image.load("sprites/friendly_station/friendly_station_2.png").convert_alpha(), pygame.image.load("sprites/friendly_station/friendly_station_3.png").convert_alpha(), pygame.image.load("sprites/friendly_station/friendly_station_4.png").convert_alpha()]

# sfx
shoot_sfx = [pygame.mixer.Sound("sfx/shoot/shoot_1.wav"), pygame.mixer.Sound("sfx/shoot/shoot_2.wav"), pygame.mixer.Sound("sfx/shoot/shoot_3.wav")]
buy_sfx = [pygame.mixer.Sound("sfx/shop sfx/buy_1.wav"), pygame.mixer.Sound("sfx/shop sfx/buy_2.wav"), pygame.mixer.Sound("sfx/shop sfx/buy_3.wav")]
menu_nav_false = pygame.mixer.Sound("sfx/menu_nav_false.wav")
enemy_shoot = pygame.mixer.Sound("sfx/enemy_shoot.wav")
enemy_die_l = pygame.mixer.Sound("sfx/enemy_die_l.wav")
player_die = pygame.mixer.Sound("sfx/player_die.wav")
enemy_die = pygame.mixer.Sound("sfx/enemy_die.wav")
fleet_hit = pygame.mixer.Sound("sfx/fleet_hit.wav")
menu_nav = pygame.mixer.Sound("sfx/menu_nav.wav")
money = pygame.mixer.Sound("sfx/credit.wav")
shoot = pygame.mixer.Sound("sfx/shoot.wav")
hit = pygame.mixer.Sound("sfx/hit.wav")

# setting up sfx volume
for sfx in buy_sfx:
    sfx.set_volume(sfx_volume)
for sfx in shoot_sfx:
    sfx.set_volume(sfx_volume)
menu_nav_false.set_volume(sfx_volume)
enemy_shoot.set_volume(sfx_volume)
enemy_die_l.set_volume(sfx_volume)
player_die.set_volume(sfx_volume)
enemy_die.set_volume(sfx_volume)
fleet_hit.set_volume(sfx_volume)
menu_nav.set_volume(sfx_volume)
money.set_volume(sfx_volume)
shoot.set_volume(sfx_volume)
hit.set_volume(sfx_volume)

# Functions --------------------------------------------------------------------------------------------------------------- #

def spawnStar(velocity):
    global star_cooldown
    if star_cooldown <= 0:
        stars.append(star(velocity))
        star_cooldown = star_cooldown_default
    else:
        star_cooldown -= 1

def redrawGameWindow():
    Screen.fill((0,0,0))
    for s in stars:
            s.draw(Screen)

    if Switch == 1:
        Screen.blit(game_title, game_title_rect)
        new_game_button.draw(Screen)
        settings_button.draw(Screen)
        credits_button.draw(Screen)

    elif Switch == 2:
        if boss_fight:
            Screen.blit(boss_health, boss_health_rect)
        for b in bullets:
            b.draw(Screen)
        for b in enemy_bullets:
            b.draw(Screen)
        for e in enemies:
            e.draw(Screen)
        player.draw(Screen)
        Screen.blit(health, (15, int(health_text_y)))
        Screen.blit(health_fleet, (15, int(health_fleet_text_y)))

    elif Switch == 3:
        Screen.blit(game_over_text, game_over_text_rect)
        restart_button.draw(Screen)

    elif Switch == 4:
        player.draw(Screen)
        Screen.blit(health, (15, int(health_text_y)))
        Screen.blit(health_fleet, (15, int(health_fleet_text_y)))
        Screen.blit(summary_text_money, summary_text_money_rect)

    elif Switch == 5:

        if switch_settings == 0:
            Screen.blit(settings_text, settings_text_rect)
            audio_settings_button.draw(Screen)
            keybind_settings_button.draw(Screen)
            back_settings_button.draw(Screen)

        elif switch_settings == 1:
            Screen.blit(audio_settings_text, audio_settings_text_rect)
            Screen.blit(music_volume_text_1, music_volume_text_1_rect)
            Screen.blit(music_volume_text_2, music_volume_text_2_rect)
            Screen.blit(sfx_volume_text_1, sfx_volume_text_1_rect)
            Screen.blit(sfx_volume_text_2, sfx_volume_text_2_rect)
            music_volume_up_button.draw(Screen)
            music_volume_down_button.draw(Screen)
            sfx_volume_up_button.draw(Screen)
            sfx_volume_down_button.draw(Screen)
            back_settings_button.draw(Screen)

        elif switch_settings == 2:
            Screen.blit(keybind_settings_text, keybind_settings_text_rect)
            back_settings_button.draw(Screen)
            for button in keybind_settings_button_list:
                button.draw(Screen)
            if keybind_change_title:
                pygame.draw.rect(Screen, (70,70,70), (0, resolution[1]//2-40, resolution[0], 80))
                Screen.blit(key_change_text, key_change_text_rect)

    elif Switch == 6:
        Screen.blit(credits_text, credits_text_rect)
        Screen.blit(credits_text_1, credits_text_1_rect)
        Screen.blit(credits_text_2, credits_text_2_rect)
        Screen.blit(credits_text_3, credits_text_3_rect)
        back_settings_button.draw(Screen)

    elif Switch == 7:
        Screen.blit(pause_text, pause_text_rect)
        resume_button.draw(Screen)
        settings_button.draw(Screen)

    elif Switch == 8:
        shop_1.draw(Screen)
        player.draw(Screen)
        if show_shop_button:
            shop_button.draw(Screen)
        if show_next_level_button:
            next_level_button.draw(Screen)

    elif Switch == 9:
        current_shop_item = shop_items[item_index]

        Screen.fill((50,50,50))
        pygame.draw.rect(Screen, (30,30,30), (0, 60, resolution[0], resolution[1] - 285))
        back_button.draw(Screen)
        next_button.draw(Screen)
        previous_button.draw(Screen)
        buy_button.draw(Screen)

        current_shop_item.draw()

    pygame.display.update()


# Main Loop --------------------------------------------------------------------------------------------------------------- #
clock = pygame.time.Clock()
restart = False
run = True
while run:
    clock.tick(FPS)

    # key registering
    keys = pygame.key.get_pressed()

    # Setting up some more things --------------------------------------------------------------------------------------------- #
    if Switch == 0:

        # Switch == 1

        new_game_button = button(resolution[0]//2-125, resolution[1]//2, 250, 76, [100,100,100], "New Game")
        settings_button = button(resolution[0]//2-125, resolution[1]//2+96, 250, 76, [100,100,100], "Settings")
        credits_button = button(resolution[0]//2-125, resolution[1]//2+192, 250, 76, [100,100,100], "Credits")
        game_title = text_font_xl.render("Game", True, (255,255,255))
        game_title_rect = game_title.get_rect(center=(resolution[0]//2, resolution[1]//2 - 170))
        main_menu_button_list = [new_game_button, settings_button, credits_button]

        # Switch == 2

        enemy_cooldown_default = 60
        star_cooldown_default = 1
        enemy_bullet_angle_1 = 320
        enemy_bullet_angle_2 = 320
        fleet_health_default = 100
        health_fleet_text_y = 85
        shoot_delay_default = 18
        game_finish_pause_1 = 20
        game_finish_pause_2 = 120
        animation_1_clock = 60
        game_over_timer = 180
        shoot_sfx_index = 0
        health_text_y = 15
        current_level = 11
        fleet_health = 100
        top_border = 0
        border = 15
        neg_2 = -1
        neg_1 = 1

        current_part = levels[str(current_level)]['part'] # integer
        boss_fight = False

        enemy_bullets = []
        enemies = []
        bullets = []
        stars = []

        enemy_cooldown = enemy_cooldown_default
        star_cooldown = star_cooldown_default
        shoot_delay = shoot_delay_default

        player = Player(100, resolution[0]//2 - 50, resolution[1]+99, 16, 104, 99, player_s)
        health_fleet = text_font.render(str(fleet_health), True, (153, 153, 255))
        health = text_font_l.render(str(player.health), True, (255, 200, 200))

        # Switch == 3

        fleet_destroyed = False
        game_over_text_show = False
        game_over_text = text_font_l.render("Game over", True, (255,255,255))
        restart_button = button(resolution[0]//2-125, resolution[1]//2+20, 250, 76, [100,100,100], "Restart")

        game_over_text_rect = game_over_text.get_rect(center=(resolution[0]//2, resolution[1]//2 - 30))

        # Switch == 4

        money_visual = 0
        money_vis_sfx_flip = 0
        summary_text_money = text_font_l.render("Credits: " + str(money_visual), True, (250,250,250))
        summary_text_money_rect = summary_text_money.get_rect(center=(resolution[0]//2, resolution[1]//2))

        # Switch == 5

        back_settings_button = button(resolution[0]//2 - 80, resolution[1]//2 + 200, 160, 76, [100,100,100], "Back")

        # switch_settings == 0
        settings_text = text_font_l.render("Settings", True, (255,255,255)) # dont look here this whole fucking thing is trash
        settings_text_rect = settings_text.get_rect(center=(resolution[0]//2, resolution[1]//2 - 250))
        audio_settings_button = button(resolution[0]//2 - 100, resolution[1]//2 - 100, 200, 76, [100,100,100], "Audio")
        keybind_settings_button = button(resolution[0]//2 - 150, resolution[1]//2 + 50, 300, 76, [100,100,100], "Controls")

        # switch_settings == 1
        audio_settings_text = text_font_l.render("Audio Settings", True, (255,255,255))
        audio_settings_text_rect = audio_settings_text.get_rect(center=(resolution[0]//2, resolution[1]//2 - 250))
        music_volume_text_1 = text_font.render("Background Music Volume", True, (250,250,250))
        music_volume_text_2 = text_font.render(str(int(music_volume*100)) + " %", True, (150,150,150))
        sfx_volume_text_1 = text_font.render("Special Effects Volume", True, (250,250,250))
        sfx_volume_text_2 = text_font.render(str(int(sfx_volume*100)) + " %", True, (150,150,150))
        music_volume_text_1_rect = music_volume_text_1.get_rect(center=(resolution[0]//2, resolution[1]//2 - 120))
        music_volume_text_2_rect = music_volume_text_2.get_rect(center=(resolution[0]//2, resolution[1]//2 - 50))
        sfx_volume_text_1_rect = sfx_volume_text_1.get_rect(center=(resolution[0]//2, resolution[1]//2 + 50))
        sfx_volume_text_2_rect = sfx_volume_text_2.get_rect(center=(resolution[0]//2, resolution[1]//2 + 120))

        music_volume_up_button = button(resolution[0]//2 + 150, resolution[1]//2 - 75, 40, 40, [100,100,100], "+", 0)
        music_volume_down_button = button(resolution[0]//2 - 190, resolution[1]//2 - 75, 40, 40, [100,100,100], "-", 0)

        sfx_volume_up_button = button(resolution[0]//2 + 150, resolution[1]//2 + 95, 40, 40, [100,100,100], "+", 0)
        sfx_volume_down_button = button(resolution[0]//2 - 190, resolution[1]//2 + 95, 40, 40, [100,100,100], "-", 0)
        audio_settings_button_list = [music_volume_up_button, music_volume_down_button, sfx_volume_up_button, sfx_volume_down_button]

        # switch_settings == 2
        keybind_change_title = None # bro what the fuck is even going on
        keybind_settings_text = text_font_l.render("Keybind Settings", True, (255,255,255))
        keybind_settings_text_rect = keybind_settings_text.get_rect(center=(resolution[0]//2, resolution[1]//2 - 250))

        keybind_settings_button_list = []
        count = 0
        for keybind in settings["key_binds"].keys():
            name = f'{keybind.capitalize()} - {str(pygame.key.name(eval(settings["key_binds"][keybind]))).capitalize()}'
            if count in [40,120,200]:
                count += 40 # seriously why i thought THIS would be a good idea
                keybind_settings_button_list.append(button(resolution[0]//2 + 20, resolution[1]//2 - 80 + count-80, 300, 50, [100,100,100], name, 0))
            else:
                keybind_settings_button_list.append(button(resolution[0]//2 - 320, resolution[1]//2 - 80 + count, 300, 50, [100,100,100], name, 0))
                count += 40

        settings_button_list = [back_settings_button, audio_settings_button, keybind_settings_button, music_volume_up_button, music_volume_down_button, sfx_volume_up_button, sfx_volume_down_button, ] + keybind_settings_button_list

        # Switch == 6

        credits_text = text_font.render("Credits", True, (255,255,255))
        credits_text_rect = credits_text.get_rect(center=(resolution[0]//2, resolution[1]//2 - 250))

        credits_text_1 = text_font_s.render("Background Music by Adam Haynes", True, (250,250,250))
        credits_text_2 = text_font_s.render("Sprites by Kenney Vleugels", True, (250,250,250))
        credits_text_3 = text_font_s.render("Development by Igor Zamojski", True, (250,250,250))
        credits_text_1_rect = credits_text_1.get_rect(center=(resolution[0]//2, resolution[1]//2 - 120))
        credits_text_2_rect = credits_text_2.get_rect(center=(resolution[0]//2, resolution[1]//2 - 50))
        credits_text_3_rect = credits_text_3.get_rect(center=(resolution[0]//2, resolution[1]//2 + 20))

        # Switch == 7

        pause_text = text_font_l.render("Game Paused", True, (255,255,255))
        pause_text_rect = pause_text.get_rect(center=(resolution[0]//2, resolution[1]//2 - 150))
        resume_button = button(resolution[0]//2 - 125, resolution[1]//2, 250, 76, [100,100,100], "Resume")
        pause = False

        # Switch == 8

        show_shop_button = False
        show_next_level_button = False
        shop_1 = station(friendly_station_s, 25, 137)
        shop_button = button(resolution[0]//1.5 - 50, resolution[1]//1.5, 150, 50, [100,100,100], "Shop", 0)
        next_level_button = button(resolution[0]//1.5 - 125, resolution[1]//1.5, 300, 50, [100,100,100], "Next Level", 0)

        # Switch == 9

        shop_items = []
        buy_sfx_index = 0
        with open("data/shop_items.json") as f:
            for item in load(f):
                shop_items.append(shopItem(item["sprite"], item["title"], item["price"], item["upgrade"]))

        item_index = 0

        back_button = button(resolution[0]//2 - 75, resolution[1] - 110, 150, 50, [100,100,100], "Back", 0)
        next_button = button(resolution[0]//2 + 100, resolution[1] - 110, 200, 50, [100,100,100], "Next Item", 0)
        previous_button = button(resolution[0]//2 - 300, resolution[1] - 110, 200, 50, [100,100,100], "Last Item", 0)
        buy_button = button(resolution[0]//2-300, resolution[1] - 180, 600, 50, [100,100,100], "Purchase", 0)
        shop_button_list = [back_button, next_button, previous_button, buy_button]


        if restart:
            pygame.mixer.music.load(f"music/part_{current_part}.mp3")
            pygame.mixer.music.set_volume(music_volume)
            pygame.mixer.music.play(-1)
            Switch = 2
        else:
            pygame.mixer.music.load("music/main_menu.mp3")
            pygame.mixer.music.set_volume(music_volume)
            pygame.mixer.music.play(-1)
            Switch = 1

    # Main Menu --------------------------------------------------------------------------------------------------------------- #
    elif Switch == 1:

        spawnStar(3)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if new_game_button.isOver(pos):
                    menu_nav.play()
                    Switch = 2
                    pygame.mixer.music.load(f"music/part_{current_part}.mp3")
                    pygame.mixer.music.set_volume(music_volume)
                    pygame.mixer.music.play(-1)

                if settings_button.isOver(pos):
                    menu_nav.play()
                    Switch = 5

                if credits_button.isOver(pos):
                    menu_nav.play()
                    Switch = 6

            if event.type == pygame.MOUSEMOTION: # change color only when hovering over w/ mouse
                for b in main_menu_button_list:
                    if b.isOver(pos):
                        b.color = [80,80,80]
                    else:
                        b.color = b.color_default

    # The Gameplay ------------------------------------------------------------------------------------------------------------ #
    elif Switch == 2:

        # X button (top right)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # player "fly-in" animation
        if animation_1_clock >= 0:
            player.y += (resolution[1]//1.2 - player.y)//7
            animation_1_clock -= 1

            # passive effect
            for s in stars:
                s.y += s.v
                if s.y > resolution[1] + 15:
                    stars.remove(s)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            redrawGameWindow()
            continue

        # win check
        if len(levels[str(current_level)]["enemies"]) == 0 and len(enemies) == 0:
            if levels[str(current_level+1)]["type"] != "wave":
                pygame.mixer.music.stop()
            Switch = 4

        # generating the stars in the background
        spawnStar(3)

        # moving the player (+ move smoothing)
        if keys[key_binds["left"]] and player.x > border + player.v:
            player.x -= player.v * player.left_v_modifier
            if player.left_v_modifier < 1:
                player.left_v_modifier += player.default_modifier
        elif player.left_v_modifier > 0:
            player.x -= player.v * player.left_v_modifier
            player.left_v_modifier -= player.default_modifier

        if keys[key_binds["right"]] and player.x + player.width < resolution[0] - border - player.v:
            player.x += player.v * player.right_v_modifier
            if player.right_v_modifier < 1:
                player.right_v_modifier += player.default_modifier
        elif player.right_v_modifier > 0:
            player.x += player.v * player.right_v_modifier
            player.right_v_modifier -= player.default_modifier

        if keys[key_binds["up"]] and player.y - player.height * 0.5 > border + player.v + top_border:
            player.y -= player.v * player.up_v_modifier
            if player.up_v_modifier < 1:
                player.up_v_modifier += player.default_modifier
        elif player.up_v_modifier > 0:
            player.y -= player.v * player.up_v_modifier
            player.up_v_modifier -= player.default_modifier

        if keys[key_binds["down"]] and player.y + player.height * 1.5 < resolution[1] - border - player.v: # this border shouldn't work XDD
            player.y += player.v * player.down_v_modifier
            if player.down_v_modifier < 1:
                player.down_v_modifier += player.default_modifier
        elif player.down_v_modifier > 0:
            player.y += player.v * player.down_v_modifier
            player.down_v_modifier -= player.default_modifier

        if keys[key_binds["pause"]]:
            Switch = 7

        # player shooting
        if shoot_delay > 0:
            shoot_delay -= 1
        elif keys[key_binds["shoot"]]:
            bullets.append(bullet(player.damage, player.x - 4 + player.width//2, player.y+10, 20, 8, 17, 0, bullet_s))
            shoot_delay = shoot_delay_default

            shoot_sfx[shoot_sfx_index].play()
            shoot_sfx_index += 1
            if shoot_sfx_index >= len(shoot_sfx):
                shoot_sfx_index = 0

        # boss border
        if boss_fight and current_level in [4,9]:
            top_border = 300
        else:
            top_border = 0

        # enemy spawning
        if len(levels[str(current_level)]["enemies"]) > 0:
            next_enemy = levels[str(current_level)]["enemies"][0] # next enemy type in level
            if enemy_cooldown <= 0:
                enemy_health = enemies_data[next_enemy]['enemy_health']
                enemy_damage = enemies_data[next_enemy]['enemy_damage']
                width = enemies_data[next_enemy]['width']
                height = enemies_data[next_enemy]['height']
                sprite = enemies_data[next_enemy]['sprite']
                boss = enemies_data[next_enemy]['boss']
                value = enemies_data[next_enemy]['value']
                v = enemies_data[next_enemy]['v']
                animation_clock = enemies_data[next_enemy]['animation_clock']
                shoot_countdown = enemies_data[next_enemy]['shoot_countdown']
                h_v_mod = enemies_data[next_enemy]['h_v_mod']
                h_limit = enemies_data[next_enemy]['h_limit']

                if boss:
                    boss_fight = True
                    enemies.append(enemy(eval(sprite), enemy_health, enemy_damage, value, (resolution[0] - width)//2, -height, v, width, height, boss, animation_clock, shoot_countdown))
                else:
                    enemies.append(enemy(eval(sprite), enemy_health, enemy_damage, value, randint(border, resolution[0]-border-width-h_limit), 0-height, v, width, height, boss, animation_clock, shoot_countdown, h_v_mod))

                del levels[str(current_level)]["enemies"][0]
                enemy_cooldown = enemy_cooldown_default
            elif next_enemy not in ['b1']:
                enemy_cooldown -= 1
            else:
                enemy_cooldown -= 0.3

        # collisions & boss mechanics
        for e in enemies:
            # boss mechanics
            if boss:
                boss_health = text_font_xl.render(str(e.health), True, (25,25,25))
                boss_health_rect = boss_health.get_rect(center=(resolution[0]//2, resolution[1]//2))
                if e.sprite == enemy_b1_s and ( (current_level == 4 and e.health > 1500) or current_level == 9 ):
                    if e.shoot_countdown > 0 and e.shoot_countdown != e.shoot_countdown_default//2:
                        e.shoot_countdown -= 1

                    elif e.shoot_countdown == e.shoot_countdown_default//2:
                        if enemy_bullet_angle_1 > 300:
                            neg_1 = -1
                        elif enemy_bullet_angle_1 < 180:
                            neg_1 = 1
                        enemy_shoot.play()
                        enemy_bullets.append(bullet(e.damage, e.x + e.width-85, e.y+e.height-25, -13, 20, 20, -enemy_bullet_angle_1, enemy_bullet_1_s, 1))
                        enemy_bullet_angle_1 += 20 * neg_1
                        e.shoot_countdown -= 1

                    else:
                        if enemy_bullet_angle_2 > 300:
                            neg_2 = -1
                        elif enemy_bullet_angle_2 < 180:
                            neg_2 = 1
                        enemy_shoot.play()
                        enemy_bullets.append(bullet(e.damage, e.x+85, e.y+e.height-25, -13, 20, 20, enemy_bullet_angle_2, enemy_bullet_1_s, 1))
                        enemy_bullet_angle_2 += 20 * neg_2

                        e.shoot_countdown = e.shoot_countdown_default

            # small enemies shooting
            if e.sprite == enemy_s4_s:
                if e.shoot_countdown > 0:
                    e.shoot_countdown -= 1
                else:
                    enemy_shoot.play()
                    enemy_bullets.append(bullet(e.damage, e.x, e.y+e.height-25, 8, 20, 20, 90, enemy_bullet_2_s, 2))
                    enemy_bullets.append(bullet(e.damage, e.x+e.width, e.y+e.height-25, -8, 20, 20, -90, enemy_bullet_2_s, 2))
                    e.shoot_countdown = e.shoot_countdown_default

            # collisions
            player_enemy_offset = (round(player.rect[0] - e.rect[0]), round(player.rect[1] - e.rect[1]))
            result = e.mask.overlap(player.mask, player_enemy_offset)
            if result and e.health >= 0:
                player.health -= floor(e.damage*4.99)
                e.health = 0
                e.explode()
                enemy_die.play()
                hit.play()
                health = text_font_l.render(str(player.health), False, (255, 200, 200))
                if player.health <= 0:
                    Switch = 3
                    pygame.mixer.music.stop()
                    player_die.play()

            for b in bullets:
                bullet_enemy_offset = (round(b.rect[0] - e.rect[0]), round(b.rect[1] - e.rect[1]))
                result = e.mask.overlap(b.mask, bullet_enemy_offset)
                if result:
                    bullets.remove(b)
                    e.health -= b.damage

                    if e.health <= 0:
                        if e.boss:
                            pygame.mixer.music.stop()
                            enemy_die_l.play()
                        else:
                            enemy_die.play()
                        player.money += e.value
                    else:
                        hit.play()

            for b in enemy_bullets:
                player_bullet_offset = (round(b.rect[0] - player.rect[0]), round(b.rect[1] - player.rect[1]))
                result = player.mask.overlap(b.mask, player_bullet_offset)
                if result:
                    enemy_bullets.remove(b)
                    player.health -= b.damage
                    health = text_font_l.render(str(player.health), True, (255, 200, 200))
                    if player.health <= 0:
                        Switch = 3
                        pygame.mixer.music.stop()
                        player_die.play()
                    else:
                        hit.play()

        # fixes
        if player.down_v_modifier < 0:
            player.down_v_modifier = player.default_modifier
        if player.up_v_modifier < 0:
            player.up_v_modifier = player.default_modifier
        if player.left_v_modifier < 0:
            player.left_v_modifier = player.default_modifier
        if player.right_v_modifier < 0:
            player.right_v_modifier = player.default_modifier

    # Game Over --------------------------------------------------------------------------------------------------------------- #
    elif Switch == 3:
        for e in enemies:
            enemies.remove(e)
        for b in bullets:
            bullets.remove(b)
        for b in enemy_bullets:
            enemy_bullets.remove(b)

        spawnStar(3)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.isOver(pos):
                    menu_nav.play()
                    del player
                    restart = True
                    Switch = 0

            if event.type == pygame.MOUSEMOTION:
                if restart_button.isOver(pos):
                    new_game_button.color = [80,80,80]
                else:
                    restart_button.color = restart_button.color_default

    # Level Summary ----------------------------------------------------------------------------------------------------------- #
    elif Switch == 4:

        spawnStar(3)
        for e in enemies:
            enemies.pop(enemies.index(e))

        # player, health & health_fleet "fly-out" animation
        if game_finish_pause_1 == 10:
            if levels[str(current_level)]["player_health_refill"] == True:
                player.health = player.health_default
                health = text_font_l.render(str(player.health), False, (255, 200, 200))
            if levels[str(current_level)]["fleet_health_refill"] == True:
                fleet_health = fleet_health_default
                health_fleet = text_font.render(str(fleet_health), True, (153, 153, 255))
            health_fleet = text_font.render(str(fleet_health), True, (153, 153, 255))
            health = text_font_l.render(str(player.health), True, (255, 200, 200))

        if player.y > -player.height*5:
            if game_finish_pause_1 < 0:
                player.y -= player.v * player.up_v_modifier
                health_text_y -= 5 * player.up_v_modifier
                health_fleet_text_y -= 5 * player.up_v_modifier
                if player.up_v_modifier < 3:
                    player.up_v_modifier += player.default_modifier
            else:
                player.up_v_modifier = player.default_modifier
                game_finish_pause_1 -= 1
        else:
            summary_text_money = text_font_l.render("Credits: " + str(money_visual), True, (250,250,250))
            summary_text_money_rect = summary_text_money.get_rect(center =((resolution[0]//2, resolution[1]//2)))

            if money_visual != player.money:
                if player.money - money_visual >= 15:
                    money_visual += 15
                else:
                    money_visual += player.money - money_visual

                # sfx
                if money_vis_sfx_flip == 0:
                    money_vis_sfx_flip = 4
                    money.play()
                else:
                    money_vis_sfx_flip -= 1

            elif str(current_level+1) in levels and game_finish_pause_2 < 0:

                # resetting stats for a new level
                show_next_level_button = False
                money_vis_sfx_flip = 0
                current_level += 1
                game_finish_pause_1 = 20
                game_finish_pause_2 = 120
                animation_1_clock = 60
                player.x = resolution[0]//2 - 50
                player.y = resolution[1]+99
                boss_fight = False
                current_part = levels[str(current_level)]['part']
                boss_exists = levels[str(current_level)]["boss_exists"]
                health_fleet_text_y = 85
                health_text_y = 15
                top_border = 0
                player.down_v_modifier = player.default_modifier
                player.up_v_modifier = player.default_modifier
                player.left_v_modifier = player.default_modifier
                player.right_v_modifier = player.default_modifier
                enemy_bullet_angle_1 = 320
                enemy_bullet_angle_2 = 320
                neg_2 = -1
                neg_1 = 1


                if levels[str(current_level)]["type"] == "wave":
                    if current_level > 2:
                        if levels[str(current_level-1)]["part"] != current_part or levels[str(current_level-1)]["type"] == "shop":
                            pygame.mixer.music.load(f"music/part_{current_part}.mp3")
                            pygame.mixer.music.set_volume(music_volume)
                            pygame.mixer.music.play(-1)
                    for s in stars:
                        s.star_modifier = 3
                    Switch = 2

                elif levels[str(current_level)]["type"] == "shop":
                    for s in stars:
                        s.star_modifier = 0.3
                        s.v = (s.thickness - s.rotation) * s.star_modifier
                        s.x = randint(0, resolution[0])
                    Switch = 8
                    pygame.mixer.music.load(f"music/shop.mp3")
                    pygame.mixer.music.set_volume(music_volume)
                    pygame.mixer.music.play(-1)

            elif str(current_level+1) not in levels and game_finish_pause_2 < 0:
                print("game completed")

            else:
                game_finish_pause_2 -= 1


        # X button (top right)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    # Settings ---------------------------------------------------------------------------------------------------------------- #
    elif Switch == 5:

        spawnStar(3)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if keybind_change_title:
                if event.type == pygame.KEYDOWN:
                    print(pygame.K_SPACE)
                    print(event.key)
                    for key in keybinds: # see keybinds.json
                        if event.key == eval(key):
                            settings["key_binds"][keybind_change_title] = key
                            keybind_change_title = None
                            menu_nav.play()
                            keybind_settings_button_list = []
                            count = 0
                            for keybind in settings["key_binds"].keys():
                                name = f'{keybind.capitalize()} - {str(pygame.key.name(eval(settings["key_binds"][keybind]))).capitalize()}'
                                if count in [40,120,200]:
                                    count += 40
                                    keybind_settings_button_list.append(button(resolution[0]//2 + 20, resolution[1]//2 - 80 + count-80, 300, 50, [100,100,100], name, 0))
                                else:
                                    keybind_settings_button_list.append(button(resolution[0]//2 - 320, resolution[1]//2 - 80 + count, 300, 50, [100,100,100], name, 0))
                                    count += 40
                        key_binds = {
                            "up": eval(settings["key_binds"]["up"]),
                            "left": eval(settings["key_binds"]["left"]),
                            "down": eval(settings["key_binds"]["down"]),
                            "right": eval(settings["key_binds"]["right"]),
                            "shoot": eval(settings["key_binds"]["shoot"]),
                            "pause": eval(settings["key_binds"]["pause"])
                        }

            if event.type == pygame.QUIT:
                run = False

            if not keybind_change_title:
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if switch_settings == 0:

                        if audio_settings_button.isOver(pos):
                            menu_nav.play()
                            switch_settings = 1

                        elif keybind_settings_button.isOver(pos):
                            menu_nav.play()
                            switch_settings = 2

                        elif back_settings_button.isOver(pos):
                            menu_nav.play()
                            if pause:
                                Switch = 7
                            else:
                                Switch = 1

                    elif switch_settings == 1:

                        if music_volume_up_button.isOver(pos) and round(music_volume, 2) <= 0.98:
                            menu_nav.play()
                            music_volume += 0.02
                            if music_volume < 0:
                                music_volume = 0
                            music_volume_text_2 = text_font.render(str(int(music_volume*100)) + " %", True, (150,150,150))
                            music_volume_text_2_rect = music_volume_text_2.get_rect(center=(resolution[0]//2, resolution[1]//2 - 50))
                            pygame.mixer.music.set_volume(music_volume)

                        elif music_volume_down_button.isOver(pos) and round(music_volume, 2) >= 0.02:
                            menu_nav.play()
                            music_volume -= 0.02
                            if music_volume < 0:
                                music_volume = 0
                            music_volume_text_2 = text_font.render(str(int(music_volume*100)) + " %", True, (150,150,150))
                            music_volume_text_2_rect = music_volume_text_2.get_rect(center=(resolution[0]//2, resolution[1]//2 - 50))
                            pygame.mixer.music.set_volume(music_volume)

                        elif sfx_volume_up_button.isOver(pos) and round(sfx_volume, 2) <= 0.98:
                            sfx_volume += 0.02
                            if sfx_volume < 0:
                                sfx_volume = 0
                            sfx_volume_text_2 = text_font.render(str(int(sfx_volume*100)) + " %", True, (150,150,150))
                            sfx_volume_text_2_rect = sfx_volume_text_2.get_rect(center=(resolution[0]//2, resolution[1]//2 + 120))
                            shoot.set_volume(sfx_volume)
                            menu_nav.set_volume(sfx_volume)
                            shoot.play()

                        elif sfx_volume_down_button.isOver(pos) and round(sfx_volume, 2) >= 0.02:
                            sfx_volume -= 0.02
                            if sfx_volume < 0:
                                sfx_volume = 0
                            sfx_volume_text_2 = text_font.render(str(int(sfx_volume*100)) + " %", True, (150,150,150))
                            sfx_volume_text_2_rect = sfx_volume_text_2.get_rect(center=(resolution[0]//2, resolution[1]//2 + 120))
                            shoot.set_volume(sfx_volume)
                            menu_nav.set_volume(sfx_volume)
                            shoot.play()

                        elif back_settings_button.isOver(pos):
                            menu_nav.play()
                            for sfx in buy_sfx:
                                sfx.set_volume(sfx_volume)
                            for sfx in shoot_sfx:
                                sfx.set_volume(sfx_volume)
                            menu_nav_false.set_volume(sfx_volume)
                            enemy_shoot.set_volume(sfx_volume)
                            enemy_die_l.set_volume(sfx_volume)
                            player_die.set_volume(sfx_volume)
                            enemy_die.set_volume(sfx_volume)
                            fleet_hit.set_volume(sfx_volume)
                            menu_nav.set_volume(sfx_volume)
                            money.set_volume(sfx_volume)
                            shoot.set_volume(sfx_volume)
                            hit.set_volume(sfx_volume)

                            new_settings = {}
                            new_settings['sfx_volume'] = sfx_volume
                            new_settings['music_volume'] = music_volume
                            new_settings['key_binds'] = lambda x: (str(key) for key in key_binds)

                            with open("data/settings.json", "w") as f:
                                dump(settings, f, indent=4)

                            switch_settings = 0

                    elif switch_settings == 2:

                        for b in keybind_settings_button_list:
                            if b.isOver(pos):
                                menu_nav.play()
                                keybind_change_title = b.text_str.split(' ')[0].lower()
                                key_change_text = text_font.render(f"Select a new key for \"{keybind_change_title.capitalize()}\"", True, (250,250,250))
                                key_change_text_rect = key_change_text.get_rect(center=(resolution[0]//2, resolution[1]//2))

                        if back_settings_button.isOver(pos):
                            menu_nav.play()
                            switch_settings = 0
                            new_settings = {}
                            new_settings['sfx_volume'] = sfx_volume
                            new_settings['music_volume'] = music_volume
                            new_settings['key_binds'] = lambda x: (str(key) for key in key_binds)

                            with open("data/settings.json", "w") as f:
                                dump(settings, f, indent=4)

                if event.type == pygame.MOUSEMOTION:
                    for b in settings_button_list + keybind_settings_button_list:
                        if b.isOver(pos):
                            b.color = [80,80,80]
                        else:
                            b.color = b.color_default

    # Credits ----------------------------------------------------------------------------------------------------------------- #
    elif Switch == 6:

        spawnStar(3)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_settings_button.isOver(pos):
                    menu_nav.play()
                    Switch = 1

            if event.type == pygame.MOUSEMOTION:
                if back_settings_button.isOver(pos):
                    back_settings_button.color = [80,80,80]
                else:
                    back_settings_button.color = back_settings_button.color_default

    # Pause Menu -------------------------------------------------------------------------------------------------------------- #
    elif Switch == 7:

        pause = True
        spawnStar(3)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.isOver(pos):
                    menu_nav.play()
                    pause = False

                    if levels[str(current_level)]["type"] == "wave":
                        Switch = 2
                    elif levels[str(current_level)]["type"] == "shop":
                        Switch = 8

                if settings_button.isOver(pos):
                    menu_nav.play()
                    Switch = 5

            if event.type == pygame.MOUSEMOTION:
                if resume_button.isOver(pos):
                    resume_button.color = [80,80,80]
                else:
                    resume_button.color = resume_button.color_default

                if settings_button.isOver(pos):
                    settings_button.color = [80,80,80]
                else:
                    settings_button.color = settings_button.color_default

    # Shop level -------------------------------------------------------------------------------------------------------------- #
    elif Switch == 8:

        spawnStar(0.3)
        if animation_1_clock >= 0:
            player.y += (resolution[1]//1.2 - player.y)//7
            animation_1_clock -= 1

            # passive effect
            for s in stars:
                s.y += s.v
                if s.y > resolution[1] + 15:
                    stars.remove(s)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            redrawGameWindow()
            continue

        # moving the player (+ move smoothing)
        if keys[key_binds["left"]] and player.x > border + player.v:
            player.x -= player.v * player.left_v_modifier
            if player.left_v_modifier < 1:
                player.left_v_modifier += player.default_modifier
        elif player.left_v_modifier > 0:
            player.x -= player.v * player.left_v_modifier
            player.left_v_modifier -= player.default_modifier

        if keys[key_binds["right"]] and player.x + player.width < resolution[0] - border - player.v:
            player.x += player.v * player.right_v_modifier
            if player.right_v_modifier < 1:
                player.right_v_modifier += player.default_modifier
        elif player.right_v_modifier > 0:
            player.x += player.v * player.right_v_modifier
            player.right_v_modifier -= player.default_modifier

        if keys[key_binds["up"]] and player.y - player.height * 0.5 > border + player.v + top_border:
            player.y -= player.v * player.up_v_modifier
            if player.up_v_modifier < 1:
                player.up_v_modifier += player.default_modifier
        elif player.up_v_modifier > 0:
            player.y -= player.v * player.up_v_modifier
            player.up_v_modifier -= player.default_modifier

        if keys[key_binds["down"]] and player.y + player.height * 1.5 < resolution[1] - border - player.v: # this border shouldn't work XDD
            player.y += player.v * player.down_v_modifier
            if player.down_v_modifier < 1:
                player.down_v_modifier += player.default_modifier
        elif player.down_v_modifier > 0:
            player.y += player.v * player.down_v_modifier
            player.down_v_modifier -= player.default_modifier

        # collisions
        show_shop_button = False
        show_next_level_button = False
        if player.x > shop_1.active_x and player.x < shop_1.active_x + shop_1.active_side:
            if player.y > shop_1.active_y - shop_1.active_side//2 and player.y < shop_1.active_y + shop_1.active_side//2:
                show_shop_button = True

        if player.y - player.height * 0.5 <= border + player.v + top_border: # next level button
            show_next_level_button = True

        if keys[key_binds["pause"]]:
            Switch = 7

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if shop_button.isOver(pos) and show_shop_button:
                    menu_nav.play()
                    Switch = 9

                if next_level_button.isOver(pos) and show_next_level_button:
                    menu_nav.play()
                    pygame.mixer.music.stop()
                    Switch = 4

            if event.type == pygame.MOUSEMOTION:
                if shop_button.isOver(pos) and show_shop_button:
                    shop_button.color = [80,80,80]
                else:
                    shop_button.color = shop_button.color_default

                if next_level_button.isOver(pos) and show_next_level_button:
                    next_level_button.color = [80,80,80]
                else:
                    next_level_button.color = next_level_button.color_default

    # Shop UI ------------------------------------------------------------------------------------------------------------------- #
    elif Switch == 9:

        spawnStar(0.3)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    menu_nav.play()
                    player.down_v_modifier = 0
                    player.up_v_modifier = 0
                    player.left_v_modifier = 0
                    player.right_v_modifier = 0
                    Switch = 8

                if next_button.isOver(pos):
                    menu_nav.play()
                    if item_index+1 < len(shop_items):
                        item_index += 1
                    else:
                        item_index = 0

                if previous_button.isOver(pos):
                    menu_nav.play()
                    if item_index-1 >= 0:
                        item_index -= 1
                    else:
                        item_index = len(shop_items) - 1

                if buy_button.isOver(pos):
                    if player.money >= shop_items[item_index].price:

                        buy_sfx[buy_sfx_index].play()
                        buy_sfx_index += 1
                        if buy_sfx_index >= len(buy_sfx):
                            buy_sfx_index = 0

                        player.money -= shop_items[item_index].price
                        exec(shop_items[item_index].upgrade)
                    else:
                        menu_nav_false.play()

            if event.type == pygame.MOUSEMOTION:
                for b in shop_button_list:
                    if b.isOver(pos):
                        b.color = [80,80,80]
                    else:
                        b.color = b.color_default


    # Things below apply to every Switch case --------------------------------------------------------------------------------- #
    # passive effects
    for s in stars:
        s.y += s.v
        if s.y > resolution[1] + 15:
            stars.remove(s)

    if not pause:
        for b in bullets:
            b.y -= b.v
            if b.y < 0 - b.height:
                bullets.remove(b)

        for e in enemies:
            if e.boss and ( (current_level == 4 and e.health > 1500) or (current_level == 9 and e.health > 0) or (current_level == 11) ) and e.y < -e.height//2:
                e.y += e.v
                player.y += e.v
            elif e.boss and current_level == 4 and e.health <= 1500:
                e.y -= e.v
                boss_health = text_font_xl.render(str(e.health), True, (0,0,0))
                if e.y < -e.height*1.5:
                    enemies.pop(enemies.index(e))
                    if levels[str(current_level+1)]["type"] != "wave":
                        pygame.mixer.music.stop()
                    Switch = 4
            elif not e.boss:
                e.y += e.v
                if e.h_v_mod:

                    e.x += e.h_v_mod*sin(radians(e.h_v*pi)) * e.neg
                    e.h_v += 1

            if e.animation_clock <= 0:
                enemies.pop(enemies.index(e))

            if e.y > resolution[1] + 15:
                fleet_health -= e.damage
                enemies.remove(e)
                fleet_hit.play()
                health_fleet = text_font.render(str(fleet_health), True, (153, 153, 255))
                if fleet_health <= 0:
                    Switch = 3
                    pygame.mixer.music.stop()
                    player_die.play()

        for b in enemy_bullets:
            if b.config == 1:
                b.y -= b.y_increment
                b.x += b.x_increment
                if b.y > resolution[1]*1.5 + b.height:
                    enemy_bullets.remove(b)

            elif b.config == 2:
                b.y += abs(b.v)
                b.x -= b.v

    redrawGameWindow()

pygame.quit()
