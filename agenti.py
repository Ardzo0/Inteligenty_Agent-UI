from dataclasses import dataclass
import numpy as np
import math
from enum import Enum

#Urcuje vsetko, co maju kazdy jeden agent spolocne
class Agenti:
    def __init__(self, sur, uhol):
        self.energia = 10
        self.pozicia = sur
        self.uhol_agent = uhol 
    class Pohyb(Enum):
        Dopredu = 8
        Dozadu = 7
        Dolava = 4
        DoPrava = 6
        Stop = 9

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
    zastavujuca_vzdialenost = 1
    vzdialenost_pokracuj = 3
    class Specialne_pohyby(Enum):
        Utok = 3
    def rozhodnutie(self, vysledok_pozorovania):
        stred = len(vysledok_pozorovania) // 2

        kod,vzdialenost = vysledok_pozorovania[stred]
        if not( kod == 1 and vzdialenost > self.zastavujuca_vzdialenost):
            return self.Pohyb.Dopredu.value

        najlepsi_ray=None
        for i, (kod,vzdialenost) in enumerate(vysledok_pozorovania):
            if vzdialenost > self.vzdialenost_pokracuj:
                if najlepsi_ray is None or abs(i - stred) < abs(najlepsi_ray - stred):
                    najlepsi_ray = i

        if najlepsi_ray is None:
            return self.Pohyb.DoPrava.value
        if najlepsi_ray < stred:
            return self.Pohyb.Dolava.value  
        return self.Pohyb.DoPrava    

            
            
    

#Specificky typ agenta - Korist      
class Korist(Agenti):
    trieda = 11
    zivot = True
    zastavujuca_vzdialenost = 1
    vzdialenost_pokracuj = 4
    def rozhodnutie(self, vysledok_pozorovania):
        stred = len(vysledok_pozorovania) // 2
        kod,vzdialenost = vysledok_pozorovania[stred]
        if not( kod == 1 and vzdialenost > self.zastavujuca_vzdialenost):
            return self.Pohyb.Dopredu.value

        najlepsi_ray=None
        for i, (kod,vzdialenost) in enumerate(vysledok_pozorovania):
            if vzdialenost > self.vzdialenost_pokracuj:
                if najlepsi_ray is None or abs(i - stred) < abs(najlepsi_ray - stred):
                    najlepsi_ray = i

        if najlepsi_ray is None:
            return self.Pohyb.DoPrava.value
        if najlepsi_ray < stred:
            return self.Pohyb.Dolava.value  
        return self.Pohyb.DoPrava        
        