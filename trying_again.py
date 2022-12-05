# V Preinfdevidfk0.1
# 
# # physicalTraits = [
#       brain_startingConnections: int,
#       sizeDeviation: float(0-1)?,# give/take up to 3
#       eggSize: int,
#       yolkEnergy: int,
#       so on...
# genes are entirely phisical?
# but so are brains, tho. okay.
# brains need to be passed genetically
# so genes are split in 2
# genes = (brainWiring, phisicalTraits)

import pygame
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

# Switches
pauseToggle = False
debugHUDtoggle = False
godMenuToggle = False
mainLoop = True

WIDTH = 480
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
# pygame.mixer.init()
debugFont = pygame.font.SysFont("monospace", 15)
simRuntime = 0
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AgentSim")
clock = pygame.time.Clock()

# Got this incredibly helpful function from https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame
def blit_text(surface, text, pos, font, color=pygame.Color("black")):
    words = [word.split(" ") for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(" ")[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.
        if y >= max_height + word_height / 2:# my edit started here
            print("Not all debug text could be displayed...")

# Classes
class Agent(pygame.sprite.Sprite):
    def __init__(self, genes, pos):
        pygame.sprite.Sprite.__init__(self)
        self.brain = genes[0]
        self.traits = genes[1]
        
        self.radius = 8
        self.image = pygame.Surface((self.radius*2, self.radius*2))
        
        pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        print("new Agent rect is :"+str(self.rect))
        self.rect.center = pos
        self.speedx = 0
        self.speedy = 0

    def layEgg(self):
        newEgg = Egg(self.genes, self.eggSizeFactor)
        all_sprites.add(newEgg)

    def die(self):
        pass


    def bounce(self, axis:str):
        if axis == "x":
            self.speedx *= -1
        elif axis == "y":
            self.speedy *= -1

class Egg(pygame.sprite.Sprite):
    def __init__(self, genes, size, pos, yolk):
        pygame.sprite.Sprite.__init__(self)
        self.brain = genes[0]
        self.traits = genes[1]
        self.radius = size
        # based on size, determines max posible yolk energy storage. volumetric rounded and reduced by an amount dictated by other factors.... I'm so tired.
        self.energy = yolk# I have none.

        self.image = pygame.Surface((self.radius*2, self.radius*2))
        pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        print("new Agent rect is :"+str(self.rect))
        self.rect.center = pos
        self.speedx = 0
        self.speedy = 0



class Food(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(self)
        self.radius = 1
        self.image = pygame.Surface((self.radius*2, self.radius*2))
        pygame.draw.circle(self.image, GREEN, self.rect.center, self.radius)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        print("new food pellet spawned")
        self.rect.center = pos
        self.speedx = 0
        self.speedy = 0

        self.energy = 1
        



# class Player(pygame.sprite.Sprite):
#     def update(self):
#         self.speedx = 0
#         keystate = pygame.key.get_pressed()
#         if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
#             self.speedx = -5
#         if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
#             self.speedx = 5
#         self.rect.x += self.speedx
#         if self.rect.right > WIDTH - 4:
#             self.rect.right = WIDTH - 4
#         if self.rect.left < 4:
#             self.rect.left = 4

# # load graphics
# background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
# background_rect = background.get_rect()
# player_img = pygame.image.load(path.join(img_dir, "fillerplayer.png")).convert()
# bullet_img = pygame.image.load(path.join(img_dir, "fillerbullet.png")).convert()
# mob_images = []
# mob_list = ['fillermob1.png', 'fillermob2.png']
# for img in mob_list:
#     mob_images.append(pygame.image.load(path.join(img_dir, img)).convert())

all_sprites = pygame.sprite.Group()
agents = pygame.sprite.Group()
foods = pygame.sprite.Group()
# for i in range(8):        # repeat 8 times
#     m = Mob()             # instantiate class
#     all_sprites.add(m)    # add instance to group

# Game loop
running = True
while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()# pressedKeysDict
    shiftKeys = [keys[pygame.K_LSHIFT], keys[pygame.K_RSHIFT]]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            print(mousePos)
            if any(shiftKeys):
                pass# spawn an Agent
            else:
                pass# spawn a food
        elif event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_w or event.key == pygame.K_UP:
            #     pass
            if event.key == pygame.K_SPACE:# toggle time paused
                if pauseToggle:
                    pauseToggle = False
                else:
                    pauseToggle = True
            elif event.key == pygame.K_F1:
                if debugHUDtoggle:
                    debugHUDtoggle = False
                else:
                    debugHUDtoggle = True




    # Update
    if not pauseToggle:
        all_sprites.update()
        simRuntime += 1

    # Render
    DebugText = f"Simulation Runtime: {simRuntime}\nLiving Agents: {len(all_sprites.sprites())}"
    screen.fill(BLACK)
    all_sprites.draw(screen)
    if debugHUDtoggle:
        blit_text(screen, DebugText, (20, 20), debugFont, color = pygame.Color("white"))
    pygame.display.flip()

pygame.quit()