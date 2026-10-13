from dataclasses import dataclass
import numpy as np
import math

#Urcuje vsetko, co maju kazdy jeden agent spolocne
class Agenti:
    def __init__(self, sur, uhol):
        self.energia = 10
        self.pozicia = sur
        self.uhol_agent = uhol 
    
    #Agenti budu vyuzivat tuto funkciu pre rozhodovanie na zaklade toho, co budu mat z funkcie range_agentov
    def rozhodnutie(self, vysledok_pozorovania):
        raise NotImplementedError

    def ratanie_delta_pozicie(self):
        dx=math.cos(self.uhol_agent) * 5
        dy=math.sin(self.uhol_agent) * 5    
        return dx,dy

#Specificky typ agenta - Lovec
class Lovec(Agenti):
    trieda =5
    zivot = True
    def rozhodnutie(self, vysledok_pozorovania):
            
            
        pass 

#Specificky typ agenta - Korist      
class Korist(Agenti):
    trieda = 11
    zivot = True
    def rozhodnutie(self, vysledok_pozorovania):
            
        pass