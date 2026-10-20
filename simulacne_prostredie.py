from dataclasses import dataclass
import agenti 
import numpy as np
import math
from mazelib import Maze
from mazelib.generate.Ellers import Ellers
import random

@dataclass
#Trieda pre uchovavanie vstupov potrebnych pre prostredie
class Parametre:
    sirka:int 
    vyska: int 
    n_lovec: int 
    n_obet: int 
    seed: int 


#Trieda pre samotne prostredie na vykonavanie simulacie
class Prostredie:
    def __init__(self, parametre: Parametre):
        self.parametre = parametre
        self.generator_nahodnych_cisiel = np.random.default_rng(parametre.seed)
        self.tick = 0
        self.agents =[]
        self.pocet_lovec = self.parametre.n_lovec 
        self.pocet_obet = self.parametre.n_obet
        self.reset()
    
    def generacia_prostredia(self):
        
        gen = Maze()
        np.random.seed()
        gen.generator = Ellers(self.parametre.sirka, self.parametre.vyska)
        gen.generate()

        
        return np.array(gen.grid,dtype=int)
        

    def reset(self):
        self.generator_nahodnych_cisiel = np.random.default_rng(self.parametre.seed)
       
        
        #self.rozlozenie_prostredia = self.generacia_prostredia()  

        #Vytvaranie Prostredia s grid tematikou 
        self.rozlozenie_prostredia = np.zeros((self.parametre.vyska, self.parametre.sirka), dtype=int)
        self.rozlozenie_prostredia[0,:] = 1
        self.rozlozenie_prostredia[49,:] = 1
        self.rozlozenie_prostredia[:,0] = 1
        self.rozlozenie_prostredia[:,49] = 1
        #self.rozlozenie_prostredia[2,2:] =1
        #self.rozlozenie_prostredia[8:27,2] =1
        #self.rozlozenie_prostredia[9,2:8] = 1
        #self.rozlozenie_prostredia[33:45,4] = 1
        #self.rozlozenie_prostredia[12:43,6]=1
        #self.rozlozenie_prostredia[12:43,8]=1
        #self.rozlozenie_prostredia[6:43,10]=1
        #self.rozlozenie_prostredia[32:45,2]=1
        #self.rozlozenie_prostredia[45,2:7]=1
        self.rozlozenie_prostredia[0:23,23]=1
        self.rozlozenie_prostredia[0:23,25]=1
        self.rozlozenie_prostredia[25:49,23]=1
        self.rozlozenie_prostredia[25:49,25]=1
        self.rozlozenie_prostredia[23,0:23]=1
        self.rozlozenie_prostredia[25,0:23]=1
        self.rozlozenie_prostredia[23,0:24]=1
        self.rozlozenie_prostredia[25,0:23]=1
        self.rozlozenie_prostredia[25,25:49]=1
        self.rozlozenie_prostredia[23,25:49]=1
        self.rozlozenie_prostredia[24,24]=2
        self.tick = 0
        
        #Snaha o generator a nahodnu volbu pre hunterov a koristi
        pocet_agentov = self.pocet_lovec + self.pocet_obet
        nulove_polia = np.argwhere(self.rozlozenie_prostredia == 2)
        indexy_buniek = self.generator_nahodnych_cisiel.choice(len(nulove_polia),pocet_agentov,False)

        uhlik = math.pi/2
        for poradie,indexy in enumerate(indexy_buniek):
            pozicia = tuple((nulove_polia[indexy]+0.5).tolist())
            if poradie < self.pocet_lovec:
                self.agents.append(agenti.Lovec(pozicia,uhol=uhlik))
            else:
                self.agents.append(agenti.Korist(pozicia,uhol=uhlik))

    
    def range_agentov(self,agentus_manus):
        visible=[]
        
        if isinstance(agentus_manus,agenti.Lovec):
                pocet_rays = 5
                y_agent,x_agent = agentus_manus.pozicia
                vy,vx,hy,hx = y_agent, x_agent,y_agent,x_agent 
                uhol = agentus_manus.uhol_agent   
                dof,uhol_luca,bunka_x, bunka_y=0,0,0,0
                ray_x,ray_y,y_offset,x_offset=0,0,0,0
                final_distance,pomocne_oznacenie_h,pomocne_oznacenie_v,oznacenie=0,0,0,0
                distH,distV = 1000000,1000000
                range_lovec = 9 
                
               
                fov = math.radians(90)
                for i in range(pocet_rays):
                    dof=0
                    distH,distV=1000000,1000000
                    pomocne_oznacenie_h,pomocne_oznacenie_v=0,0
                    final_distance,oznacenie = 0,0
                    
                    if pocet_rays == 1:
                            offset = 0
                    else:
                        offset = -fov / 2 + i * fov / (pocet_rays - 1)
                        
                    uhol_luca = uhol + offset
                    delta_y,delta_x = math.sin(uhol_luca) * 5, math.cos(uhol_luca) * 5  
        
                     
                    #Horizontalne luce  
                    if delta_y < 0: #Pozeranie hore
                        ray_y = math.floor(y_agent) - 0.001
                        ray_x = (y_agent - ray_y )*(-delta_x/delta_y)+x_agent
                        y_offset = -1
                        x_offset =-y_offset*(-delta_x/delta_y)
                        
                    if delta_y > 0: #Pozeranie dole
                        ray_y = math.floor(y_agent) + 1
                        ray_x = (y_agent - ray_y )*(-delta_x/delta_y)+x_agent
                        y_offset = 1
                        x_offset =-y_offset*(-delta_x/delta_y)
                        
                    if delta_y == 0: #Pozeranie v pravo a lavo
                        ray_x=x_agent
                        ray_y=y_agent
                        dof=8
                    while dof < 8:
                        bunka_x = math.floor(ray_x)
                        bunka_y = math.floor(ray_y)
                        if 0 <= bunka_y < self.parametre.vyska and 0 <= bunka_x < self.parametre.sirka and self.rozlozenie_prostredia[bunka_y][bunka_x] == 1: #trafili sme stenu
                            hx = ray_x
                            hy= ray_y
                            distH = math.sqrt((hx-x_agent)*(hx-x_agent)+(hy-y_agent)*(hy-y_agent))
                            pomocne_oznacenie_h = 1
                            dof = 8
                        else: #dalsia ciara
                            ray_x += x_offset
                            ray_y += y_offset
                            dof +=1

                    dof=0
                        #Vertikalne luce
                    if delta_x < 0: #Pozeranie vlavo
                        ray_x = math.floor(x_agent) - 0.001
                        ray_y = (x_agent - ray_x )*(-delta_y/delta_x)+y_agent
                        x_offset = -1
                        y_offset =-x_offset*(-delta_y/delta_x)
                                                
                    if delta_x > 0: #Pozeranie vpravo
                        ray_x = math.floor(x_agent) + 1
                        ray_y = (x_agent - ray_x )*(-delta_y/delta_x)+y_agent
                        x_offset = 1
                        y_offset =-x_offset*(-delta_y/delta_x)
                                                
                    if delta_x == 0: #Pozeranie hore, dole
                        ray_x=x_agent
                        ray_y=y_agent
                        dof=8
                    while dof < 8:
                        bunka_x = math.floor(ray_x)
                        bunka_y = math.floor(ray_y)
                        if 0 <= bunka_y < self.parametre.vyska and 0 <= bunka_x < self.parametre.sirka and self.rozlozenie_prostredia[bunka_y][bunka_x] == 1: #trafili sme stenu
                            dof = 8
                            vx= ray_x
                            vy= ray_y
                            distV = math.sqrt((vx-x_agent)*(vx-x_agent)+(vy-y_agent)*(vy-y_agent))
                            pomocne_oznacenie_v=1
                        else: #dalsia ciara
                            ray_x += x_offset
                            ray_y += y_offset
                            dof +=1
                    if distV < distH:
                            ray_x=vx
                            ray_y=vy
                            final_distance = distV
                            oznacenie = pomocne_oznacenie_v
                    else:# distH <distV
                            ray_x=hx
                            ray_y=hy    
                            final_distance = distH
                            oznacenie = pomocne_oznacenie_h
                    if final_distance > range_lovec:
                            oznacenie =0
                            final_distance = 0
                    visible.append((oznacenie,final_distance))   
                            
                            #https://www.youtube.com/watch?v=gYRrGTC7GtA&t=376s tutorial, pri nechapani bola vyuzita AI
        


        
        if isinstance(agentus_manus,agenti.Korist):
                pocet_rays = 5
                y_agent,x_agent = agentus_manus.pozicia
                vy,vx,hy,hx = y_agent, x_agent,y_agent,x_agent 
                uhol = agentus_manus.uhol_agent   
                dof,uhol_luca,bunka_x, bunka_y=0,0,0,0
                ray_x,ray_y,y_offset,x_offset=0,0,0,0
                final_distance,pomocne_oznacenie_h,pomocne_oznacenie_v,oznacenie=0,0,0,0
                distH,distV = 1000000,1000000
                range_korist = 13
            
                fov = math.radians(90)
                for i in range(pocet_rays):
                    dof=0
                    distH,distV=1000000,1000000
                    pomocne_oznacenie_h,pomocne_oznacenie_v=0,0
                    final_distance,oznacenie = 0,0
                    

                    if pocet_rays == 1:
                            offset = 0
                    else:
                        offset = -fov / 2 + i * fov / (pocet_rays - 1)

                    uhol_luca = uhol + offset
                    delta_y,delta_x = math.sin(uhol_luca) * 5,math.cos(uhol_luca) * 5  
                    
                     
                    #Horizontalne luce  
                    if delta_y < 0: #Pozeranie hore
                        ray_y = math.floor(y_agent) - 0.001
                        ray_x = (y_agent - ray_y )*(-delta_x/delta_y)+x_agent
                        y_offset = -1
                        x_offset =-y_offset*(-delta_x/delta_y)
                        
                    if delta_y > 0: #Pozeranie dole
                        ray_y = math.floor(y_agent) + 1
                        ray_x = (y_agent - ray_y )*(-delta_x/delta_y)+x_agent
                        y_offset = 1
                        x_offset =-y_offset*(-delta_x/delta_y)
                        
                    if delta_y == 0: #Pozeranie v pravo a lavo
                        ray_x=x_agent
                        ray_y=y_agent
                        dof=8
                    while dof < 8:
                        bunka_x = math.floor(ray_x)
                        bunka_y = math.floor(ray_y)
                        if 0 <= bunka_y < self.parametre.vyska and 0 <= bunka_x < self.parametre.sirka and self.rozlozenie_prostredia[bunka_y][bunka_x] == 1: #trafili sme stenu
                            hx = ray_x
                            hy= ray_y
                            distH = math.sqrt((hx-x_agent)*(hx-x_agent)+(hy-y_agent)*(hy-y_agent))
                            pomocne_oznacenie_h = 1
                            dof = 8
                        else: #dalsia ciara
                            ray_x += x_offset
                            ray_y += y_offset
                            dof +=1

                    dof=0
                    #Vertikalne luce
                    if delta_x < 0: #Pozeranie vlavo
                            ray_x = math.floor(x_agent) - 0.001
                            ray_y = (x_agent - ray_x )*(-delta_y/delta_x)+y_agent
                            x_offset = -1
                            y_offset =-x_offset*(-delta_y/delta_x)
                                                
                    if delta_x > 0: #Pozeranie vpravo
                            ray_x = math.floor(x_agent) + 1
                            ray_y = (x_agent - ray_x )*(-delta_y/delta_x)+y_agent
                            x_offset = 1
                            y_offset =-x_offset*(-delta_y/delta_x)
                                                
                    if delta_x == 0: #Pozeranie hore, dole
                            ray_x=x_agent
                            ray_y=y_agent
                            dof=8
                    while dof < 8:
                        bunka_x = math.floor(ray_x)
                        bunka_y = math.floor(ray_y)
                        if 0 <= bunka_y < self.parametre.vyska and 0 <= bunka_x < self.parametre.sirka and self.rozlozenie_prostredia[bunka_y][bunka_x] == 1: #trafili sme stenu
                            dof = 8
                            vx= ray_x
                            vy= ray_y
                            distV = math.sqrt((vx-x_agent)*(vx-x_agent)+(vy-y_agent)*(vy-y_agent))
                            pomocne_oznacenie_v=1
                        else: #dalsia ciara
                            ray_x += x_offset
                            ray_y += y_offset
                            dof +=1
                    if distV < distH:
                        ray_x=vx
                        ray_y=vy
                        final_distance = distV
                        oznacenie = pomocne_oznacenie_v
                    else: #distH <distV
                        ray_x=hx
                        ray_y=hy    
                        final_distance = distH
                        oznacenie = pomocne_oznacenie_h
                    
                             
                    if final_distance > range_korist:
                        oznacenie =0
                        final_distance = 0
                    visible.append((oznacenie,final_distance))   
        
        
        return visible

   
    def krok(self):
        #Faza 1 
        rozhodnutia = []
        for agent in self.agents:
            pozorovanie = self.range_agentov(agent)
            akcia = agent.rozhodnutie(pozorovanie)
            rozhodnutia.append((agent,akcia))
            print(type(agent).__name__,akcia)
            
        #Faza 2 
        for agent, akcia in rozhodnutia: 
            self.sprav(agent,akcia)
        
        self.tick +=1

    def dopredu(self,agent,uhol, krok):
        y_agent, x_agent = agent.pozicia
        uhol_ = agent.uhol_agent
        delta_x,delta_y = math.cos(uhol_), math.sin(uhol_)
        hotove_x,hotove_y = x_agent + delta_x*krok,y_agent + delta_y*krok
        stara_y, stara_x=math.floor(y_agent),math.floor(x_agent)
        bunka_X,bunka_Y = math.floor(hotove_x),math.floor(hotove_y)
        diagonala,blokada = (bunka_Y != stara_y and bunka_X != stara_x),self.rozlozenie_prostredia[bunka_Y][bunka_X] ==1
        
        if diagonala:
            if (self.rozlozenie_prostredia[stara_y][bunka_X] ==1 or self.rozlozenie_prostredia[bunka_Y][stara_x] == 1): 
                blokada = True   
        if not blokada:
             agent.pozicia = (hotove_y,hotove_x)
    
    #TODO Treba spravit, aby po naburani bola normlana reakcia        
    def sprav(self, agent, action):
        uhol_=agent.uhol_agent
        if action == agenti.Agenti.Pohyb.Dopredu.value:
           self.dopredu(agent,agent.uhol_agent,krok=0.1)
        if action == agenti.Agenti.Pohyb.Pravo_chod.value:
            krok_uhla = agent.uhol_krok
            self.dopredu(agent,agent.uhol_agent+krok_uhla/2,0.1)   
            agent.uhol_agent = (agent.uhol_agent + krok_uhla) % ( 2 * math.pi)

        if action == agenti.Agenti.Pohyb.DoPrava.value:  
            if isinstance(agent, agenti.Lovec):
                agent.uhol_agent = uhol_ + agenti.Lovec.uhol_otocenia 
                       
            if isinstance(agent, agenti.Korist):
                agent.uhol_agent = uhol_ + agenti.Korist.uhol_otocenia 
            
                          
        if action == agenti.Agenti.Pohyb.Dolava.value:  
            if isinstance(agent, agenti.Lovec):
                agent.uhol_agent = uhol_ - agenti.Lovec.uhol_otocenia 
                       
            if isinstance(agent, agenti.Korist):
                    agent.uhol_agent = uhol_ - agenti.Korist.uhol_otocenia 
                    
       
                              
        