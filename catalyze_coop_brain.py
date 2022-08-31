# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 17:34:57 2022

@author: ADMIN
"""
import pygame
import colors
import numpy as np

def drawhunter(screen,mloc,radius,hunter):
    hunterstrat,belief = hunter.getme()[:2],hunter.getme()[2]
    if hunterstrat[0] == "S":
        pygame.draw.circle(surface = screen, color = colors.TOMATO, center = mloc, radius = radius, draw_top_right= True, draw_top_left=True)
    else:
        pygame.draw.circle(surface = screen, color = colors.GREEN, center = mloc, radius = radius, draw_top_right= True, draw_top_left=True)
            
    if hunterstrat[1] == "S":
        pygame.draw.circle(surface = screen,color = colors.TOMATO, center = mloc, radius = radius, draw_bottom_left=True,draw_bottom_right= True)
    else:
        pygame.draw.circle(surface = screen, color = colors.GREEN, center = mloc, radius = radius, draw_bottom_left=True,draw_bottom_right= True)
            
    if belief == 1:
        pygame.draw.circle(surface = screen,color = colors.AQUA, center = mloc, radius = radius/2)
    else:
        pygame.draw.circle(surface = screen,color = colors.YELLOW, center = mloc, radius = radius/2)

def writetext(font,towrite,screen,loc,color,background):
    text = font.render(f'{towrite}', True, color, background)
    textRect = text.get_rect()
    textRect.center = ( loc[0] , loc[1] )
    screen.blit(text,textRect)

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


class hunter:
    def __init__(self,a1,a2,u):
        self.a1 = a1
        self.a2 = a2
        self.u = u
    
    def getstrat(self,consensus):
        if consensus == 1:
            return self.a1
        return self.a2
    
    def getme(self):
        return self.a1,self.a2,self.u
    
    def reproduce(self,mutation,allstrats):
        mrand = np.random.uniform(0,1)
        if mrand <= mutation:
            pick = np.random.randint(0,7)
            newstrat = allstrats[pick]
        else:
            newstrat = self.getme()
        return hunter(*newstrat)
    def __repr__(self):
        return f"{self.a1} {self.a2} {self.u}"


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def consensus1forsim(hunterchunk):
    mine = [item.u for item in hunterchunk if item.u == 1]
    return len(mine)/len(hunterchunk)


def gethunterstrat(hunter,consensus,typecheck):
    if consensus == 1:
        return int(hunter[0] == typecheck)
    return int(hunter[1] == typecheck)

def getgroups(thelen,size):
    torandomize = np.arange(0,thelen,1)
    np.random.shuffle(torandomize)
    return chunker(torandomize,size)

def getnarrative(proba1):
    mrand = np.random.uniform(0,1)
    if mrand <= proba1:
        return 1
    return 2

def calc_payoff_for_each_hunter(listofhunters,chunk,payoffs,stagthresh):
    hunterchunk = [listofhunters[item] for item in chunk]
    proba1 = consensus1forsim(hunterchunk)
    consensus = getnarrative(proba1)
    #Once we have the narratives, we can calculate the strategy
    strats = [item.getstrat(consensus) for item in hunterchunk]
    m_payoffs = []
    stags = len([item for item in strats if item == "S"]) >= stagthresh
    for item in strats:
        if item == "H":
            m_payoffs.append(payoffs[0])
        elif item == "S":
            if stags:
                m_payoffs.append(payoffs[1])
            else:
                m_payoffs.append(0)
    
    return m_payoffs

def fromcontcdf(cdf_array,randnum):
    mymax = -1
    idx = 0
    res = None
    for item in cdf_array:
        if item > randnum:
            break
        if item > mymax:
            mymax = item
            res = idx
        idx += 1
        #Keep going upwards until you reach the largest number in the distribution that's smaller than randnum...
        #Get the index associated... that's the hunter you chose
    return res

def getfitnessandreproduce(allpayoffs,weight = 1.0):
    #allpayoffs = A bunch of 0,Hare_pay,Stag_pay for each hunter
    #Two things to consider, the frequency of the people with different payoffs, and the difference in payoffs themselves
    #1 + wf -> w is the weight to the game, f is the payoff itself! ok that's cool
    fitness = 1 + (weight*np.array(allpayoffs))
    total_fitness = np.sum(fitness)
    proba_selection = fitness/total_fitness
    
    #Selection for death is RANDOM
    proba_death = np.array([1.0/len(allpayoffs)]*len(allpayoffs))
    
    #How to sample from this distribution -> Inverse transform sampling
#     cdf = np.array([np.sum(proba_selection[:item]) for item in range(1,len(proba_selection) + 1,1)])
#     cdfdie = np.array([np.sum(proba_death[:item]) for item in range(1,len(proba_death) + 1,1)])
    
#     todie = 0
#     toreprod = 0
#     while todie == toreprod:
#         choose_reprod = np.random.uniform(0,1)
#         choose_die = np.random.uniform(0,1)
#         toreprod = fromcontcdf(cdf,choose_reprod)
#         todie = fromcontcdf(cdfdie,choose_die)
    
    #This is also built-in though, so might as well do that
    toreprod = -1
    todie = -1
    while todie == toreprod:
        toreprod = np.random.choice(list(range(len(allpayoffs))),1,p=proba_selection)[0] #specifying p is important
        todie = np.random.choice(list(range(len(allpayoffs))),1,p=proba_death)[0]
    
    return toreprod,todie

def getnextgen(hunterlist,toreprod,todie,mutation,strategies):
    #Population size remains the same
    reprod = hunterlist[toreprod]
    
    new = reprod.reproduce(mutation,strategies)
    hunterlist[todie] = new
    
def taketimestep(hunterlist,size,payoffs,stagthresh,fitnessweight,mutnrate,strategies):
    m_chunks = getgroups(len(hunterlist),size)
    payofflist = [0]*len(hunterlist)
    for chunk in m_chunks:
        m_payoffs = calc_payoff_for_each_hunter(hunterlist,chunk,payoffs,stagthresh)
        i = 0
        for idx in chunk:
            payofflist[idx] = m_payoffs[i]
            i += 1
    toreprod,todie = getfitnessandreproduce(payofflist,weight = fitnessweight)
    getnextgen(hunterlist,toreprod,todie,mutnrate,strategies)
    
def spawnhunters(strategies,proportions,total):
    #Strategies {1:("H","H",1),2:("H","S",1)...and so on}
    #proportions {1:0.2,2:0.2...and so on}
    mynums = dict()
    for i,proportion in enumerate(proportions):
        mynum = round(total*proportions[i])
        mynums[i] = mynum
    myres = []
    for item in mynums:
        myres += [hunter(*strategies[item]) for i in range(mynums[item])]
    print(len(myres))
    return myres