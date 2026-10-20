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
        Pravo_chod = 12
        Lavo_chod = 13

    #Agenti budu vyuzivat tuto funkciu pre rozhodovanie na zaklade toho, co budu mat z funkcie range_agentov
    def rozhodnutie(self, vysledok_pozorovania):
        raise NotImplementedError

    def ratanie_delta_pozicie(self):
        dx=math.cos(self.uhol_agent) * 5
        dy=math.sin(self.uhol_agent) * 5    
        return dx,dy

#Specificky typ agenta - Lovec
class Lovec(Agenti):
    uhol_krok = 10
    trieda =5
    zivot = True
    uhol_otocenia = math.pi/2
    zastavujuca_vzdialenost = 1
    vzdialenost_pokracuj = 4
    class Specialne_pohyby(Enum):
        Utok = 3
    def rozhodnutie(self, vysledok_pozorovania):
        #prvy_luc, posledny_luc = 0, -1

        stred = len(vysledok_pozorovania) // 2
        kod,vzdialenost = vysledok_pozorovania[stred]
        kod_vpravo,vzdialenost_vpravo = vysledok_pozorovania[-1]
        kod_vlavo,vzdialenost_vlavo = vysledok_pozorovania[0]
        volno_vpredu = (kod == 0) or (vzdialenost > self.vzdialenost_pokracuj)
        blokada_vpredu = (kod == 1) and (vzdialenost < self.zastavujuca_vzdialenost)
        moznosti=[self.Pohyb.Pravo_chod.value]
        zvolena_moznost= np.random.choice(moznosti)


        def volne(z):
            return 100 if z[0] == 0 else z[1]


        if kod_vpravo == kod_vlavo and vzdialenost_vpravo == vzdialenost_vlavo and not blokada_vpredu:
                        self.smer_otacania = self.Pohyb.Dolava.value
                        print("Krizovatka")
                        print("Vlavo_kod:" ,kod_vlavo,"Vpravo_kod: ",kod_vpravo)
                        print(vzdialenost_vlavo,"<--Vlavo",vzdialenost_vpravo,"<----Vpravo")
                        return zvolena_moznost
        
        if self.smer_otacania is None:
            if not blokada_vpredu:
                print("Pred")
                return self.Pohyb.Dopredu.value
                
            
            vlavo = sum(volne(z) for z in vysledok_pozorovania[:stred])
            vpravo = sum(volne(z) for z in vysledok_pozorovania[stred +1:])
            
            if vlavo > vpravo:
                self.smer_otacania =  self.Pohyb.Dolava.value  
            else:
               self.smer_otacania = self.Pohyb.DoPrava.value 
            return self.smer_otacania


        if volno_vpredu:
            self.smer_otacania = None
            return self.Pohyb.Dopredu.value
        return self.smer_otacania       


           

       
#Specificky typ agenta - Korist      
class Korist(Agenti):
    uhol_krok = 10
    trieda = 11
    zivot = True
    uhol_otocenia = math.pi/2
    zastavujuca_vzdialenost = 1
    vzdialenost_pokracuj = 4
    def rozhodnutie(self, vysledok_pozorovania):
        stred = len(vysledok_pozorovania) // 2
        kod,vzdialenost = vysledok_pozorovania[stred]
        volno_vpredu = (kod == 0) or (vzdialenost > self.vzdialenost_pokracuj)
        blokada_vpredu = (kod == 1) and (vzdialenost < self.zastavujuca_vzdialenost)
        


        def volne(z):
            return 100 if z[0] == 0 else z[1]
        
        if self.smer_otacania is None:
            if not blokada_vpredu:
                return self.Pohyb.Dopredu.value

        
            vlavo = sum(volne(z) for z in vysledok_pozorovania[:stred])
            vpravo = sum(volne(z) for z in vysledok_pozorovania[stred +1:])
            if vlavo > vpravo:
                self.smer_otacania =  self.Pohyb.Dolava.value  
                
            else:
                self.smer_otacania = self.Pohyb.DoPrava.value 
            return self.smer_otacania


        if volno_vpredu:
            self.smer_otacania = None
            return self.Pohyb.Dopredu.value
        return self.smer_otacania       
  