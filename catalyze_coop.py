# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 12:40:07 2022

@author: ADMIN
"""

import pygame
import colors
import numpy as np
from catalyze_coop_brain import *
import sys

class vec2:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def elems(self):
        return self.x,self.y
    
    def __add__(self,pos2):
        return vec2(self.x + pos2.x,self.y + pos2.y)
    
    def __sub__(self,pos2):
        return vec2(self.x - pos2.x,self.y - pos2.y)
    
    def mag(self):
        return (self.x**2 + self.y**2)**0.5
    
    def __truediv__(self,myfrac):
        if isinstance(myfrac,vec2):
            return vec2(*[a/b for a,b in zip(self.elems(),myfrac)])
        else:
            return vec2(self.x/myfrac,self.y/myfrac)
    
    def __mul__(self,myfrac):
        if isinstance(myfrac,vec2):
            return vec2(*[a*b for a,b in zip(self.elems(),myfrac)])
        else:
            return vec2(self.x*myfrac,self.y*myfrac)
    
    def __repr__(self):
        return "({}, {})".format(self.x,self.y)
    
    def __getitem__(self,i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        else:
            raise KeyError

def gen_random_point(xrange,yrange):
    myx = np.random.randint(xrange[0],xrange[1] + 1)
    myy = np.random.randint(yrange[0],yrange[1] + 1)
    return myx,myy

def getminimadist(newpoint,allpoints):
    return min([(newpoint - item).mag() for item in allpoints])

def gen_hunter_locs(hunterlist,xrange,yrange,radius):
    #xrange is [0,width of drawscreen]
    #yrange is [0,length of drawscreen]
    reslist = []
    
    for i in range(len(hunterlist)):
        newpoint = vec2(*gen_random_point(xrange, yrange))
        if len(reslist) > 0:
            #This implementation is terrible
            while getminimadist(newpoint, reslist) < radius:
                newpoint = vec2(*gen_random_point(xrange, yrange))
            reslist.append(newpoint)
        else:
            reslist.append(newpoint)
            
    
    resdict = dict(zip(range(len(hunterlist)),reslist))
    
    return resdict



class myscene:
    def __init__(self,strategies,proportions,total,size,payoffs,fitnessweight,stagthresh,mutnrate,screensize,radius,overlap):
        self.hunterlist = spawnhunters(strategies, proportions, total)
        self.oldhunters = self.hunterlist.copy()
        self.radius = abs(radius)
        self.loclist = gen_hunter_locs(self.hunterlist,[0,screensize[0] - (2*int(radius))],[0,screensize[1] - (2*int(radius))],abs(radius - overlap))
        self.total = total
        self.size = size
        self.payoffs = payoffs
        self.fitnessweight = fitnessweight
        self.stagthresh = stagthresh
        self.mutnrate = mutnrate
        self.strategies = strategies
        #How would you paint this?
    
    def c_taketimestep(self):
        taketimestep(self.hunterlist,self.size,self.payoffs,self.stagthresh,self.fitnessweight,self.mutnrate,self.strategies)
    
    def updatehunters(self):
        self.oldhunters = self.hunterlist
    
    def draw(self,screen):
        for k,hunter in enumerate(self.oldhunters):
            mloc = self.loclist[k].elems()
            hunterstrat,belief = hunter.getme()[:2],hunter.getme()[2]
            if hunterstrat[0] == "S":
                pygame.draw.circle(surface = screen, color = colors.TOMATO, center = mloc, radius = self.radius, draw_top_right= True, draw_top_left=True)
            else:
                pygame.draw.circle(surface = screen, color = colors.GREEN, center = mloc, radius = self.radius, draw_top_right= True, draw_top_left=True)
            
            if hunterstrat[1] == "S":
                pygame.draw.circle(surface = screen,color = colors.TOMATO, center = mloc, radius = self.radius, draw_bottom_left=True,draw_bottom_right= True)
            else:
                pygame.draw.circle(surface = screen, color = colors.GREEN, center = mloc, radius = self.radius, draw_bottom_left=True,draw_bottom_right= True)
            
            if belief == 1:
                pygame.draw.circle(surface = screen,color = colors.AQUA, center = mloc, radius = self.radius/2)
            else:
                pygame.draw.circle(surface = screen,color = colors.YELLOW, center = mloc, radius = self.radius/2)
                

pygame.init()
clock = pygame.time.Clock()
framerate = 1 # In case you want to limit framerate to look at things slowly
screensize = pygame.display.Info().current_w,pygame.display.Info().current_h
print(screensize)
mysurfacesize = width, height =screensize[0] - 100,screensize[1] - 200
screen = pygame.display.set_mode(mysurfacesize)
drawwhen = 20 # update every 20 generations




strategies = [
    ("H","H",1),
    ("H","H",2),
    ("H","S",1),
    ("H","S",2),
    ("S","H",1),
    ("S","H",2),
    ("S","S",1),
    ("S","S",2)
]

proportions = [
    0.5,
    0.0,
    0.1,
    0.0,
    0.1,
    0.0,
    0.0,
    0.3
]

total = 100
size = 5
payoffs = [1,4] #Hare,stag
stagthresh = 4
fitnessweight = 0.9
mutnrate = 0.001
radius = 10
overlap = 5

thescene = myscene(strategies,proportions,total,size,payoffs,fitnessweight,stagthresh,mutnrate,mysurfacesize,radius,overlap)

mygen = 0
i = 0
font = pygame.font.Font('freesansbold.ttf', 20)

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
    screen.fill(colors.BLACK)
    thescene.c_taketimestep()
    
    if i % drawwhen == 0:
        thescene.updatehunters()
        i = 0
    
    thescene.draw(screen)
    #pygame.draw.circle(screen, colors.AQUA, center=(200,200), radius=20)
    
    i += 1
    mygen += 1
    text = font.render(f'{mygen}', True, colors.BLACK, colors.WHITE)
    textRect = text.get_rect()
    textRect.center = ( width/2 , height - 10 )
    screen.blit(text,textRect)
    pygame.display.flip()