import pygame
from pygame.locals import *
import random
import math
import time


import os
import shutil

# DIRECTORIES AND FILES

cardData = open('mosiacData.csv', 'w+')
cardData.write("id")

while os.path.isdir("mosaics"):
    shutil.rmtree("mosaics", ignore_errors=True)

neededDirs = ["mosaics"]

for dir in neededDirs:
    os.mkdir(dir)



pygame.init()
pygame.font.init()


WIDTH = 500
HEIGHT = 500


white = (255, 255, 255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
background = (127,255,255)

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
screen.fill(black)

def V2toPointList(points, xOff, yOff):
    out = []
    for point in points:
        out.append([point.x+xOff, point.y+yOff])
    return out

def randColor():
    return (random.randrange(255), random.randrange(255), random.randrange(255))

class Vector2():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Shape():
    initialPoints = []
    points = []
    
    def __init__(self, shape, s=1, hS=1, vS=1):
        self.setPointsOffShape(shape)
        self.scale = s
        self.horzStretch = hS
        self.vertStretch = vS
        self.calculateTransformedPoints()
        
    def setPointsOffShape(self, shape):
        if shape == "square":
            self.initialPoints=[(-1.0,-1.0),(1.0,-1.0),(1.0, 1.0),(-1.0,1.0)]
        elif shape == "equilateral":
            self.initialPoints=[(0.0,1.0),(-0.866,-0.5),(0.866,-0.5)]
        elif shape == "hexagon":
            self.initialPoints=[(1.0,0.0),(0.5774,1.0),(-0.5774,1.0),(-1.0,0.0),(-0.5774,-1.0),(0.5774,-1.0)]
            
    def calculateTransformedPoints(self):
        self.points = []
        for point in self.initialPoints:
            newPoint = Vector2()
            newPoint.x = point[0]*self.horzStretch*self.scale
            newPoint.y = point[1]*self.vertStretch*self.scale
            self.points.append(newPoint)
    
    def setScale(self, value):
        self.scale = value
        self.calculateTransformedPoints()
        
    def setHStretch(self, value):
        self.horzStretch = value
        self.calculateTransformedPoints()
        
    def setVStretch(self, value):
        self.vertStretch = value
        self.calculateTransformedPoints()
        
class Tile():
    bufferWidth=1
    
    rotation = None
    children = None
    
    def __init__(self, shape, pos=Vector2(), s=1, hS=1, vS=1, p=None, c=[]):
        self.shape = Shape(shape,s,hS,vS)
        self.position = pos
        
        self.scale = s
        self.horzStretch = hS
        self.vertStretch = vS
        
        self.parent = p
        self.children = c
        
        self.width = 2*self.horzStretch*self.scale +2*Tile.bufferWidth
        self.height = 2*self.vertStretch*self.scale +2*Tile.bufferWidth
        
        self.createSurface()
        self.createShape()
        self.blitChildren()
        
    def createSurface(self):
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.surface.fill(blue)
        self.surface.set_colorkey(blue)
        
    def createShape(self):
        #for point in self.shape.points:
        #    pygame.draw.circle(self.surface, black, (self.width/2+point.x, self.height/2+point.y), 2)
        pygame.draw.polygon(self.surface, randColor(), V2toPointList(self.shape.points, self.width/2,self.height/2), 0)
            
    def blitChildren(self):
        for child in self.children:
            self.surface.blit(child.surface, (self.width/2+child.position.x-child.width/2, self.height/2+child.position.y-child.height/2))

class TesselationType():
    # Position, Shape, Rotation, 
    nodeMap = []
    
    def __init__(self, type, width, height):
        self.width = width
        self.height = height
        
        if type == "simple-rectangles":
            self.simpleRectangles(width, height, 50, 50)
        elif type == "rotated-rectangles":
            pass
        elif type == "simple-equilaterals":
            pass
        elif type == "rotated-equilaterals":
            pass
        elif type == "simple-hexagons":
            pass
        elif type == "rotated-hexagons":
            pass
    
    def simpleRectangles(self, width, height, sqWidth, sqHeight):
        self.nodeMap = []
        for x in range(int(-width/2 -sqWidth/2), int(width/2 +sqWidth/2)+1, sqWidth):
            for y in range(int(-height/2 -sqHeight/2), int(height/2 +sqHeight/2)+1, sqHeight):
                shapeData = ["hexagon", Vector2(x,y), 1, (sqWidth-2*Tile.bufferWidth)/2, (sqHeight-2*Tile.bufferWidth)/2]
                self.nodeMap.append(shapeData)

class Tesselation():
    type = None
    tiles = []

    def __init__(self, type):
        self.width = type.width
        self.height = type.height

        for tileData in type.nodeMap:
            self.tiles.append(Tile(tileData[0], tileData[1], tileData[2], tileData[3], tileData[4]))
        
        self.createSurface()

    def createSurface(self):
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.surface.fill(white)
        #self.surface.set_colorkey(white)

    def draw(self):
        for tile in self.tiles:
            self.surface.blit(tile.surface, (self.width/2 + tile.position.x-tile.width/2, self.height/2+tile.position.y-tile.height/2))

simpleRectangles = TesselationType("simple-rectangles",500,500)

tessalation = Tesselation(simpleRectangles)
tessalation.draw()
screen.blit(tessalation.surface, (WIDTH/2-tessalation.width/2, HEIGHT/2-tessalation.height/2))



while (True):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
        time.sleep(.01)