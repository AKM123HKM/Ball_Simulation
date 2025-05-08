import pygame, sys, math, time
from random import randint

pygame.init()

class Ball(pygame.sprite.Sprite):
    def __init__(self,x,y,radius,damping):
        super().__init__()
        self.image = pygame.image.load("ball.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image,0,radius/100)
        self.rect = self.image.get_rect(center = (x,y))

        self.vel = pygame.math.Vector2(5,0)
        self.pos = pygame.math.Vector2(self.rect.x,self.rect.y)
        self.damping = damping
        self.y_state = "move"
        self.x_state = "move"

    def move_ball(self,pos):
        self.y_state = "rest"
        self.vel.update(0,0)
        self.pos.update(pos)
        self.rect.center = self.pos

    def update(self,gravity,friction,surfaces,ground,dt):
        if self.y_state == "move":
            self.vel.y += gravity * dt
            self.pos.y += self.vel.y * dt
            self.rect.center = self.pos

            if check_collision(self, ground):
                self.pos.y = ground_surf.rect.top - self.rect.height / 2
                self.rect.centery = self.pos.y

                # Apply damping
                self.vel.y = -self.vel.y * self.damping

                # Threshold check AFTER damping
                threshold_vel = math.sqrt(2 * gravity * dt)
                if abs(self.vel.y) < threshold_vel:
                    self.vel.y = 0
                    self.y_state = "rest"

        if self.x_state == "move":
            # Update the position
            self.pos.x += self.vel.x
            self.rect.center = self.pos

            # Apply friction on ground and stop ball is velocity if it is too low
            if check_collision(self, ground):
                if self.vel.x != 0:
                    friction_effect = friction * dt
                    if abs(self.vel.x) <= friction_effect:
                        self.vel.x = 0
                        self.x_state = "rest"
                    else:
                        self.vel.x -= friction_effect * (1 if self.vel.x > 0 else -1)

            # Check if ball collides with walls and reverts the velocity
            if check_collision(self,surfaces):
                self.vel.x = -self.vel.x

        # Checks if ball is above the ground
        if not check_collision(self,ground): self.y_state = "move"

class Surface(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        super().__init__()
        self.image = pygame.image.load("surface.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(width,height))
        self.rect = self.image.get_rect(topleft = (x,y))

# Constants
WIDTH, HEIGHT = 800, 400
GRAVITY = 600
FRICTION = 10

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Ball simulation")
clock = pygame.time.Clock()

Balls = pygame.sprite.Group()
Surfaces = pygame.sprite.Group()
Ground = pygame.sprite.GroupSingle()

ground_surf = Surface(0,HEIGHT-10,WIDTH,10)
right_wall = Surface(0,0,10,HEIGHT)
left_wall = Surface(WIDTH-10,0,10,HEIGHT)
Ground.add(ground_surf)
Surfaces.add(right_wall)
Surfaces.add(left_wall)

previous_time = time.time()

selected_ball = None

# Functions

# Small groups seems logical to loop and check collision to 
# reduce number of loops but IDK
def check_collision(sprite,Group):
    if pygame.sprite.spritecollideany(sprite,Group):
        return True

    return False

def mouse_collision(sprite,pos):
    if sprite.rect.collidepoint(pos): return True

    return False

def select_ball(selected_ball):
    mouse_keys = pygame.mouse.get_pressed()

    # Selects a ball if no ball is selected
    if mouse_keys[2] and not selected_ball:
        mouse_pos = pygame.mouse.get_pos()
        for ball in Balls.sprites():
            if mouse_collision(ball,mouse_pos):
                selected_ball = ball
                break

    # De-select a ball if right click is not pressed
    if selected_ball and not mouse_keys[2]:
        selected_ball = None

    return selected_ball

while True:
    dt = time.time() - previous_time
    previous_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x,y = pygame.mouse.get_pos()
                radius = randint(5,15)
                damping = randint(1,9)/10
                Balls.add(Ball(x,y,radius,0.9))

    selected_ball = select_ball(selected_ball) 
    if selected_ball: selected_ball.move_ball(pygame.mouse.get_pos())

    screen.fill((100,100,100))
    Balls.draw(screen)
    Balls.update(GRAVITY,FRICTION,Surfaces,Ground,dt)
    Ground.draw(screen)
    Surfaces.draw(screen)

    # for ball in Balls.sprites():
    #     pygame.draw.rect(screen,"red",ball.rect,2)
    #     pygame.draw.line(screen,"blue",ball.rect.center,(ball.rect.centerx,ball.rect.centery+ball.rect.height/2),2)

    pygame.display.update()
    clock.tick(60)