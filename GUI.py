
import sys
import numpy   #unneeded rn
import pygame
from pygame.locals import *

from Sprites import Obstacle, Bus, BG
import constants


class GUI:
    def __init__(self):
        pygame.init()
        self.fps = 24    
        self.fpsClock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT), 0, 32)
        pygame.display.set_caption("Kinchbus Kollision Avoidance System GUI")

        #self.screen.fill(constants.white)
        self.main_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.bus = Bus()
        self.bg = BG()
        
        self.main_sprites.add(self.bg, self.bus)
        
    def quit(self):
        pygame.quit()

    # def add_obstacle(self, Obstacle):
    #     self.obstacle_sprites.add(Obstacle)
    
    def run_1_loop(self):
        self.main_sprites.draw(self.screen)
        self.draw_distances()
        self.obstacle_sprites.draw(self.screen)
        
        self.obstacle_sprites.empty()
        pygame.display.update()

    def draw_distances(self):
        for sprite in self.obstacle_sprites:
            if sprite.type == 'bus' or sprite.type == 'bg':
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

            #display the display
            self.obstacle_sprites.add(Obstacle('soldier', 0, 20))
            self.obstacle_sprites.add(Obstacle('redcar', 45, 15))
            
            self.main_sprites.draw(self.screen)
            self.obstacle_sprites.draw(self.screen)
            #self.draw_distances()
            #self.draw_distances(constants.white)

            self.obstacle_sprites.empty()

            self.fpsClock.tick(self.fps)

if __name__ == '__main__':
    gui = GUI()
    gui.run()
    #gui.run_1_loop()
