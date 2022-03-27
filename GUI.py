
import sys
import numpy   #unneeded rn
import pygame
from pygame.locals import *

from Sprites import Obstacle, Bus
import constants


class GUI:
    def __init__(self):
        pygame.init()
        self.fps = 24    
        self.fpsClock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT), 0, 32)
        pygame.display.set_caption("Kinchbus Kollision Avoidance System GUI")

        self.screen.fill(constants.white)
        self.all_sprites = pygame.sprite.Group()
        self.bus = Bus()
        # self.O = Obstacle('Person', 90, 15)
        self.all_sprites.add(self.bus)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        pygame.display.update()


    def quit(self):
        pygame.quit()

        

    def add_obj(self, O):
        self.all_sprites.add(O)

    
    def run_1_loop(self):
        # self.all_sprites.empty()
        # self.all_sprites.add(self.bus)

        self.all_sprites.update()
        pygame.display.update()
        self.screen.fill(constants.white)
        self.draw_distances()
        self.all_sprites.draw(self.screen)

        self.all_sprites.empty()
        self.all_sprites.add(self.bus)


    def draw_distance(self):
        start = (constants.WIDTH/2,constants.HEIGHT/2)
        end = (self.O.x, self.O.y)
        pygame.draw.line(self.screen, constants.red, start, end, 3)
        font = pygame.font.SysFont('Calibri', 20, True, False)
        text = font.render(str(self.O.distance)+'cm', True, constants.white, constants.red)
        self.screen.blit(text, ((start[0]+end[0])/2-20, (start[1]+end[1])/2-10))

    def draw_distances(self):
        for sprite in self.all_sprites:
            if sprite.type == 'bus':
                continue
            start = (constants.WIDTH/2,constants.HEIGHT/2)
            end = (sprite.x, sprite.y)
            pygame.draw.line(self.screen, constants.red, start, end, 3)
            font = pygame.font.SysFont('Calibri', 20, True, False)
            text = font.render(str(round(sprite.distance))+'cm', True, constants.white, constants.red)
            self.screen.blit(text, ((start[0]+end[0])/2-20, (start[1]+end[1])/2-10))


    def run(self):
        while True:
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            #update display
            pygame.display.update()
            self.all_sprites.update()

            #display the display
            self.screen.fill(constants.white)
            self.draw_distance()
            self.all_sprites.draw(self.screen)          

            self.fpsClock.tick(self.fps)

if __name__ == '__main__':
    gui = GUI()
    gui.run()
