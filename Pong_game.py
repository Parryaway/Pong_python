import pygame
pygame.init()



#This game was coded by Yoi    :)     Cheers and have Fun!!


width, height = 1000, 700 #size of the window
WIN = pygame.display.set_mode((width, height)) 
pygame.display.set_caption("Pong")
FPS= 60 #setting up similar to a sec to make it comfortable

#Font for score board
score_font = pygame.font.SysFont("Timesnewroman", 40)

#Size of ball
ball_radius = 7

#Size of Guard
Guard_width, Guard_height = 30, 100

#Winning Score
win_score= 5

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)



class Guard: #class for the two guard units
    COLOR= RED
    VEL = 9
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):      # to bring into original position
        self.x = self.original_x
        self.y = self.original_y
        

class Ball:
    max= 20
    color= WHITE
    def __init__(self, x, y, radius):
        self.x= self.original_x = x
        self.y= self.original_y = y
        self.radius = radius
        self.x_vel = self.max
        self.y_vel = 0
    
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
    
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
    
    def reset(self): #bringing into original position
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1



def draw(win, guards, ball, left_score, right_score):
    win.fill(BLACK)
    
    left_score_txt = score_font.render(f"{left_score}", 1, WHITE)
    right_score_txt = score_font.render(f"{right_score}", 1, WHITE)

    win.blit(left_score_txt,(width//4 -left_score_txt.get_width()//2,20))
    win.blit(right_score_txt,(width * (3/4)-right_score_txt.get_width()//2,20))

    for guard in guards:
        guard.draw(win)
    
    for i in range(10, height, height//20): #for the middle line
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE,(width//2 - 5, i, 10, height//20)) #Creating a dash line (where, what color, (x-axis, y-axis))
    
    ball.draw(win)

    pygame.display.update() #continuous updating required since its display

def handle_collision (ball, left_guard, right_guard): #U dont wanna know where this comes from
    if ball.y + ball.radius >= height: 
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    
    if ball.x_vel < 0: #Headache help
        if ball.y >= left_guard.y and ball.y <= left_guard.y + left_guard.height:
            if ball.x -ball.radius <= left_guard.x +left_guard.width:
                ball.x_vel *= -1

                middle_y = left_guard.y + left_guard.height/2 #ball moving y-axis
                difference = middle_y - ball.y
                reduction = (left_guard.height/2)/ ball.max
                y_vel= difference/reduction
                ball.y_vel = -1 * y_vel
                

    else:
        if ball.y >= right_guard.y and ball.y <= right_guard.y + right_guard.height:# the other part
            if ball.x + ball.radius >= right_guard.x:
                ball.x_vel *= -1

                middle_y = right_guard.y + right_guard.height/2
                difference = middle_y- ball.y
                reduction = (right_guard.height/2)/ ball.max
                y_vel=difference/reduction
                ball.y_vel = -1 *y_vel


def handle_guard_movement(keys, left_guard, right_guard): #movement of guards
    if keys[pygame.K_w] and left_guard.y - left_guard.VEL >= 0:
        left_guard.move(up=True)
    if keys[pygame.K_s] and left_guard.y + left_guard.VEL + left_guard.height <= height: #interesting Formula
        left_guard.move(up=False)
    
    if keys[pygame.K_UP] and right_guard.y - right_guard.VEL >= 0:
        right_guard.move(up=True)
    if keys[pygame.K_DOWN] and right_guard.y + right_guard.VEL + right_guard.height <= height: 
        right_guard.move(up=False)

def main():
    run=True
    clock= pygame.time.Clock() 

    left_guard = Guard(10, height//2- Guard_height//2, Guard_width, Guard_height) #placement of the left guard. (0,0) = top left corner
    right_guard = Guard(width -10 - Guard_width, height//2- Guard_height//2, Guard_width, Guard_height)

    ball = Ball (width//2, height//2, ball_radius)
    
    left_score = 0
    right_score = 0

    while run: #the game is to be run as a continuous loop
        clock.tick(FPS) #Putting a limit on to the game
        draw(WIN, [left_guard,right_guard], ball, left_score, right_score)

        for event in pygame.event.get ():
            if event .type ==pygame.QUIT:
                run = False 
                break
        

        keys= pygame.key.get_pressed() #implementing key pressed on keyboard
        handle_guard_movement(keys, left_guard, right_guard)

        ball.move()
        handle_collision(ball, left_guard, right_guard)

        if ball.x < 0:
            right_score += 1
            ball.reset()
            right_guard.reset()
            left_guard.reset()
        elif ball.x >width:
            left_score += 1
            ball.reset()
            left_guard.reset()
            right_guard.reset()
        
        win= False

      

        if left_score >= win_score:
            win= True
            win_txt = "Left player Wins!!!"
        elif right_score >= win_score:
            win= True
            win_txt = "Right player Wins!!!"
        
        if win:
            text = score_font.render(win_txt,1,WHITE)
            WIN.blit(text, (width//2 -text.get_width()//2,height//2-text.get_height()//2)) #middle calculation
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_guard.reset()
            right_guard.reset()

    pygame.quit()

if __name__ == "__main__":
    main()
