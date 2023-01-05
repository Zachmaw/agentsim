import pygame

WINSIZE = WIDTH, HEIGHT = (640, 480)
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize Pygame and set up the display
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Initialize the mixer and load a sound file
# pygame.mixer.init()
# collision_sound = pygame.mixer.Sound('ball.ogg')
clock = pygame.time.Clock()
# Set up the first ball's initial position and velocity
x1 = 320
y1 = 240
vx1 = 1
vy1 = 1

# Set up the second ball's initial position and velocity
x2 = 100
y2 = 100
vx2 = 2
vy2 = 2




class Particle():
    def __init__(self, pos) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.radius = 3
        self.velocity = 0
        self.image_orig = pygame.Surface((self.radius*2, self.radius*2))
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        pygame.draw.circle(screen, (255, 255, 255), (x1, y1), self.radius)
        pygame.draw.circle(screen, (255, 255, 0), (x2, y2), self.radius)
        self.rect.center = pos
        print("new Agent rect is :"+str(self.rect)+" and "+str(self.rect.center))
        self.velx = 0
        self.vely = 0
        self.rot_angle = 0# of 359
        self.rot_vel = 0

    def update(self):
        self.rect.x += self.velx# x position
        self.rect.y += self.vely# y position
        old_center = self.rect.center# fix sprite angle
        self.image = pygame.transform.rotate(self.image_orig, self.rot_angle)# make a new copy of the original image rotated by current angle and set as self.image
        self.rect = self.image.get_rect()# fix the Rect
        self.rect.center = old_center# keep it in place




# Run the game loop
running = True
while running:
# Handle user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                vx1 -= 2
            elif event.key == pygame.K_RIGHT:
                vx1 += 2
            elif event.key == pygame.K_UP:
                vy1 -= 2
            elif event.key == pygame.K_DOWN:
                vy1 += 2
            # elif event.type == pygame.KEYUP:
            #     vx1 = 0
            #     vy1 = 0

    # Update the balls' positions
    x1 += vx1
    y1 += vy1
    x2 += vx2
    y2 += vy2

    # Check if the balls are out of bounds and reverse their velocities if necessary
    if x1 - self.radius <= 0 or x1 + self.radius >= WIDTH:
        vx1 = -vx1# reverse X velocity of first ball
    if y1 - self.radius <= 0 or y1 + self.radius >= HEIGHT:
        vy1 = -vy1# reverse y velocity of first ball
    if x2 - self.radius <= 0 or x2 + self.radius >= WIDTH:
        vx2 = -vx2# reverse X velocity of second ball
    if y2 - self.radius <= 0 or y2 + self.radius >= HEIGHT:
        vy2 = -vy2# reverse y velocity of second ball

    # Check if the balls collide and reverse their velocities if necessary
    dx = x1 - x2
    dy = y1 - y2
    distance = (dx ** 2 + dy ** 2) ** 0.5
    if distance <= 2 * self.radius:
        vx1, vx2 = vx2, vx1
        vy1, vy2 = vy2, vy1
        # collision_sound.play()# Play the collision sound

    # Draw the balls and update the display
    screen.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(FPS)