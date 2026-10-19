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
        self.smer_otacania = None
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
    uhol_otocenia = math.pi
    zastavujuca_vzdialenost = 2
    vzdialenost_pokracuj = 4
    class Specialne_pohyby(Enum):
        Utok = 3
    def rozhodnutie(self, vysledok_pozorovania):
        
        stred = len(vysledok_pozorovania) // 2
        kod,vzdialenost = vysledok_pozorovania[stred]
        volno_vpredu = (kod == 0) or (vzdialenost > self.vzdialenost_pokracuj)
        blokada_vpredu = (kod == 1) and (vzdialenost < self.zastavujuca_vzdialenost)
        

        if self.smer_otacania is None:
            if not blokada_vpredu:
                return self.Pohyb.Dopredu.value

        def volne(z):
            return 100 if z[0] == 0 else z[1]
        vlavo = sum(volne(z) for z in vysledok_pozorovania[:stred])
        vpravo = sum(volne(z) for z in vysledok_pozorovania[stred +1:])
        if vlavo > vpravo:
            self.smer_otacania =  self.Pohyb.Dolava.value  
            return self.smer_otacania 
        else:
           self.smer_otacania = self.Pohyb.DoPrava.value 
           return self.smer_otacania


        if volno_vpredu:
            self.smer_otacania = None
            return self.Pohyb.Dopredu.value
        return self.smer_otacania       


           

       
#Specificky typ agenta - Korist      
class Korist(Agenti):
    trieda = 11
    zivot = True
    uhol_otocenia = math.pi
    zastavujuca_vzdialenost = 1
    vzdialenost_pokracuj = 4
    def rozhodnutie(self, vysledok_pozorovania):
        stred = len(vysledok_pozorovania) // 2
        kod,vzdialenost = vysledok_pozorovania[stred]
        volno_vpredu = (kod == 0) or (vzdialenost > self.vzdialenost_pokracuj)
        blokada_vpredu = (kod == 1) and (vzdialenost < self.zastavujuca_vzdialenost)
        print(stred)
        print(self.pozicia)
        print(self.uhol_agent)

        if self.smer_otacania is None:
            if not blokada_vpredu:
                return self.Pohyb.Dopredu.value

        def volne(z):
            return 100 if z[0] == 0 else z[1]
        vlavo = sum(volne(z) for z in vysledok_pozorovania[:stred])
        vpravo = sum(volne(z) for z in vysledok_pozorovania[stred +1:])
        if vlavo > vpravo:
            self.smer_otacania =  self.Pohyb.Dolava.value  
            return self.smer_otacania 
        else:
           self.smer_otacania = self.Pohyb.DoPrava.value 
           return self.smer_otacania


        if volno_vpredu:
            self.smer_otacania = None
            return self.Pohyb.Dopredu.value
        return self.smer_otacania       
  