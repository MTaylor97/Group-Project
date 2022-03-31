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
        self.image = sprite_sheet.get_image(150, 0, 24, 44, 4, constants.white).convert_alpha()
        self.x = constants.WIDTH/2
        self.y = constants.HEIGHT/2 + 88 # measure from front of bus
        self.rect = self.image.get_rect(center=(self.x, self.y))

class BG(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = 'bg'
        self.image = sprite_sheet.get_image(0, 0, 150, 150, 4, None).convert_alpha()
        self.x = constants.WIDTH/2
        self.y = constants.HEIGHT/2
        self.rect = self.image.get_rect(center=(self.x, self.y))

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type, angle, distance):
        super().__init__()
        self.type = type
        self.angle = angle
        self.distance = distance
        self.distance_sf = 5 #10pixels == 1cm. So it's 24cm from middle of bus to top of screen.
        if angle > 0:
            self.x = (constants.WIDTH/2) + math.sin(math.radians(angle))*distance*self.distance_sf
        else:
            self.x = (constants.WIDTH/2) + math.sin(math.radians(angle))*distance*self.distance_sf
        self.y = (constants.HEIGHT/2) - math.cos(math.radians(angle))*distance*self.distance_sf
        self.front = (self.x,self.y)
        
        if self.type == 'soldier':
            self.image = sprite_sheet.get_image(180, 0, 9, 7, 4, constants.white).convert_alpha()
            
            self.y -= 14
            
        elif self.type == 'redcar':
            self.image = sprite_sheet.get_image(190, 0, 19, 35, 4, constants.white).convert_alpha()
            self.y -= 70
            
        self.rect = self.image.get_rect(center=(self.x, self.y))

