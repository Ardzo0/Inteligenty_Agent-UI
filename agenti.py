from dataclasses import dataclass
import numpy as np
import math
from enum import Enum

#Určuje všetko, čo má každý agent spoločné
class Agenti:
    vzdialenost_ignorovania_kriz = 1.5
    def __init__(self, sur, uhol):
        self.energia = 10
        self.pozicia = sur
        self.uhol_agent = uhol 
        self.smer_otacania = None
        self.polomer = 0.3
        self.v_max = 0.1
        self.w_max = math.radians(11)
        self.w_obluk = math.radians(11)
        self.cielovy_uhol = None
        self.miesto_konca = None
    class Pohyb(Enum):#Zoznám pohybov a ich "kódov"
        Dopredu = 8
        OtocenieKUhlu=10
    
    def rozhodnutie(self, vysledok_pozorovania):
        raise NotImplementedError

    def chyba_uhla(self):
        return (self.cielovy_uhol - self.uhol_agent + math.pi) % (2 * math.pi) - math.pi
    
    def zatocenie(self,posun):
        kvadrant = round(self.uhol_agent/ (math.pi/2))#Svetová strana Kvadrant 0 má uhol a na obrázovke ide doprava
        #1 má uhol pi/2 a na obrázovke ide dole, 2 má uhol pi a na obrázovke ide doľava, 3 má uhol 3pi/2 a na obrázovke hore
        self.cielovy_uhol = ((kvadrant + posun) % 4) * math.pi/2
        return self.Pohyb.OtocenieKUhlu.value
    def vyber(self, posuny):
        posun = int(np.random.choice(posuny))
        if posun == 0:
            self.miesto_konca == self.pozicia
            return self.Pohyb.Dopredu.value
        return self.zatocenie(posun)
#Specificky typ agenta - Lovec
class Lovec(Agenti):
    trieda =5
    zivot = True
    uhol_otocenia = math.pi/2
    zastavujuca_vzdialenost = 0.4
    vzdialenost_pokracuj = 1.7
    prah_bok = 0.7
    class Specialne_pohyby(Enum):
        Utok = 3
    
    def rozhodnutie(self, vysledok_pozorovania):#Táto funkcia obsahuje väčšiu aktivitu AI, ako ostatné 
        
        if self.cielovy_uhol is not None:
            if abs(self.chyba_uhla()) < 1e-6:
                self.cielovy_uhol = None
                self.miesto_konca = self.pozicia
                return self.Pohyb.Dopredu.value
            return self.Pohyb.OtocenieKUhlu.value
        
        prvy_luc, posledny_luc = 0, -1

        stred = len(vysledok_pozorovania) // 2
        kod,vzdialenost = vysledok_pozorovania[stred]
        kod_vpravo,vzdialenost_vpravo = vysledok_pozorovania[posledny_luc]
        kod_vlavo,vzdialenost_vlavo = vysledok_pozorovania[prvy_luc]
        
        
        volno_vpredu = (kod == 0) or (vzdialenost > self.vzdialenost_pokracuj)
        blokada_vpredu = (kod == 1) and (vzdialenost < self.zastavujuca_vzdialenost)
        volno_vpravo = (kod_vpravo == 0) or (vzdialenost_vpravo > self.prah_bok)
        volno_vlavo = (kod_vlavo == 0) or (vzdialenost_vlavo > self.prah_bok)
        
        if self.miesto_konca is not None:
            delta_y = self.pozicia[0] - self.miesto_konca[0]
            delta_x = self.pozicia[1] - self.miesto_konca[1]
            if delta_y **2 + delta_x **2 > self.vzdialenost_ignorovania_kriz **2:
                self.miesto_konca = None
            elif not blokada_vpredu:
                return self.Pohyb.Dopredu.value

        if volno_vpredu:
            if volno_vpravo and volno_vlavo:
                y,x = self.pozicia
                y_agent = math.floor(y)
                x_agent = math.floor(x)
                y_agent +=0.5
                x_agent +=0.5 
                self.pozicia =((y_agent),(x_agent))
                return self.vyber([0, +1, -1])
            if  volno_vlavo and not volno_vpravo:
                y,x = self.pozicia
                y_agent = math.floor(y)
                x_agent = math.floor(x)
                y_agent +=0.5
                x_agent +=0.5  
                self.pozicia =((y_agent),(x_agent))
                return self.zatocenie(-1)
            if  volno_vpravo and not volno_vlavo:
                y,x = self.pozicia
                y_agent = math.floor(y)
                x_agent = math.floor(x)
                y_agent +=0.5
                x_agent +=0.5 
                self.pozicia =((y_agent),(x_agent))
                return self.zatocenie(+1)
       
        if blokada_vpredu:
            if volno_vlavo and volno_vpravo:
                y,x = self.pozicia
                y_agent = math.floor(y)
                x_agent = math.floor(x)
                y_agent +=0.5
                x_agent +=0.5  
                self.pozicia =((y_agent),(x_agent))
                return self.vyber([+1,-1])
            if volno_vpravo:
                y,x = self.pozicia
                y_agent = math.floor(y)
                x_agent = math.floor(x)
                y_agent +=0.5
                x_agent +=0.5 
                  
                self.pozicia =((y_agent),(x_agent))
                return self.zatocenie(+1)
            if volno_vlavo:
                y,x = self.pozicia
                y_agent = math.floor(y)
                x_agent = math.floor(x)
                y_agent +=0.5
                x_agent +=0.5 
                   
                self.pozicia =((y_agent),(x_agent))
                return self.zatocenie(-1)
            return self.zatocenie(+2)
        return self.Pohyb.Dopredu.value
    
       
     
#Specificky typ agenta - Korist      
class Korist(Agenti):
    
    trieda = 11
    zivot = True
    uhol_otocenia = math.pi/2
    zastavujuca_vzdialenost = 1
    vzdialenost_pokracuj = 4
    prah_bok = 0.7
    uhol_otocenia = math.pi/2

    def rozhodnutie(self, vysledok_pozorovania):
        if self.cielovy_uhol is not None:
            if abs(self.chyba_uhla()) < 1e-6:
                self.cielovy_uhol = None
                self.miesto_konca = self.pozicia
                return self.Pohyb.Dopredu.value
            return self.Pohyb.OtocenieKUhlu.value
                
        prvy_luc, posledny_luc = 0, -1  
        stred = len(vysledok_pozorovania) // 2
        kod,vzdialenost = vysledok_pozorovania[stred]
        kod_vpravo,vzdialenost_vpravo = vysledok_pozorovania[posledny_luc]
        kod_vlavo,vzdialenost_vlavo = vysledok_pozorovania[prvy_luc]


        volno_vpredu = (kod == 0) or (vzdialenost > self.vzdialenost_pokracuj)
        blokada_vpredu = (kod == 1) and (vzdialenost < self.zastavujuca_vzdialenost)
        volno_vpravo = (kod_vpravo == 0) or (vzdialenost_vpravo > self.prah_bok)
        volno_vlavo = (kod_vlavo == 0) or (vzdialenost_vlavo > self.prah_bok)

        if self.miesto_konca is not None:
            delta_y = self.pozicia[0] - self.miesto_konca[0]
            delta_x = self.pozicia[1] - self.miesto_konca[1]
            if delta_y **2 + delta_x **2 > self.vzdialenost_ignorovania_kriz **2:
                self.miesto_konca = None
            elif not blokada_vpredu:
                return self.Pohyb.Dopredu.value 
        if volno_vpredu and volno_vpravo and volno_vlavo:
            return self.vyber([0, +1, -1])
        if volno_vpredu and volno_vlavo:
            return self.zatocenie(-1)
        if volno_vpredu and volno_vpravo:
            return self.zatocenie(+1)
        if blokada_vpredu:
            if volno_vlavo and volno_vpravo:
                return self.vyber([+1,-1])
            if volno_vpravo:
                return self.zatocenie(+1)
            if volno_vlavo:
                return self.zatocenie(-1)
            return self.zatocenie(+2)
        return self.Pohyb.Dopredu.value     