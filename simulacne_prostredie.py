from dataclasses import dataclass
import agenti 
import numpy as np
import math

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
    
    def reset(self):
        
        #Vytvaranie Prostredia s grid tematikou 
        self.rozlozenie_prostredia = np.zeros((self.parametre.vyska, self.parametre.sirka), dtype=int)
        self.rozlozenie_prostredia[0,:] = 1
        self.rozlozenie_prostredia[49,:] = 1
        self.rozlozenie_prostredia[:,0] = 1
        self.rozlozenie_prostredia[:,49] = 1
        self.rozlozenie_prostredia[2,2:] =1

        self.tick = 0
        
        #Snaha o generator a nahodnu volbu pre hunterov a koristi
        self.generator_nahodnych_cisiel = np.random.default_rng(self.parametre.seed)
        pocet_agentov = self.pocet_lovec + self.pocet_obet
        nulove_polia = np.argwhere(self.rozlozenie_prostredia == 0)
        indexy_buniek = self.generator_nahodnych_cisiel.choice(len(nulove_polia),pocet_agentov,False)

        for poradie,indexy in enumerate(indexy_buniek):
            pozicia = tuple(nulove_polia[indexy].tolist())
            if poradie < self.pocet_lovec:
                self.agents.append(agenti.Lovec(pozicia))
            else:
                self.agents.append(agenti.Korist(pozicia))
            
    #TODO Nejak vymysliet, aby agenti mohli otacat ich viziu
    def range_agentov(self,agentus_manus):
        visible=[]
        for n in self.agents:
            if isinstance(agentus_manus,agenti.Lovec):
                pocet_rays = 5
                y_agent,x_agent = agentus_manus.pozicia
                y_agent = y_agent +0.5
                x_agent = x_agent +0.5
                uhol = agentus_manus.uhol_agenta   
                dof,bunka_x, bunka_y, ray_x, ray_y, uhol_luca, y_offset, x_offset, final_distance, pomocne_oznacenie_h,pomocne_oznacenie_v, oznacenie
                distH = 1000000
                hx=x_agent
                hy=y_agent
                distV = 1000000
                vx=x_agent
                vy=y_agent
               
                fov = math.radians(90)
                for i in range(pocet_rays):
                    
                    if pocet_rays == 1:
                            offset = 0
                    else:
                        offset = -fov / 2 + 1 * fov / (pocet_rays - 1)

                        uhol_luca = uhol + offset
                        delta_y = math.sin(uhol_luca)
                        delta_x = math.sin(uhol_luca)   
                     
                    #Horizontalne luce  
                    if delta_y < 0: #Pozeranie hore
                        ray_y = math.floor(y_agent) - 0.001
                        ray_x = (y_agent - ray_y )*(-delta_x/delta_y)+x_agent
                        y_offset = -1
                        x_offset =-y_offset*(-delta_x/delta_y)
                        
                    if delta_y > 0: #Pozeranie dole
                        ray_y = math.floor(y_agent) - 1
                        ray_x = (y_agent - ray_y )*(-delta_x/delta_y)+x_agent
                        y_offset = 1
                        x_offset =y_offset*(-delta_x/delta_y)
                        
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
                        
                        #Vertikalne luce
                        if delta_x < 0: #Pozeranie vlavo
                            ray_x = math.floor(x_agent) - 0.001
                            ray_y = (y_agent - ray_y )*(-delta_y/delta_x)+y_agent
                            x_offset = -1
                            y_offset =-x_offset*(-delta_y/delta_x)
                                                
                        if delta_x > 0: #Pozeranie vpravo
                            ray_x = math.floor(x_agent) - 1
                            ray_y = (y_agent - ray_y )*(-delta_y/delta_x)+y_agent
                            x_offset = 1
                            y_offset =x_offset*(-delta_y/delta_x)
                                                
                        if delta_y == 0: #Pozeranie hore, dole
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
                                distV = math.sqrt((hx-x_agent)*(hx-x_agent)+(hy-y_agent)*(hy-y_agent))
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
                        if distH <distV:
                            ray_x=hx
                            ray_y=hy    
                            final_distance = distH
                            oznacenie = pomocne_oznacenie_h
                        if final_distance > dof:
                            oznacenie =0
                            final_distance = dof
                        visible.append((oznacenie,final_distance))   
                            
                            #https://www.youtube.com/watch?v=gYRrGTC7GtA&t=376s tutorial, pri nechapani bola vyuzita AI
        


        for n in self.agents:
            if isinstance(agentus_manus,agenti.Korist):
                y,x = agentus_manus.pozicia
                pass
        pass
        
        
        
        return visible

    #TODO Napisat, funkcia funguje ako server resp. ak mate serverovy anticheat tak ten server musi za urcity cyklus vykonat predpisane funkcie:range_agentov, rozhodnutie agentov a skontrolovanie agentov.
    # tick je hodnota kolko krat
    def krok(self):
        
        
        pass
    #TODO Napisat, v tejto funkci su definovane pravidla ako 1 = stena, 0 = prazdne, 2 = jedlo..., a rozhoduje, ci vyber agenta je legalny, a ak je aplikuje ho
    def sprav(self, agent, action):
        
        pass