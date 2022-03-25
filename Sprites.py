import pygame
import spritesheet
import constants
import math

joes_art = pygame.image.load(r"Images/Spritesheet.png")#.convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(joes_art)

class Bus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = 'bus'
        self.image = sprite_sheet.get_image(0, 0, 22, 26, 4, constants.white).convert_alpha()
        self.x = constants.WIDTH/2
        self.y = constants.HEIGHT/2
        self.rect = self.image.get_rect(center=(self.x, self.y))

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type, angle, distance):
        super().__init__()
        self.type = type
        self.angle = angle
        self.distance = distance
        self.distance_sf = 10 #10pixels == 1cm. So it's 24cm from middle of bus to top of screen.

        if angle > 0:
            self.x = (constants.WIDTH/2) + round(math.sin(abs(angle)))*distance*self.distance_sf
            print(self.x)
        else:
            self.x = (constants.WIDTH/2) - round(math.sin(abs(angle)))*distance*self.distance_sf
            print(self.x)

        self.y = (constants.HEIGHT/2) - round(math.cos(abs(angle)))*distance*self.distance_sf
        print(self.y)

        if self.type == 'person':
            self.image = sprite_sheet.get_image(30, 0, 9,23, 4, constants.white).convert_alpha()
        elif self.type == 'car':
            self.image = sprite_sheet.get_image(60, 0, 30, 30, 4, constants.white).convert_alpha()

        self.rect = self.image.get_rect(center=(self.x, self.y))

