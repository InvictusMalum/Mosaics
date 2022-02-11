from curses.ascii import alt
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

def roundint(x):
    return int(x+0.5)

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
        self.width=0
        self.height=0
        self.getWidths()
        
    def setPointsOffShape(self, shape):
        if shape == "square":
            self.initialPoints=[(-1.0,-1.0),(1.0,-1.0),(1.0, 1.0),(-1.0,1.0)]
        elif shape == "equilateral":
            self.initialPoints=[(0.0,1.0),(-0.866,-0.5),(0.866,-0.5)]
        elif shape == "hexagon":
            self.initialPoints=[(1.0,0.0),(0.5,0.866),(-0.5,0.866),(-1.0,0.0),(-0.5,-0.866),(0.5,-0.866)]
            
    def calculateTransformedPoints(self):
        self.points = []
        for point in self.initialPoints:
            newPoint = Vector2()
            newPoint.x = point[0]*self.horzStretch*self.scale
            newPoint.y = point[1]*self.vertStretch*self.scale
            self.points.append(newPoint)
    
    def getWidths(self):
        maxWidth=0
        maxHeight=0
        for point in self.points:
            if abs(point.x) > maxWidth:
                maxWidth = abs(point.x)
            if abs(point.y) > maxHeight:
                maxHeight = abs(point.y)
        self.width = maxWidth*2
        self.height = maxHeight*2
    
    def setScale(self, value):
        self.scale = value
        self.calculateTransformedPoints()
        self.getWidths()
        
    def setHStretch(self, value):
        self.horzStretch = value
        self.calculateTransformedPoints()
        self.getWidths()
        
    def setVStretch(self, value):
        self.vertStretch = value
        self.calculateTransformedPoints()
        self.getWidths()
        
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
        
        self.width = self.shape.width +2*Tile.bufferWidth
        self.height = self.shape.height +2*Tile.bufferWidth
        
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
            self.simpleEquilaterals(width, height, 24)
        elif type == "rotated-equilaterals":
            pass
        elif type == "simple-hexagons":
            self.simpleHexagons(width, height, 50)
        elif type == "rotated-hexagons":
            pass
    
    def simpleRectangles(self, width, height, sqWidth, sqHeight):
        self.nodeMap = []
        for x in range(roundint(-width/2 -sqWidth/2), roundint(width/2 +sqWidth/2)+1, sqWidth):
            for y in range(roundint(-height/2 -sqHeight/2), roundint(height/2 +sqHeight/2)+1, sqHeight):
                shapeData = ["square", Vector2(x,y), 1, (sqWidth-2*Tile.bufferWidth)/2, (sqHeight-2*Tile.bufferWidth)/2]
                self.nodeMap.append(shapeData)
    
    def simpleEquilaterals(self, width, height, eqWidth):
        self.nodeMap = []
        eqHeight=roundint(eqWidth/2*1.73205)
        alternator = True
        for y in range(roundint(-height/2 -eqHeight/2), roundint(height/2 +eqHeight/2)+1, eqHeight):
            alternator = not(alternator)
            for x in range(roundint(-width/2 -eqWidth/2), roundint(width/2 +eqWidth/2)+1, eqWidth):
                shapeData = []
                if alternator:
                    shapeData = ["equilateral", Vector2(x,y), eqWidth//2, 1, 1]
                else:
                    shapeData = ["equilateral", Vector2(x+eqWidth//2,y), eqWidth//2, 1, 1]
                self.nodeMap.append(shapeData)
        alternator = True
        for y in range(roundint(-height/2 -eqHeight/6), roundint(height/2 +eqHeight/2)+1, eqHeight):
            alternator = not(alternator)
            for x in range(roundint(-width/2), roundint(width/2 +eqWidth)+1, eqWidth):
                shapeData = []
                if alternator:
                    shapeData = ["equilateral", Vector2(x,y), eqWidth//2, 1, -1]
                else:
                    shapeData = ["equilateral", Vector2(x+eqWidth//2,y), eqWidth//2, 1, -1]
                self.nodeMap.append(shapeData)
    
    def simpleHexagons(self, width, height, hexWidth):
        self.nodeMap = []
        hexHeight = roundint(hexWidth/2*1.73205)
        
        alternator=True
        for x in range(round(-width/2), roundint(width/2 +hexWidth)+1, roundint(hexWidth*3/4)-1):
            alternator = not(alternator)
            for y in range(roundint(-height/2 -hexHeight/6), roundint(height/2 +hexHeight/2)+1, hexHeight):
                shapeData = []
                if alternator:
                    shapeData = ["hexagon", Vector2(x,y), hexWidth//2, 1, 1]
                else:
                    shapeData = ["hexagon", Vector2(x,y+hexHeight//2), hexWidth//2, 1, 1]
                self.nodeMap.append(shapeData)
    
    def starHexagons(self, width, height, hexWidth):
        self.nodeMap = []
        hexHeight = roundint(hexWidth/2*1.73205)
        alternator=True
        for y in range(roundint(-height/2 -hexHeight/6), roundint(height/2 +hexHeight/2)+1, hexHeight):
            alternator = not(alternator)
            for x in range(roundint(-width/2), roundint(width/2 +hexWidth)+1, hexWidth):
                shapeData = []
                if alternator:
                    shapeData = ["hexagon", Vector2(x,y), hexWidth//2, 1, 1]
                else:
                    shapeData = ["hexagon", Vector2(x+hexWidth//2,y), hexWidth//2, 1, 1]
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

type = TesselationType("simple-hexagons",500,500)
tessalation = Tesselation(type)
tessalation.draw()
screen.blit(tessalation.surface, (WIDTH/2-tessalation.width/2, HEIGHT/2-tessalation.height/2))



while (True):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
        time.sleep(.01)