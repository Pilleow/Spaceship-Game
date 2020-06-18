import pygame
from random import randint, choice
from math import sin, cos, radians

pygame.mixer.pre_init(44100,-16,2,512)
pygame.mixer.init()
pygame.init()
resolution = (750, 800)
Screen = pygame.display.set_mode(resolution)
text_font_s = pygame.font.SysFont('Consolas', 30)
text_font = pygame.font.SysFont('Consolas', 50)
text_font_l = pygame.font.SysFont('Consolas', 70)

explosion_s = [pygame.image.load("sprites/explosion/explosion_1.png").convert_alpha(), pygame.image.load("sprites/explosion/explosion_2.png").convert_alpha(), pygame.image.load("sprites/explosion/explosion_3.png").convert_alpha()]
explosion_s_l = [pygame.image.load("sprites/explosion/explosion_1_l.png").convert_alpha(), pygame.image.load("sprites/explosion/explosion_2_l.png").convert_alpha(), pygame.image.load("sprites/explosion/explosion_3_l.png").convert_alpha()]

class Player(object):
    def __init__(self, health, x, y, v, width, height, sprite):
        self.x = x
        self.y = y
        self.v = v // 2
        self.width = width
        self.height = height
        self.sprite = sprite
        self.default_modifier = 0.07
        self.left_v_modifier = self.default_modifier
        self.right_v_modifier = self.default_modifier
        self.up_v_modifier = self.default_modifier
        self.down_v_modifier = self.default_modifier

        self.health_default = health
        self.health = self.health_default
        self.damage = 35
        self.money = 0

        self.setMask()

    def draw(self, Screen):
        Screen.blit(self.sprite, (int(self.x), int(self.y)))
        self.setMask()

    def setMask(self):
        self.mask = pygame.mask.from_surface(self.sprite)
        self.rect = self.sprite.get_rect(center=(self.x+self.width//2, self.y+self.height//2))


class enemy(object):
    def __init__(self, sprite, health, damage, value, x, y, v, width, height, boss, animation_clock, shoot_countdown, h_v_mod=None):
        self.x = x
        self.y = y
        self.v = v // 2
        self.width = width
        self.height = height
        self.neg = choice([-1,1])

        self.sprite = sprite
        self.health = health
        self.damage = damage
        self.boss = boss
        self.value = value
        self.h_v_mod=h_v_mod
        self.h_v = 0
        self.animation_clock_default = animation_clock
        self.animation_clock = self.animation_clock_default
        self.shoot_countdown_default = shoot_countdown
        self.shoot_countdown = self.shoot_countdown_default

        self.setMask()

    def draw(self, Screen):
        if self.health > 0:
            self.setMask()
            Screen.blit(self.sprite, (self.x, self.y))

        elif self.health <= 0:
            self.explode()
            self.explode_center = self.sprite.get_rect(center=(self.x+self.width//2, self.y+self.height//2))
            Screen.blit(self.sprite, self.explode_center)

    def setMask(self):
        self.mask = pygame.mask.from_surface(self.sprite)
        self.rect = self.sprite.get_rect(center=(self.x+self.width//2, self.y+self.height//2))

    def explode(self):
        self.rect = (resolution[0], resolution[1], 0, 0)

        if self.boss:
            selected_lib = explosion_s_l
        else:
            selected_lib = explosion_s

        if self.animation_clock > self.animation_clock_default//5 * 4:
            self.sprite = selected_lib[0]
        elif self.animation_clock <= self.animation_clock_default//5 * 4 and self.animation_clock > self.animation_clock_default//5 * 3:
            self.sprite = selected_lib[1]
        elif self.animation_clock <= self.animation_clock_default//5 * 3 and self.animation_clock > self.animation_clock_default//5 * 2:
            self.sprite = selected_lib[2]
        elif self.animation_clock <= self.animation_clock_default//5 * 2 and self.animation_clock > self.animation_clock_default//5:
            self.sprite = selected_lib[1]
        elif self.animation_clock <= self.animation_clock_default//5 and self.animation_clock > 0:
            self.sprite = selected_lib[0]

        self.animation_clock -= 1


class station(object):
    def __init__(self, animation, x, y):
        self.animation = animation
        self.x = x
        self.y = y
        self.animation_clock = 80
        self.index = 0

        self.active_x = 355+self.x
        self.active_y = 67+self.y
        self.active_side = 99

    def draw(self, Screen):
        Screen.blit(self.animation[self.index], (self.x, self.y))

        if self.animation_clock == 70:
            self.index += 1
        elif self.animation_clock == 60:
            self.index += 1
        elif self.animation_clock == 10:
            self.index += 1
        elif self.animation_clock <= 0:
            self.index = 0
            self.animation_clock = 80

        self.animation_clock -= 1


class shopItem(object):
    def __init__(self, sprite, text, price, upgrade):
        self.sprite = pygame.image.load(f"sprites/shop/{sprite}.png")
        self.text = text_font.render(text, True, (250,250,250))
        self.price = price
        self.upgrade = upgrade

        self.text_rect = self.text.get_rect(center=(resolution[0]//2, resolution[1] - 285))
        self.sprite_rect = self.sprite.get_rect(center=(resolution[0]//2, resolution[1]//2 - 125))

    def draw(self):
        Screen.blit(self.sprite, self.sprite_rect)
        Screen.blit(self.text, self.text_rect)


class bullet(object):
    def __init__(self, damage, x, y, v, width, height, angle, sprite, config=None):
        self.x = round(x)
        self.y = round(y)
        self.v = v // 2
        self.width = width
        self.height = height
        self.angle = angle
        self.damage = damage
        self.config = config

        if self.config == 1: # b1
            self.y_increment = round(self.v - self.v * cos(radians(angle)))
            self.x_increment = round(self.v * sin(radians(angle)) * 1.7)

            if self.angle > 0.0:
                self.sprite = pygame.transform.rotate(sprite, 9 * (angle+180)/17)
            else:
                self.sprite = pygame.transform.rotate(sprite, 9 * (angle-180)/17)

        elif self.config == 2: # s4
            self.sprite = pygame.transform.rotate(sprite, angle)

        else:
            self.sprite = sprite

        self.setMask()

    def draw(self, Screen):
        Screen.blit(self.sprite, self.rect)
        self.setMask()

    def setMask(self):
        self.mask = pygame.mask.from_surface(self.sprite)
        self.rect = self.sprite.get_rect(center=(self.x+self.width//2, self.y+self.height//2))


class star(object):
    def __init__(self, star_modifier):
        self.thickness = randint(1,10)
        self.rotation = randint(0,10)
        self.star_modifier = star_modifier
        self.x = randint(0, resolution[0])
        self.y = -15
        self.v = (self.thickness - self.rotation) * self.star_modifier

        self.color = randint(10,50)
        self.points = ((self.x - self.thickness + self.rotation, self.y + self.rotation), (self.x - self.rotation ,self.y + self.thickness - self.rotation), (self.x + self.thickness - self.rotation, self.y - self.rotation), (self.x + self.rotation, self.y - self.thickness + self.rotation))

    def draw(self, Screen):
        self.points = ((self.x - self.thickness + self.rotation, self.y + self.rotation), (self.x + self.rotation ,self.y + self.thickness - self.rotation), (self.x + self.thickness - self.rotation, self.y - self.rotation), (self.x - self.rotation, self.y - self.thickness + self.rotation))
        pygame.draw.polygon(Screen, (self.color, self.color, self.color), self.points)


class button(object):
    def __init__(self, x, y, width, height, color_default, text="", size=1):
        self.x = x
        self.y = y
        self.text_str = text
        self.width = width
        self.height = height
        self.color_default = color_default
        self.color = self.color_default

        if size == 0: # small
            self.text = text_font_s.render(text, True, (250,250,250))
        elif size == 1: # normal
            self.text = text_font.render(text, True, (250,250,250))
        elif size == 2: # large
            self.text = text_font_l.render(text, True, (250,250,250))
        elif size == 3: # extra large
            self.text = text_font_xl.render(text, True, (250,250,250))

        self.text_box = self.text.get_rect(center=(self.x+self.width//2, self.y+self.height//2))

    def draw(self, Screen):
        pygame.draw.rect(Screen, tuple(self.color), (self.x, self.y, self.width, self.height))
        Screen.blit(self.text, self.text_box)

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False
