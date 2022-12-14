# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 12:40:07 2022

@author: ADMIN
"""

import pygame
import colors
import numpy as np
from catalyze_coop_brain import *
from movebarscript import *
import sys



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
            drawhunter(screen, mloc, self.radius, hunter)
     



#if __name__ == "__main__":
pygame.init()
clock = pygame.time.Clock()
framerate = 1 # In case you want to limit framerate to look at things slowly
screensize = pygame.display.Info().current_w,pygame.display.Info().current_h
mysurfacesize = width, height =1000,700
screen = pygame.display.set_mode(mysurfacesize)

BACKGROUND = colors.BLACK
myfont = font = pygame.font.Font('freesansbold.ttf', 10)
font = pygame.font.Font('freesansbold.ttf', 20)


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


hunters = [hunter(*item) for item in strategies]

###########################edit these#####################################
size = 5 #number of hunters out of total to create a group
payoffs = [1,4] #Harepayoff, stagpayoff
stagthresh = 4 #Number of hunters needed for a successful stag hunt
fitnessweight = 0.9 #Contribution of the game to fitness
drawwhen = 20 #update screen every 20 generations
##########################################################################
radius = 10
overlap = 5


mygen = 0
i = 0
paused = False

init = True

midpoint = int(len(hunters)/2)

allbars = create_spaced_bars(mysurfacesize, height/2 - 150 , [0,1], 20, hunters[:midpoint], 10)
allbars += create_spaced_bars(mysurfacesize, height/2 + 150 , [0,1], 20, hunters[midpoint:], 10)
totalbar = basemovebar(vec2((width/2) - 100,height - 100), vec2((width/2) + 100,height - 100), 20, [100,1000])
mutn = mutnbar(vec2((width/2) - 100,100), vec2((width/2) + 100,100), 20, [0,1])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            if event.key == pygame.K_RETURN:
                #This will restart the process whenever we press enter
                proportions = [item.getval() for item in allbars]
                mytotal = totalbar.getval("int")
                mymutnrate = mutn.getval("_")
                mygen = 0
                thescene = myscene(strategies,proportions,mytotal,size,payoffs,fitnessweight,stagthresh,mymutnrate,mysurfacesize,radius,overlap)
                init = not init
                
    
    if init:
        click = pygame.mouse.get_pressed()[0]
        change = process_values([item.getval() for item in allbars])
        
        i = 0
        totalbar.update(click)
        mutn.update(click)
        for bar in allbars:
            bar.update(click)
            bar.changeposn(click, change[i])
            i += 1
            
        
        
        screen.fill(BACKGROUND)
        totalbar.draw(screen, myfont, "TOTAL")
        mutn.draw(screen, myfont, "MUTATION PROBABILITY")
        for bar in allbars:
            bar.draw(screen,myfont)
        writetext(font,"Press Enter to simulate",screen,[width/2 , height - 40],colors.WHITE,BACKGROUND)
        writetext(font,"Once simulation starts, press Space to pause and Enter to return",screen,[width/2 , height - 20],colors.WHITE,BACKGROUND)
        pygame.display.flip()
    else:
        if not paused:
            thescene.c_taketimestep()
            mygen += 1
    
        screen.fill(BACKGROUND)
    
        if i % drawwhen == 0:
            thescene.updatehunters()
            i = 0
    
        thescene.draw(screen)
    
        i += 1
    
        writetext(font,f"GEN {mygen}",screen,[width/2 , height - 10],colors.WHITE,BACKGROUND)
        pygame.display.flip()
                
        
    