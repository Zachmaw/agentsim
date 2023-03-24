# V Preinfdev0.4
# Before I can step that up
# using your brain needs to cost slightly more than having it.

# # physicalTraits = [
#       brainWiring: list[neuralConnections],
#       brain_startingConnections: list[neuralConnections],
#       eggSize: int,
#       eggshellThickness: int
#       yolkEnergy: int,
#       size: int,
#       rotStrMult: int,
#       moveStrMult: int
#       so on...
# 
# lifeStages = ["egg", "hatchling", "mature", "elder"]

import pygame
from os import path
from defaults import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.preprocessing.sequence import TimeseriesGenerator
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

img_dir = path.join(path.dirname(__file__), 'img')


def blit_text(surface, text, pos, font, color=pygame.Color("black")):
    # Got this incredibly helpful function from https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame
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

def genesDefault():
    genes = {
      "brainWiring": list[neuralConnection],# each has energy cost = abs(connectionStrength)(/2 while not in use)
      "brain_startingConnections": list[neuralConnection],# no max len, per neuron/synapse cost trippled.
      "eggshell": 0,# multiplier for material cost and Egg deffense
      "yolk": 0,# 
      "size": 1,
      "rotStr": 1,
      "moveStr": 1
    }
    return genes

# initialize pygame and create window
pygame.init()
# pygame.mixer.init()
debugFont = pygame.font.SysFont("monospace", 15)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AgentSim")
clock = pygame.time.Clock()
background = buildBackdrop(screen.get_rect().size)
# define generator
n_input = 3
n_features = 1
generator = TimeseriesGenerator(scaled_train, scaled_train, length=n_input, batch_size=1)
# define groups
all_sprites = pygame.sprite.Group()
agents = pygame.sprite.Group()
foods = pygame.sprite.Group()
# define model
model = Sequential()
model.add(LSTM(100, activation='relu', input_shape=(n_input, n_features)))          # here.
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

# so a default brain..... I'm so confused about the dimentionallity of output space? Right up
# every brain has the same number of inputs and outputs, yes?

# each input neuron has a range of 0-1, weights can be anywhere -4 to 4, and output neurons expect -1 to 1.

# # physicalTraits = [
#       brainWiring: list[neuralConnections],
#       brain_startingConnections: list[neuralConnections],
#       eggshellThickness: int
#       yolkEnergy: int,
#       rotStrMult: int,
#       moveStrMult: int
#       so on...
# 
# Classes
class Brain():
    def __init__(self, genes):
        self.hatchlingStage = []
        self.completedStructure = []
        for connection in genes[1]:
            self.hatchlingStage.append(connection)
        for connection in genes[0]:
            self.completedStructure.append(connection)# so what that does is builds the brain how it will be , based on solely genetic factors, at the begining of adulthood. Ofc experience should come into play, yet to implement.

class Agent(pygame.sprite.Sprite):
    def __init__(self, genes, pos, yolk:"int", eggshell:"int"):
        pygame.sprite.Sprite.__init__(self)
        self.brain = Brain(genes[:2])### initialize brain from genes.
        self.traits = genes[2:]
        self.lifeStage = 0# when spawned in at lifestage zero, am egg. child, adult, elder.
        self.vitality = 10
        self.energy = yolk # energy is equivalent to yolk energy bestowed by parent.
        self.defense = eggshell
        self.radius = eggshell/2 + yolk/3
        self.image_orig = pygame.Surface((self.radius*2, self.radius*2))
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.center = pos
        print("new Agent rect is :"+str(self.rect)+" centered on "+str(self.rect.center))
        self.speedx = 0
        self.speedy = 0
        self.rot_angle = 0# of 359
        self.rot_speed = 0

    def update(self):
        self.speedx *= FRICTION
        self.speedy *= FRICTION
        self.rot_speed *= FRICTION * (self.radius * 0.85)
        self.rect.x = self.rect.x + self.speedx
        self.rect.y = self.rect.y + self.speedy
        self.rot_angle += self.rot_speed
        old_center = self.rect.center# fix sprite angle
        self.image = pygame.transform.rotate(self.image_orig, self.rot_angle)# make a new copy of the original image rotated by current angle and set as self.image
        self.rect = self.image.get_rect()# fix the Rect
        self.rect.center = old_center# keep it in place

    def useEnergy(self, amount):
        if self.energy >= amount:
            self.energy -= amount
        else:# Energy is Not enough, nothing removed
            amount -= self.energy# but use the energy you do have to not take as much damage
            self.energy = 0
            self.vitality -= amount# take it from life instead

    def ageUp(self):
        if self.lifeStage == 0:
            pass
            # make self.defence dynamically related to self.armor?
        self.lifeStage += 1
        ### so the different things
        # egg
        # child
        # adult
        # elder

    def rotate(self, rot_force:"float"):# OUT: a float between -1 and 1
        # SO, it's trying to rotate at a certain intensity. Am I calculating resistance? no.
        # calculate how much energy it takes to rotate the requested amount
        # reduce energy as much as possible, returning the remainder
        # set actual rotation based on used energy



        self.rot_speed += rot_force * self.traits[rotStr]



    def buildEgg(self):# determine size from self.traits
        # cost energy for yolk
        self.useEnergy(self.traits["yolk"])
        # cost material for shell
        pass

    def layEgg(self):
        egg = Agent(self.genes, self.eggSizeFactor, self.rect.center, )
        all_sprites.add(egg)
        agents.add(egg)


    def accelerate(self):
        pass
    

class neuralConnection():
    def __init__(self):
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
















# WHY DIDNT I LEAVE ANY NOTES FOR WHAT THIS WAS ABOUT?!
# X,y = generator[0]
# print(f'Given the Array: \n{X.flatten()}')
# print(f'Predict this y: \n {y}')

# X.shape

# # We do the same thing, but now instead for 12 months
# n_input = 12
# generator = TimeseriesGenerator(scaled_train, scaled_train, length=n_input, batch_size=1)


# model.summary()

# # fit model
# model.fit(generator,epochs=50)

# loss_per_epoch = model.history.history['loss']
# plt.plot(range(len(loss_per_epoch)),loss_per_epoch)

# last_train_batch = scaled_train[-12:]

# last_train_batch = last_train_batch.reshape((1, n_input, n_features))

# model.predict(last_train_batch)

# scaled_test[0]

# test_predictions = []

# first_eval_batch = scaled_train[-n_input:]
# current_batch = first_eval_batch.reshape((1, n_input, n_features))

# for i in range(len(test)):
    
#     # get the prediction value for the first batch
#     current_pred = model.predict(current_batch)[0]
    
#     # append the prediction into the array
#     test_predictions.append(current_pred) 
    
#     # use the prediction to update the batch and remove the first value
#     current_batch = np.append(current_batch[:,1:,:],[[current_pred]],axis=1)

# test_predictions

# test.head()

# test['Predictions'] = scaler.inverse_transform(test_predictions)

# test.plot(figsize=(14,5))













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
                tempAgentVar = Agent(genesInit(), mousePos, defaultYolk, 0)#####
                all_sprites.add(tempAgentVar)
                agents.add(tempAgentVar)
                simEnergy += defaultYolk
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