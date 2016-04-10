import pygame, sys
from pygame.locals import *
from agar_game import *
from pygame import gfxdraw
if not pygame.font: print('Warning, fonts disabled')

#set up window
pygame.init()
height = pygame.display.Info().current_h
width = pygame.display.Info().current_w
DISPLAYSURF = pygame.display.set_mode((width, height),(pygame.FULLSCREEN|pygame.HWSURFACE))

pygame.display.set_caption('Agar by Sanil')
fpsClock=pygame.time.Clock()
game_fps = 60

#colours
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
col = [BLUE, GREEN, RED]#list of colours for bubbles

WHITE = (255, 255, 255)#mouse
BLACK = (  0,   0,   0)#background
PINK  = (255, 0, 255)#powerups

#drawing functions
def draw_bubble(bubble):
     bubble_col = col[divmod(bubble.size,3)[1]]#bubble colour dependent on size
     gfxdraw.aacircle(DISPLAYSURF,int(bubble.position_x), int(bubble.position_y),int(bubble.size),bubble_col)
     gfxdraw.filled_circle(DISPLAYSURF,int(bubble.position_x), int(bubble.position_y),int(bubble.size),bubble_col)

def draw_mouse(mouse):
     gfxdraw.aacircle(DISPLAYSURF,int(mouse.pos_x), int(mouse.pos_y),int(mouse.size),WHITE)
     gfxdraw.filled_circle(DISPLAYSURF,int(mouse.pos_x), int(mouse.pos_y),int(mouse.size),WHITE)

def draw_powerup(powerup):
     gfxdraw.aacircle(DISPLAYSURF,int(powerup.pos_x), int(powerup.pos_y),int(powerup.size),PINK)
     gfxdraw.filled_circle(DISPLAYSURF,int(powerup.pos_x), int(powerup.pos_y),int(powerup.size),PINK)
     font = pygame.font.SysFont("comicsansms", 12)
     text = font.render(powerup.feature, True, WHITE)
     DISPLAYSURF.blit(text,(powerup.pos_x - 20, powerup.pos_y - 10))
     

def play():
     global mousex, mousey#code doesn't work without this for some reason!!!
     #initialise game  
     g = game(game_x = width, game_y = height, fps =game_fps)
     level = 0 # used to cache level values so dont have to keep on drawing
     score = -1 # used to cache score so dont have to keep on drawing
     while True: # main game loop - play till dead 
          #Input code from mouse/keyboard     
          for event in pygame.event.get():
               if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
               elif event.type == MOUSEMOTION:
                    mousex, mousey = event.pos
               elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:#restart mid game
                    return play()
              
          DISPLAYSURF.fill(BLACK)#clear last screen
          
          #check if alive and if not finish game and save highscore
          if not g.mo.state:
               with open('highscores.txt', 'a') as file:
                    file.write(str(round(g.mo.score,1)))
                    file.write('\n')
               scores = []
               with open('highscores.txt', 'r') as file:
                    for line in file:
                         scores.append(line[:-1])
               scores = [float(x) for x in scores]
               high_score = max(scores)
               
               #play again code
               font = pygame.font.SysFont("comicsansms", 72)
               text1 = font.render("Game Over! Current score: " + str(round(g.mo.score,1)), True, WHITE)
               text2 = font.render('Highscore: ' + str(high_score), True, WHITE)
               text3 = font.render('Play Again?', True, WHITE)
               text4 = font.render('Press Space or Enter to play again', True, WHITE)
               DISPLAYSURF.blit(text1,(width/2 - text1.get_rect().width/2, height/2 - text1.get_rect().height/2 - text2.get_rect().height))
               DISPLAYSURF.blit(text2,(width/2 - text2.get_rect().width/2, height/2 - text2.get_rect().height/2))
               DISPLAYSURF.blit(text3,(width/2 - text3.get_rect().width/2, height/2 + text3.get_rect().height/2))
               DISPLAYSURF.blit(text4,(width/2 - text4.get_rect().width/2, height/2 + text4.get_rect().height/2 +  text3.get_rect().height))
               pygame.display.flip()
               while True:
                    for event in pygame.event.get():
                         if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                              return play()
                         elif event.type == pygame.KEYDOWN and event.key != pygame.K_RETURN:#return restarts the game
                              pygame.quit()
                              sys.exit()
     
          #draw current screen
          for x in g.bubbles:
               draw_bubble(x)
          for x in g.powerups:
               draw_powerup(x)
          draw_mouse(g.mo)
          
          #simulate next step with mouse data
          g.time_step(mousex,mousey)
          
          #Display text for score + level
          font = pygame.font.SysFont("comicsansms", 28)
          if score != g.mo.score:
               score = g.mo.score
               textScore = font.render("Score: " + str(round(g.mo.score,1)), True, WHITE)
          DISPLAYSURF.blit(textScore,(width - 360, 100))
          if level != g.level:
               level = g.level
               textLevel = font.render("Level: " + str(g.level), True, WHITE)
          DISPLAYSURF.blit(textLevel,(width - 720, 100))
          
          #display current screen  
          pygame.display.flip()
          fpsClock.tick(game_fps)# game runs at 80 fps

play()
