# V Preinfdev0.3
# 
# # physicalTraits = [
#       brainWiring: list of neuralConnections
#       brain_startingConnections: int,
#       eggSize: int,
#       eggshellThickness: int
#       yolkEnergy: int,
#       size: int
#       so on...
# 
# lifeStages = ["egg", "hatchling", "mature", "elder"]

import pygame
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

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

def buildBackdrop(size:"pygame.surface._Coordinate"):
    def flipColor(colorState, colorA:"tuple[int,int,int]", colorB:"tuple[int,int,int]"):
        if not colorState or colorState == colorA:
            colorState = colorB
        else: 
            colorState = colorA
        return colorState
    c = None
    backdrop = pygame.surface.Surface(size)
    backdrop.fill(BLACK)
    for y in range(0,HEIGHT,cellSize): 
        c = flipColor(c, RED, BLACK)
        for x in range(0,WIDTH,cellSize):
            c = flipColor(c, RED, BLACK)
            pygame.draw.rect(backdrop, c, pygame.Rect(x, y, x+cellSize, y+cellSize))
    return backdrop

# Switches
pauseToggle = False
debugHUDtoggle = False
mainLoop = True

# counters
simRuntime = 0
simEnergy = 0

cellSize = 32
gridWidth = 10
gridHeight = 10
WIDTH = cellSize * gridWidth
HEIGHT = cellSize * gridHeight
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
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AgentSim")
clock = pygame.time.Clock()
background = buildBackdrop(screen.get_rect().size)
all_sprites = pygame.sprite.Group()
agents = pygame.sprite.Group()
foods = pygame.sprite.Group()

# Classes
class Agent(pygame.sprite.Sprite):
    def __init__(self, genes, pos):
        pygame.sprite.Sprite.__init__(self)
        self.brain = genes[0] 
        self.traits = genes[1]
        self.lifeStage = 0
        self.energy = 0
        
        self.radius = self.traits[4]*3
        self.image_orig = pygame.Surface((self.radius*2, self.radius*2))
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.center = pos
        print("new Agent rect is :"+str(self.rect)+" and "+str(self.rect.center))
        self.speedx = 0
        self.speedy = 0
        self.rot_angle = 0# of 359
        self.rot_vel = 0

    def update(self):
        self.rect.x += self.speedx# x position
        self.rect.y += self.speedy# y position
        old_center = self.rect.center# fix sprite angle
        self.image = pygame.transform.rotate(self.image_orig, self.rot_angle)# make a new copy of the original image rotated by current angle and set as self.image
        self.rect = self.image.get_rect()# fix the Rect
        self.rect.center = old_center# keep it in place

    def useEnergy(self) -> bool:
        if self.energy >= 1:
            self.energy -= 1
            return True
        else:# Energy is Zero, nothing removed
            return False

    def rotate(self, rot_force:"float"):# a float between -1 and 1
        tr = 0
        numberCrunching = abs(rot_force) % 1
        if numberCrunching < 0.695 and numberCrunching > 0.358:
            tr += 1
        
        for i in range(int(rot_force)/36):##### Stop this madness, brother...







            #####








            pass
        def calcolo():
            n = rot_force % 1
            output = self.rot_angle + n % 360
            return output



        self.rot_angle = calcolo()





    def layEgg(self):# determine size from self.traits
        egg = Agent(self.genes, self.eggSizeFactor, self.rect.center, )
        all_sprites.add(egg)
        agents.add(egg)


    def accelerate(self):
        pass
    
# class Egg(pygame.sprite.Sprite):
#     def __init__(self, genes, size, pos, yolk):
#         pygame.sprite.Sprite.__init__(self)
#         self.brain = genes[0]
#         self.traits = genes[1:]
#         self.radius = size
#         # based on size, determines max posible yolk energy storage. volumetric rounded and reduced by an amount dictated by other factors.... I'm so tired.
#         self.yolk = yolk# I have none.
#         self.hullStrength = self.traits[2] * 12

#         self.image = pygame.Surface((self.radius*2, self.radius*2))
#         self.rect = self.image.get_rect()
#         pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)
#         self.image.set_colorkey(BLACK)
#         print("new Agent rect is :"+str(self.rect))
#         self.rect.center = pos
#         self.speedx = 0
#         self.speedy = 0

#     def update(self):
#         self.rect.x += self.speedx
#         self.rect.y += self.speedy
    
#     def mature(self):
#         pass

#     def hatch(self):
#         pass

class Food(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 1
        self.image = pygame.Surface((self.radius*2, self.radius*2))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, GREEN, self.rect.center, self.radius)
        print("new food pellet spawned at "+str(pos))
        self.rect.center = pos
        self.speedx = 0
        self.speedy = 0

        self.energy = 1

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

# class Player(pygame.sprite.Sprite):
#     def update(self):
#         self.speedx = 0
#             self.speedx = -5
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
            if any(shiftKeys):### spawn an Agent
                pass
            else:# spawn a food
                tempFoodVar = Food(mousePos)
                all_sprites.add(tempFoodVar)
                foods.add(tempFoodVar)
                simEnergy += 1
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
    # Check collisions


    # Update
    if not pauseToggle:
        all_sprites.update()
        simRuntime += 1

    # Render
    screen.fill(BLACK)
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    if debugHUDtoggle:
        DebugText = f"Simulation Runtime: {simRuntime}\nNutrient Pellets: {len(foods.sprites())}\nLiving Agents: {len(agents.sprites())}\nSimulation Energy:{simEnergy}"
        blit_text(screen, DebugText, (20, 20), debugFont, color = pygame.Color("white"))
    pygame.display.flip()

pygame.quit()