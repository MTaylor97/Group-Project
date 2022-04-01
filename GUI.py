
import sys
import pygame

from Sprites import Obstacle, Bus, BG
import constants
import spritesheet

class GUI:
    def __init__(self):
        pygame.init()
        
        self.fps = 60 
        self.fpsClock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT), 0, 32)
        pygame.display.set_caption("Kinchbus Kollision Avoidance System GUI")

        joes_art = pygame.image.load(r"Images/Spritesheet.png").convert_alpha()
        self.sprite_sheet = spritesheet.SpriteSheet(joes_art)

        self.background_sprites = pygame.sprite.Group()
        self.foreground_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.bus = Bus(self.sprite_sheet)
        self.bg2 = BG(self.sprite_sheet, -constants.HEIGHT/2)
        self.bg1 = BG(self.sprite_sheet, constants.HEIGHT/2)
        
        self.background_sprites.add(self.bg1, self.bg2)
        self.foreground_sprites.add(self.bus)

    def obstacle_found(self, type, angle, distance):
        self.obstacle_sprites.add(Obstacle(self.sprite_sheet, type, angle, distance))

    def hud(self):
        font = pygame.font.SysFont('Calibri', 20, True, False)
        colour = constants.red
        for sprite in self.obstacle_sprites:
            if sprite.front[1] <= 0: # off screen
                pygame.draw.polygon(self.screen, colour, [[sprite.x-10, 20],[sprite.x+10, 20],[sprite.x, 0]])
                text = font.render(str(sprite.type), True, constants.white, colour)
                self.screen.blit(text, (sprite.x-10, 20))
                text = font.render(str(round(sprite.distance))+'cm', True, constants.white, colour)
                self.screen.blit(text, (sprite.x-10, 40))
                continue

            if sprite.distance <= 20: # if close
                start = (constants.WIDTH/2,constants.HEIGHT/2)
                end = (sprite.front[0], sprite.front[1])
                pygame.draw.line(self.screen, colour, start, end, 3)
                if sprite.type == 'soldier':
                    pygame.draw.rect(self.screen, colour, [sprite.x-22, sprite.y-18, 44, 36], 3) 
                else:
                    pygame.draw.rect(self.screen, colour, [sprite.x-42, sprite.y-74, 84, 148], 3)

            if sprite.type == 'soldier':
                text = font.render(str(round(sprite.distance))+'cm', True, constants.white, colour)
                self.screen.blit(text, (sprite.x + 22, sprite.y -1))    
            else:
                text = font.render(str(round(sprite.distance))+'cm', True, constants.white, colour)
                self.screen.blit(text, (sprite.x + 42, sprite.y + 55))


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            #update display
            
            #fake detection for testing
            self.obstacle_found('soldier', 90, 40)
            self.obstacle_found('redcar', 0, 60)
            self.obstacle_found('redcar', 30, 20)

            self.background_sprites.draw(self.screen)
            self.obstacle_sprites.draw(self.screen)# obstacles added by GUI_Detectv2.py
            self.hud()# lines n distances n stuff
            self.foreground_sprites.draw(self.screen)# bus
            # wipe obstacles every loop
            

            self.background_sprites.update()
            
            self.obstacle_sprites.empty()

            pygame.display.update()
            self.fpsClock.tick(self.fps)

    def run_1_loop(self):
    
        self.background_sprites.draw(self.screen)
        self.obstacle_sprites.draw(self.screen)
        #self.hud()
        self.foreground_sprites.draw(self.screen)

        
        self.background_sprites.update() # moving background
        self.obstacle_sprites.empty()
        pygame.display.update()

if __name__ == '__main__':
    gui = GUI()
    gui.run()