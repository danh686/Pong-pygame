import pygame

FPS= 60
WIDTH, HEIGHT= 700, 500
WIN= pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pong")
pygame.font.init()

BALL_RADIUS= 8
PADDLE_WIDTH, PADDLE_HEIGHT= 15,115
BORDER_WIDTH, BORDER_HEIGHT= 10,18

WINNING_SCORE= 10
SCORE_FONT= pygame.font.SysFont('comicsans', 70)
WINNER_FONT= pygame.font.SysFont('comicsans', 70)

class Colour:
    WHITE= (255,255,255)
    BLACK= (0,0,0)
    GREY= (211,211,211)

class Ball:
    MAX_VEL= 5
    COLOUR= Colour.GREY
    def __init__(self, x, y, radius):
        self.x= x
        self.y= y
        self.radius= radius
        self.x_vel= self.MAX_VEL
        self.y_vel= 0
    def draw(self,win):
        pygame.draw.circle(win, self.COLOUR, (self.x, self.y), 7)
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
    def reset(self):
        self.x= WIDTH//2
        self.y= HEIGHT//2 
        self.x_vel *= -1
        self.y_vel= 0

class Paddle:    
    COLOUR= Colour.GREY
    VEL= 4
    def __init__(self, x, y, width, height):
        self.x= x
        self.y= y
        self.width= width
        self.height= height
        self.vel= self.VEL

    def draw(self, win):
        pygame.draw.rect(win, self.COLOUR, (self.x, self.y, self.width, self.height))
    
    def move(self, up):
        if up:
            self.y -= self.vel
        else:
            self.y += self.vel

def draw_window(win, ball, left_paddle, right_paddle, left_score, right_score):
    win.fill(Colour.BLACK)
    ball.draw(win)
    left_paddle.draw(win)
    right_paddle.draw(win)

    left_score_text= SCORE_FONT.render(f"{left_score}", 1, Colour.GREY)
    right_score_text= SCORE_FONT.render(f"{right_score}", 1, Colour.GREY)
    win.blit(left_score_text, (WIDTH//2 - left_score_text.get_width() - 30, 0))
    win.blit(right_score_text, (WIDTH//2 + 30, 0))

    for i in range(10, HEIGHT, 33):
        pygame.draw.rect(win, Colour.GREY, (WIDTH//2 - BORDER_WIDTH//2, i, BORDER_WIDTH, BORDER_HEIGHT))
    pygame.display.update()

def draw_winner(win, winner_text):
    text= WINNER_FONT.render(winner_text, 1, Colour.GREY)
    win.blit(text,(WIDTH//2 - (text.get_width()//2), HEIGHT//2 - (text.get_height())))
    pygame.display.update()

def handle_collision(ball, left_paddle, right_paddle):
    right_paddle_collision= (ball.x_vel > 0) and (ball.x + ball.radius >= right_paddle.x) and (ball.y >= right_paddle.y) and (ball.y <= right_paddle.y + right_paddle.height)
    left_paddle_collision= (ball.x_vel < 0) and (ball.x - ball.radius <= left_paddle.x + left_paddle.width) and (ball.y >= left_paddle.y) and (ball.y <= left_paddle.y + left_paddle.height)
    
    if ball.y - ball.radius <= 0 or ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    if right_paddle_collision:
        ball.x_vel *= -1  
        reduction= right_paddle.height/(2*Ball.MAX_VEL)
        paddle_centre= right_paddle.y + (right_paddle.height//2)
        ball.y_vel = (ball.y - paddle_centre)/reduction
    if left_paddle_collision:
        ball.x_vel *= -1
        reduction= left_paddle.height/(2*Ball.MAX_VEL)
        paddle_centre= left_paddle.y + (left_paddle.height//2)
        ball.y_vel = (ball.y - paddle_centre)/reduction

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.vel > 0:
        left_paddle.move(up= True)
    if keys[pygame.K_s] and (left_paddle.y + left_paddle.height + left_paddle.vel) < HEIGHT:
        left_paddle.move(up= False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.vel > 0:
        right_paddle.move(up= True)
    if keys[pygame.K_DOWN] and (right_paddle.y + right_paddle.height + right_paddle.vel) < HEIGHT:
        right_paddle.move(up= False)
        
def main():
    run= True 
    clock= pygame.time.Clock()
    ball= Ball(WIDTH//2, HEIGHT//2, 7)
    
    left_score= 0
    right_score= 0

    left_paddle= Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle= Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    
    while run:
        clock.tick(FPS)
        draw_window(WIN, ball, left_paddle, right_paddle, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run= False
                break
        
        keys_pressed= pygame.key.get_pressed()
        handle_paddle_movement(keys_pressed, left_paddle, right_paddle)
        
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)
        
        if ball.x < 0:
            right_score += 1
            ball.reset()
        if ball.x > WIDTH:
            left_score += 1
            ball.reset()
        
        won= False
        if left_score == WINNING_SCORE:
            draw_winner(WIN, "Left player won")
            won= True 
        if right_score == WINNING_SCORE:
            draw_winner(WIN, "Right player won")
            won= True 
        if won:
            pygame.time.delay(2000)
            main()
    pygame.quit()

if __name__  == "__main__":
    main()