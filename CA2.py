#Peace Samuel
#121376141

import sys, pygame
import math

#Game caption
pygame.display.set_caption("SPACE INVADERS? by PEACE SAMUEL") 

def collision_(x1, y1, x2, y2) -> bool:
        """Collision function:
        determines whether a collision has occurred
        Takes in: the x position and y position of two objects and detects collision
        Returns: Bool
        """
        distance = math.sqrt((math.pow(x1 - x2,2)) + (math.pow(y1 - y2,2)))
        if distance <= 5:
            return True
        else:
            return False

#GAME IMPLEMENTATION
class Space_Invader_Game:
    def __init__(self) -> None:
        pygame.init()

        #Screen details
        self._font = pygame.font.SysFont("game_font.ttf",25)
        self._size = self._width, self._height = 450, 300
        self._black = 0, 0, 0
        self._screen = pygame.display.set_mode(self._size)
        self._score_value = 0
        self._game_over = False
        
        #Rocket character details:
        #width of rocket image: 55, height: 50
        self._rocket = pygame.image.load("rocket.png")
        self._rocket_xpos = 225
        self._rocket_ypos = 250
        self._rocket_change = 0

        #Invader details:
        #width of invader image:25, height:19
        self._invader_image = pygame.image.load("alien.png")
        self._invader_list = []
        self._invader_X1 = []
        self._invader_Y1 = []
        self._invader_X2 = []
        self._invader_Y2 = []
        self._invader_X3 = []
        self._invader_Y3 = []
        self._invader_xpos1 = 3
        self._invader_xpos2 = 3
        self._invader_xpos3 = 3
        self._invader_cols = 8
        self._invader_xchange = 0.05
        self._invader_xchange2 = 0.05
        self._invader_xchange3 = 0.05
        self._invader_ychange = 20
        #Invader creation row 1:
        for col in range(self._invader_cols):
            self._invader_list.append(self._invader_image)
            self._invader_xpos1 += 40
            self._invader_Y1.append(3)
            self._invader_X1.append(self._invader_xpos1)
        #Invader creation row 2:
        for col in range(self._invader_cols):
            self._invader_xpos2 += 40
            self._invader_Y2.append(30)
            self._invader_X2.append(self._invader_xpos2)
        #Invader creation row 3:
        for col in range(self._invader_cols):
            self._invader_xpos3 += 40
            self._invader_Y3.append(57)
            self._invader_X3.append(self._invader_xpos3)

        #Bullet details:
        #width of bullet image: 5, height: 10
        self._bullet = pygame.image.load("bullet.png")
        self._bullet_xpos = 0
        self._bullet_ypos = 0
        self._bullet_state = False
        self._bullet_change = 0

    def rungame(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                #rocket movement, using arrow keys
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self._rocket_change = -0.5
                    if event.key == pygame.K_RIGHT:
                        self._rocket_change = 0.5
                    #bullet movement, in y axis, hold space bar to shoot, shoots one bullet at a time
                    #bullet spawns from the rockets position
                    if event.key == pygame.K_SPACE:
                       self._bullet_state = True
                       self._bullet_ypos = self._rocket_ypos
                       self._bullet_xpos = self._rocket_xpos + 25
                       self._bullet_change = -1
                if event.type == pygame.KEYUP:
                    self._rocket_change = 0
                    self._bullet_state = False
            #adding change in rocket position (movement)
            #also keep the rocket within the bounds of the screen
            if self._rocket_xpos + self._rocket_change > 0 and self._rocket_xpos + self._rocket_change < self._width -55:
                self._rocket_xpos += self._rocket_change
            #adding change in bullet position (movement)
            self._bullet_ypos += self._bullet_change
            #Movement in invaders
            #increment the x position of the invaders to create movement
            for i in range(len(self._invader_X1)):
                self._invader_X1[i] += self._invader_xchange
                self._invader_X2[i] += self._invader_xchange
                self._invader_X3[i] += self._invader_xchange
                # if the furthest invader hits either edge of the screen (width or zero), then move in the opposite direction, and move down ie. increase y position by invader height
                if self._invader_X1[i] > (self._width - 25) or self._invader_X1[i] <= 0:
                    self._invader_xchange *= -1
                    self._invader_xchange2 *= -1
                    self._invader_xchange3 *= -1
                    self._invader_Y1 = [ item + self._invader_ychange for item in (self._invader_Y1)]
                    self._invader_Y2 = [ item + self._invader_ychange for item in (self._invader_Y2)]
                    self._invader_Y3 = [ item + self._invader_ychange for item in (self._invader_Y3)]
                #collision with rocket is GAME OVER
                #if the difference between the rockets x position and the invaders x position, and the the invader y position is greater than or equal to the rockets y position, a collision has occurred
                if  (abs(self._rocket_xpos - self._invader_X1[i]) < 50 and (self._invader_Y1[i] >= self._rocket_ypos)) or (abs(self._rocket_xpos - self._invader_X2[i]) < 50 and (self._invader_Y2[i] >= self._rocket_ypos)) or (abs(self._rocket_xpos - self._invader_X3[i]) < 50 and (self._invader_Y2[i] >= self._rocket_ypos)) :
                    self._game_over = True
                #checks for a collision between the bullet and the invader for invaders in each row
                collision1 = collision_(self._invader_X1[i], self._invader_Y1[i], self._bullet_xpos, self._bullet_ypos)
                collision2 = collision_(self._invader_X2[i], self._invader_Y2[i], self._bullet_xpos, self._bullet_ypos)
                collision3 = collision_(self._invader_X3[i], self._invader_Y3[i], self._bullet_xpos, self._bullet_ypos)
                #If a collision is detected between the bullet and the invader then the score should increase
                #increase score by 5 for each invader shot
                #remove the invader and the bullet, on collision
                if collision1:
                    self._score_value += 5
                    self._bullet_state = False
                ###doesn't work index out of range??, can't remove invaders from screen upon collision###
                    # del self._invader_X1[i]
                    # del self._invader_Y1[i]
                if collision2:
                    self._score_value += 5
                    self._bullet_state = False
                ###same problem###
                    # del self._invader_X2[i]
                    # del self._invader_Y2[i]
                if collision3:
                    self._score_value += 5
                    self._bullet_state = False
                ###same problem###
                    # self._invader_X3.remove(self._invader_X3[i])
                    # self._invader_Y3.remove(self._invader_Y3[i])
                    # del self._invader_X3[i]
                    # del self._invader_Y3[i]


            #draw screen
            #draw rocket, bullet, invaders and score on screen
            self._screen.fill(self._black)
            self._screen.blit(self._rocket, (self._rocket_xpos, self._rocket_ypos))
            self._score = self._font.render("Score:" + str(self._score_value), True, (255, 255, 255), None)
            self._screen.blit(self._score, (350, 10))
            for i in range(len(self._invader_X1)):
                self._screen.blit(self._invader_list[i],(self._invader_X1[i], self._invader_Y1[i]))
                self._screen.blit(self._invader_list[i],(self._invader_X2[i], self._invader_Y2[i]))
                self._screen.blit(self._invader_list[i],(self._invader_X3[i], self._invader_Y3[i]))
            if self._bullet_state is True:
                self._screen.blit(self._bullet, (self._bullet_xpos, self._bullet_ypos))
            #draw game over screen
            if self._game_over:
                self._game_state = self._font.render("GAME OVER :(", True, (255, 255, 255), None)
                self._screen.fill(self._black)
                self._screen.blit(self._game_state, (150, 150))
                #sys.exit()
                    
                
            pygame.display.flip()


if __name__ == "__main__":
    game = Space_Invader_Game()
    game.rungame()
