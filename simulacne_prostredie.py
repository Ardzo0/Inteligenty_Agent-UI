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
       
        
        self.rozlozenie_prostredia = self.generacia_prostredia() 
        self.vyska, self.sirka = self.rozlozenie_prostredia.shape
        #Vytvaranie Prostredia s grid tematikou 
        self.tick = 0
        
        #Podľa celkového počtu agentov vyberie tabulku nulových polií pomoocu argwhere teraz tam je 2, pretoze testujem custom spawn v strede
        pocet_agentov = self.pocet_lovec + self.pocet_obet
        nulove_polia = np.argwhere(self.rozlozenie_prostredia == 0)
        indexy_buniek = self.generator_nahodnych_cisiel.choice(len(nulove_polia),pocet_agentov,False)

        uhlik = 0#math.pi/2#Štartovací uhol pre agenta v tomto pripade sa každý agent pozerá dole. Všetky uhly sú v radianoch, lebo math.sin, math.cos pracuju s nimi. V buducnosti je možne...
        #Spraviť nahodné uhly nech im to da od 0 - math.pi * 2
        for poradie,indexy in enumerate(indexy_buniek):
            pozicia = tuple((nulove_polia[indexy]+0.5).tolist())
            if poradie < self.pocet_lovec:
                self.agents.append(agenti.Lovec(pozicia,uhol=uhlik))
            else:
                self.agents.append(agenti.Korist(pozicia,uhol=uhlik))

    
    def range_agentov(self,agentus_manus):
        visible=[]
        
        if isinstance(agentus_manus,agenti.Lovec):
                pocet_rays = 35
                y_agent,x_agent = agentus_manus.pozicia
                vy,vx,hy,hx = y_agent, x_agent,y_agent,x_agent 
                uhol = agentus_manus.uhol_agent   
                dof,uhol_luca,bunka_x, bunka_y=0,0,0,0
                ray_x,ray_y,y_offset,x_offset=0,0,0,0
                final_distance,pomocne_oznacenie_h,pomocne_oznacenie_v,oznacenie=0,0,0,0
                distH,distV = 1000000,1000000
                range_lovec = 9 
                
               
                fov = math.radians(180)
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
                        if 0 <= bunka_y < self.vyska and 0 <= bunka_x < self.sirka and self.rozlozenie_prostredia[bunka_y][bunka_x] == 1: #trafili sme stenu
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
                        if 0 <= bunka_y < self.vyska and 0 <= bunka_x < self.sirka and self.rozlozenie_prostredia[bunka_y][bunka_x] == 1: #trafili sme stenu
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
                            final_distance = max(0, final_distance - agentus_manus.polomer)
                            oznacenie = pomocne_oznacenie_v
                    else:# distH <distV
                            ray_x=hx
                            ray_y=hy    
                            final_distance = distH
                            final_distance = max(0, final_distance - agentus_manus.polomer)
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
                        if 0 <= bunka_y < self.vyska and 0 <= bunka_x < self.sirka and self.rozlozenie_prostredia[bunka_y][bunka_x] == 1: #trafili sme stenu
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
                        if 0 <= bunka_y < self.vyska and 0 <= bunka_x < self.sirka and self.rozlozenie_prostredia[bunka_y][bunka_x] == 1: #trafili sme stenu
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
                        final_distance = max(0, final_distance - agentus_manus.polomer)
                        oznacenie = pomocne_oznacenie_v
                    else: #distH <distV
                        ray_x=hx
                        ray_y=hy    
                        final_distance = distH
                        final_distance = max(0, final_distance - agentus_manus.polomer)
                        oznacenie = pomocne_oznacenie_h
                    
                             
                    if final_distance > range_korist:
                        oznacenie =0
                        final_distance = 0
                    visible.append((oznacenie,final_distance))   
        
        
        return visible

   
    def krok(self):
        #Faza 1 - Prejde pole vytvorených agentov a načíta pozorovanie pre nich a ich reakcie.
        rozhodnutia = []
        for agent in self.agents:
            pozorovanie = self.range_agentov(agent)
            akcia = agent.rozhodnutie(pozorovanie)
            rozhodnutia.append((agent,akcia))
            #print("Agent:",type(agent).__name__,"\n","Príkaz v kodovom tvare:",akcia,"\n""Pozicia:",agent.pozicia)
            
        #Faza 2 - Sprav skontroluje akciu jednotlivého agenta a či je legalna 
        for agent, akcia in rozhodnutia: 
            self.sprav(agent,akcia)
        
        self.tick +=1

        
    
    def rychlosti(self,agent, akcia):
        P = agenti.Agenti.Pohyb
        if akcia == P.Dopredu.value:
             return agent.v_max, 0.0
        if akcia == P.OtocenieKUhlu.value:
             return 0.0, max(-agent.w_max, min(agent.w_max, agent.chyba_uhla()))
        raise ValueError(f"Nepoznám chuju: {akcia}")
    
    def integruj(self, agent, v,w):
         y_agent, x_agent = agent.pozicia
         uhol = agent.uhol_agent
         stred = uhol + w /2
         y_agent += v * math.sin(stred)  
         x_agent += v * math.cos(stred)
         agent.uhol_agent = (uhol +w) % (2 * math.pi)
         return y_agent,x_agent
    
    def vytlac_zo_steny(self, y_agent, x_agent, r):
         vyska, sirka = self.vyska, self.sirka
         for _ in range(2):
              by, bx = math.floor(y_agent), math.floor(x_agent)
              for cy in range(by -1, by + 2):
                   for cx in range(bx -1, bx+2):
                        if not (0 <= cy < vyska and 0 <= cx < sirka):
                            continue
                        if self.rozlozenie_prostredia[cy][cx] !=1:
                             continue
                        ny = min(max(y_agent,cy), cy + 1)
                        nx = min(max(x_agent,cx),cx+1)
                        dy,dx = y_agent -ny, x_agent - nx
                        d2 = dy *dy + dx*dx
                        if 1e-12 < d2 < r *r:
                             d =math.sqrt(d2)
                             y_agent += dy / d *(r-d)
                             x_agent += dx/ d * (r-d)
         return y_agent,x_agent   
                     
    def sprav(self, agent, action): 
        v,w = 0,0
        v,w = self.rychlosti(agent, action)
        y_agent,x_agent = self.integruj(agent, v,w)
        print(type(agent).__name__, agent.uhol_agent, action)
        y_agent,x_agent = self.vytlac_zo_steny(y_agent,x_agent,agent.polomer)
        if self.rozlozenie_prostredia[math.floor(y_agent)][math.floor(x_agent)] == 1:
           return
        
        agent.pozicia = (y_agent,x_agent)
        
        
        
                    
       
                              
        