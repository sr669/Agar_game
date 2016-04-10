from random import randint,choice

class bubble:

    def __init__(self,maxsize = 10, minsize = 1, game_x = 1920, game_y = 1080):
        maxspeed = 2
        self.game_x = game_x 
        self.game_y = game_y 
        self.size = randint(minsize,maxsize)
        self.speed_x = choice([0.5*x for x in range(-2*maxspeed,2*maxspeed + 1)])
        self.speed_y = choice([0.5*x for x in range(-2*maxspeed,2*maxspeed + 1)])
        if randint(1,2)==1:#initialise bubbles on edges
            self.position_x = choice([0,self.game_x])
            self.position_y = randint(0,self.game_y)
        else:
            self.position_x = randint(0,self.game_x)
            self.position_y = choice([0,self.game_y])
        
    def move(self):
        self.position_x = self.position_x + self.speed_x
        self.position_y = self.position_y + self.speed_y

    def hit(self,mouse):
        if abs(self.position_x - mouse.pos_x) <= self.size + mouse.size and abs(self.position_y - mouse.pos_y) <= self.size + mouse.size:
            return True
        else:
            return False

    def exists(self):#returns true if bubble is in game window
        if self.position_x < 0 or self.position_x > self.game_x:
            return False
        elif self.position_y < 0 or self.position_y > self.game_y:
            return False
        else:
            return True

    def eat(self,game):#either eaten or finishes game
        if self.hit(game.mo) and self.size < game.mo.size:
            game.mo.size = game.mo.size + (self.size/3)**game.growthRate
            game.mo.score = game.mo.score + (self.size/3)**game.growthRate
            self.position_x = self.game_x + 10 #removes eaten bubble from game
        elif self.hit(game.mo) and self.size >= game.mo.size:
            game.mo.state = False
	
class mouse:
    
    def __init__(self, game_x = 1920, game_y = 1080):
        self.game_x = game_x 
        self.game_y = game_y 
        self.size = 2 # initial mouse size (>= 2)
        self.pos_x = game_x/2
        self.pos_y = game_y/2
        self.state = True # alive or not
        self.score = 0

    def exists(self, game):#levels up mous and kills mouse if it gets bigger than the game
        if self.size > 150 and game.level == 1:#upper limit on size going to lvl 2
            self.size = 4
            game.level = 2
        elif self.size > 150 and game.level == 2:#upper limit on size going to lvl 3
            self.size = 8
            game.level = 3
        elif self.size > 150 and game.level > 2:#upper limit on size going to lvl 4
            self.size = 12 + 2*(game.level - 3)
            game.bubbleDensity = game.bubbleDensity + 5
            game.powerup_creation_rate = game.powerup_creation_rate + 5
            game.upperBubbleSizeLimit = game.upperBubbleSizeLimit + 1
            game.level = game.level + 1
        if self.size + self.pos_x > self.game_x or self.size + self.pos_y > self.game_y or min(self.pos_x - self.size, self.pos_y - self.size) < 0:
            print('mouse has left the game')
            self.state = False
            
    def move(self,x,y):#in future get x and y from computer mouse position
        self.pos_x = x
        self.pos_y = y

class game:

    def __init__(self,game_x = 1920, game_y = 1080, fps = 80):
        self.game_x = game_x 
        self.game_y = game_y
        self.fps = fps
        self.powerup_creation_rate = 10# powerup created every 10 seconds on average
        self.bubbleDensity = 220 # max bubbles on screen
        self.bubbleGenerationRate = 10 #max bubbles created per timestep
        self.lowerBubbleSizeLimit = 3 #new bubbles generated are up to x less than mouse size
        self.upperBubbleSizeLimit = 12 #new bubbles generated are up to x more than mouse size
        self.growthRate = 0.3
        self.level = 1
        #initalise mouse, bubbles and powerups
        self.mo = mouse(game_x = self.game_x, game_y = self.game_y)
        self.mo.size = 2 #change starting mouse size
        self.bubbles =  self.new_bubbles(20)
        self.powerups = self.new_powerups(2)#start game with 2 powerups
            
    def new_bubbles(self,no):
        new_bub = [bubble(maxsize = round(self.mo.size + self.upperBubbleSizeLimit), minsize = max(1,round(self.mo.size - self.lowerBubbleSizeLimit)), game_x = self.game_x, game_y = self.game_y) for z in range (0,no)]# ensure that new bubbles capable of killing are generated
        return new_bub

    def new_powerups(self,no):
        new_powerup = [powerup(game_x = self.game_x, game_y = self.game_y, fps = self.fps) for z in range (0,no)]
        return new_powerup
    
    def time_step(self,mousex,mousey):
        #mouse code
        prevSize = self.mo.size
        self.mo.exists(self)#checks if mouse has left the game
        newSize = self.mo.size
        if prevSize != newSize:#bubble has reached upper limit and shrunk
            self.bubbles = []
        self.mo.move(mousex,mousey)#the mouse moves

        #bubble code
        self.bubbles = [x for x in self.bubbles if x.exists()]#removes bubbles out of view
        if len(self.bubbles) <= self.bubbleDensity:#put upper limit on bubbles on screen
            new_bubs = self.new_bubbles(self.bubbleGenerationRate)#new bubbles generated at edges
            self.bubbles = self.bubbles + new_bubs
        for bub in self.bubbles:# move bubbles and eat bubbles
            bub.move()
            bub.eat(self)

        #powerup code
        self.powerups = [x for x in self.powerups if x.exists()]
        a = randint(1,self.powerup_creation_rate * self.fps)#1 powerup created every f frames
        if a == 2:
            self.powerups = self.powerups + self.new_powerups(1)
        for power in self.powerups:
            power.eat(self)
            power.frames_alive = power.frames_alive - 1
            power.size = max(3, 15 * ((power.frames_alive) / (self.fps * power.time_alive)))
            

class powerup:
    
    def __init__(self,game_x = 1920, game_y = 1080, fps = 80):
        self.game_x = game_x 
        self.game_y = game_y
        self.size = 15
        self.pos_x = randint(200, self.game_x - 200)
        self.pos_y = randint(200, self.game_y - 200)
        self.feature = choice(['SlowDown', 'SpeedUp', 'SizeUp', 'SizeDown', 'ScoreBonus','PauseTime','LessBubbles','MoreBubbles','SmallBubbles', 'BigBubbles','GrowFast','GrowSlow','MorePowerups','Reverse'])
        self.time_alive = randint(10,30)
        self.frames_alive = fps * self.time_alive
		
    def hit(self,mouse):
        if abs(self.pos_x - mouse.pos_x) <= self.size + mouse.size and abs(self.pos_y - mouse.pos_y) <= self.size + mouse.size:
                return True
        else:
                return False

    def eat(self, game):
        if self.hit(game.mo):
            if self.feature == 'SlowDown':
                for x in game.bubbles:
                    x.speed_x = x.speed_x * 0.25
                    x.speed_y = x.speed_y * 0.25                
            elif self.feature == 'SpeedUp':
                for x in game.bubbles:
                    x.speed_x = x.speed_x * 1.5
                    x.speed_y = x.speed_y * 1.5
            elif self.feature == 'PauseTime':
                for x in game.bubbles:
                    x.speed_x = 0
                    x.speed_y = 0
            elif self.feature == 'SizeUp':
                game.mo.size = game.mo.size + 5
            elif self.feature == 'SizeDown':
                game.mo.size = max(2, game.mo.size - 3)
            elif self.feature == 'ScoreBonus':
                game.mo.score = game.mo.score + 20
            elif self.feature == 'LessBubbles':
                game.bubbleDensity = max(10, game.bubbleDensity - 25)
            elif self.feature == 'MoreBubbles':
                game.bubbleDensity = game.bubbleDensity + 25
            elif self.feature == 'SmallBubbles':
                game.lowerBubbleSizeLimit = game.lowerBubbleSizeLimit + 2
                game.upperBubbleSizeLimit = game.upperBubbleSizeLimit - 2
            elif self.feature == 'BigBubbles':
                game.lowerBubbleSizeLimit = game.lowerBubbleSizeLimit - 1
                game.upperBubbleSizeLimit = game.upperBubbleSizeLimit + 1
            elif self.feature == 'GrowFast':
                game.growthRate = game.growthRate + 0.5
            elif self.feature == 'GrowSlow':
                game.growthRate = max(0.05, game.growthRate - 0.2)
            elif self.feature == 'MorePowerups':
                game.powerup_creation_rate = game.powerup_creation_rate - 2
            elif self.feature == 'Reverse':
                for x in game.bubbles:
                    x.speed_x = -x.speed_x
                    x.speed_y = -x.speed_y
            #move eaten powerup out of game window
            self.pos_x = self.pos_x + self.game_x

    def exists(self):#returns true if powerup is in game window
        if self.pos_x < 0 or self.pos_x > self.game_x:
            return False
        elif self.pos_y < 0 or self.pos_y > self.game_y:
            return False
        elif self.frames_alive <= 0:
            return False
        else:
            return True
        
