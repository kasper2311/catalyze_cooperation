# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 13:43:57 2022

@author: ADMIN
"""

class movebar:
    def __init__(self,pos1,pos2,width,mrange):
        assert pos2.y == pos1.y
        assert pos1.x < pos2.x
        self.pos1 = pos1
        self.pos2 = pos2
        self.mrange = mrange
        self.mousepos = pos1
        self.rect = pygame.Rect(pos1.x, pos1.y - (width/2), width, pos2.x - pos1.x)
        
    def draw(self,screen):
        radius = self.width/2
        place = self.mousepos
        #Draw the rect
        pygame.draw.rect(screen, 
                        colors.GRAY, 
                        self.rect)
        #Draw circle on top of rect
        pygame.draw.circle(screen, colors.WHITE, place, radius)
    
    def update(self,event,currently_occupied):
        if len(currently_occupied) > 0:
            return None
        cur = vec2(*pygame.mouse.get_pos())
        click = pygame.mouse.get_pressed()
        self.rect.collidepoint(x, y)