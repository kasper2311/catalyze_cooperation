# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 13:43:57 2022

@author: ADMIN
"""
import pygame
import colors
import sys
from catalyze_coop_brain import vec2,writetext,drawhunter,hunter

class movebar:
    def __init__(self,pos1,pos2,width,mrange,hunter,radius,bg = colors.BLACK,color = colors.WHITE):
        assert pos2.y == pos1.y
        assert pos1.x < pos2.x
        self.pos1 = pos1
        self.pos2 = pos2
        self.hunter = hunter
        self.radiush = radius
        self.width = width
        self.mrange = mrange
        self.mousepos = pos1 - vec2(0,0) # Somehow this nonsense is needed to decouple self.pos1 from self.mousepos
        self.color = color
        self.bg = bg
        self.rect = pygame.Rect(pos1.x, pos1.y - (width/2), pos2.x - pos1.x, width)
        
    def draw(self,screen,font):
        radius2 = self.width/2
        place = self.mousepos
        #Draw the rect
        gap1 = 10
        gap2 = 10
        pygame.draw.rect(screen,
                        colors.GRAY,
                        self.rect)
        #Draw circle on top of rect
        pygame.draw.circle(screen, colors.WHITE, [place.x,self.pos1.y], radius2)
        writetext(font, self.mrange[0], screen, (self.pos1 - vec2(gap1,0)).elems(), self.color, self.bg)
        writetext(font, self.mrange[1], screen, (self.pos2 + vec2(gap1,0)).elems(), self.color, self.bg)
        
        
        mloc = vec2(((self.pos2.x - self.pos1.x)/2.) + self.pos1.x,self.pos1.y - (self.radiush*2.0) - gap2)
        writetext(font, self.hunter, screen, (mloc - vec2(0,(self.radiush*3.) - gap2)).elems(), self.color, self.bg)
        drawhunter(screen, mloc.elems(), self.radiush, self.hunter)
    
    def update(self,click):
        cur = vec2(*pygame.mouse.get_pos())
        iscollide = self.rect.collidepoint(cur.x, cur.y)
        if click and iscollide:
            #currently_occupied.add(self)
            self.mousepos = cur
    
    def getval(self):
        posn = (self.mousepos.x - self.pos1.x)/(self.pos2.x - self.pos1.x)
        fin = posn*(self.mrange[1] - self.mrange[0]) + self.mrange[0]
        return fin
    
    def changeposn(self,click,newval):
        #THIS WILL NOT WORK FOR ALL RANGES! ONLY 0-1 RANGES
        cur = vec2(*pygame.mouse.get_pos())
        iscollide = self.rect.collidepoint(cur.x, cur.y)
        if click and iscollide:
            pass
        elif self.mrange[0] != 0 or self.mrange[1] != 1:
            pass
        else:
            #fin = (self.mousepos.x - self.pos1.x)/(self.pos2.x - self.pos1.x)
            self.mousepos.x = newval*(self.pos2.x - self.pos1.x) + self.pos1.x # For 0-1 range only
            
        
        



def create_spaced_bars(screensize,myy,mrange,barwidth,hunters,radius,edge = 40):
    
    lenary = len(hunters)
    scr_ary = edge,screensize[0] - edge
    gaplen = 100
    #An array of x's containing the starts of each bar is ideal
    
    #lenary*barlength + (lenary-1)*gaplen = scr_ary[1] - scr_ary[0]
    barlength = ((scr_ary[1] - scr_ary[0]) - ((lenary - 1)*gaplen))/lenary
    pos1s = [((barlength + gaplen)*j) + edge for j in range(lenary)]
    pos2s = [item + barlength for item in pos1s]
    ys = [myy]*lenary
    
    pos1s = [vec2(item,y) for item,y in zip(pos1s,ys)]
    pos2s = [vec2(item,y) for item,y in zip(pos2s,ys)]
    final = []
    for pos1,pos2,mhunter in zip(pos1s,pos2s,hunters):
        mbar = movebar(pos1, pos2, barwidth, [0,1], mhunter, radius)
        final.append(mbar)
    
    return final

def process_values(barvals):
    if sum(barvals) <= 0:
        return [1/len(barvals)]*len(barvals)
    elif sum(barvals) == 1:
        return barvals
    elif sum(barvals) < 1:
        #again, normalize the non-zero values
        missing = 1 - sum(barvals)
        proportions = [item/sum(barvals) for item in barvals]
        toadd = [missing*proportion for proportion in proportions]
        final = [item + plus for item,plus in zip(barvals,toadd)]
        return final
    elif sum(barvals) > 1:
        #we need to normalize the non-zero values
        excess = sum(barvals) - 1
        proportions = [item/sum(barvals) for item in barvals]
        toremove = [excess*proportion for proportion in proportions]
        final = [item - torm for item,torm in zip(barvals,toremove)]
        return final 
    
    

if __name__ == "__main__":
    pygame.init()
    myfont = font = pygame.font.Font('freesansbold.ttf', 10)
    clock = pygame.time.Clock()
    screensize = pygame.display.Info().current_w,pygame.display.Info().current_h
    mysurfacesize = width, height =screensize[0] - 100,screensize[1] - 200
    screen = pygame.display.set_mode(mysurfacesize)
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
    
    allbars = create_spaced_bars(mysurfacesize, height/2 - 150 , [0,1], 20, hunters[:4], 10)
    allbars += create_spaced_bars(mysurfacesize, height/2 + 150 , [0,1], 20, hunters[4:], 10)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            else:
                pass
        
        
        click = pygame.mouse.get_pressed()[0]
        change = process_values([item.getval() for item in allbars])
        
        i = 0
        for bar in allbars:
            bar.update(click)
            bar.changeposn(click, change[i])
            i += 1
            
        
        
        screen.fill(colors.BLACK)
        for bar in allbars:
            bar.draw(screen,myfont)
        
        pygame.display.flip()
        