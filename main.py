from numpy.core.fromnumeric import var
from numpy.lib.function_base import gradient
from numpy.random.mtrand import f
import pygame
from pygame.locals import *
import random
import math
import time

import matplotlib.pyplot as plt
import numpy as np

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
screen.fill(white)

def V2toPointList(points, xOff, yOff):
    out = []
    for point in points:
        out.append([point.x+xOff, point.y+yOff])
    return out

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
            self.initialPoints=[(-0.707,-0.707),(0.707,-0.707),(0.707, 0.707),(-0.707,0.707)]
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
    bufferWidth=5
    
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
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(blue)
        self.surface.set_colorkey(blue)
        
    def createShape(self):
        for point in self.shape.points:
            pygame.draw.circle(self.surface, black, (self.width/2+point.x, self.height/2+point.y), 2)
        pygame.draw.polygon(self.surface, green, V2toPointList(self.shape.points, self.width/2,self.height/2), 0)
            
    def blitChildren(self):
        for child in self.children:
            self.surface.blit(child.surface, (self.width/2+child.position.x-child.width/2, self.height/2+child.position.y-child.height/2))

class TesselationType():
    # Position, Shape, Rotation, 
    nodeMap = []
    
    def __init__(self, type):
        if type == "simple-rectangles":
            pass
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
    
    def simpleRectangles(self, width, height):
        self.nodeMap = []
        for x in range(width/2, WIDTH/2+width/2):
            for y in range(height/2,HEIGHT/2+height/2):
                shapeData = [Vector2(x,y), ("square", width, height)]

class Tesselation():
    type = None
    tiles = []
    
    def __init__(self, type):
        pass


tile = Tile("hexagon", pos=Vector2(200,200), s=20, c=[Tile("square", s=20)])
screen.blit(tile.surface, (tile.position.x - Tile.bufferWidth, tile.position.y - Tile.bufferWidth))



while (True):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
        time.sleep(.01)