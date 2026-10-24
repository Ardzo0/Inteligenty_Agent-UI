from dataclasses import dataclass
import numpy as np
import math
from enum import Enum

#Určuje všetko, čo má každý agent spoločné
class Agenti:
    def __init__(self, sur, uhol):
        self.energia = 10
        self.pozicia = sur
        self.uhol_agent = uhol 
        self.smer_otacania = None
        self.polomer = 0.3
        self.v_max = 0.1
        self.w_max = math.radians(11)
        self.w_obluk = math.radians(11)
    class Pohyb(Enum):#Zoznám pohybov a ich "kódov"
        Dopredu = 8
        Dozadu = 7
        Dolava = 4
        DoPrava = 6
        Stop = 9
        Pravo_chod = 12
        Lavo_chod = 13
    
    def rozhodnutie(self, vysledok_pozorovania):
        raise NotImplementedError

    

#Specificky typ agenta - Lovec
class Lovec(Agenti):
    trieda =5
    zivot = True
    uhol_otocenia = math.pi/2
    zastavujuca_vzdialenost = 1.2
    vzdialenost_pokracuj = 1.7
    class Specialne_pohyby(Enum):
        Utok = 3
    def chyba_uhla(self):
                return (self.Cielovy_uhol - self.uhol_agent + math.pi) % (2 * math.pi) - math.pi    
    def rozhodnutie(self, vysledok_pozorovania):#Táto funkcia obsahuje väčšiu aktivitu AI, ako ostatné 
        prvy_luc, posledny_luc = 0, -1

        stred = len(vysledok_pozorovania) // 2
        kod,vzdialenost = vysledok_pozorovania[stred]
        kod_vpravo,vzdialenost_vpravo = vysledok_pozorovania[0]
        kod_vlavo,vzdialenost_vlavo = vysledok_pozorovania[-1]
        volno_vpredu = (kod == 0) or (vzdialenost > self.vzdialenost_pokracuj)
        blokada_vpredu = (kod == 1) and (vzdialenost < self.zastavujuca_vzdialenost)
        volno_vpravo = (kod == 0) or (vzdialenost_vpravo > self.vzdialenost_pokracuj)
        volno_vlavo = (kod == 0) or (vzdialenost_vlavo > self.vzdialenost_pokracuj)
        blokda_vpravo = (kod == 1) and (vzdialenost_vpravo < self.zastavujuca_vzdialenost)
        blokada_vlavo = (kod == 1) and (vzdialenost_vlavo < self.zastavujuca_vzdialenost)
        moznosti=[self.Pohyb.DoPrava.value,self.Pohyb.Dolava.value,self.Pohyb.Dopredu.value]#Zoznám možnosti, čo môže spraviť agent na križovatke Rovno, Pravo a ľavo. Zatial len pre testy Práva strana, ale toto bude tiež do nejakej miery náhradené krátko dobou a dlhodobou pamôťou
        zvolena_moznost= np.random.choice(moznosti)#Generátor, ktorý bude vyberať medzi nimi 
 

        def volne(z):
            return 100 if z[0] == 0 else z[1]


        if volno_vpredu  and (kod_vlavo and kod_vpravo)==0: #Funguje !!!!!!!!! 
            self.smer_otacania = zvolena_moznost
            return self.smer_otacania    
            
        #if blokada_vpredu:
        #    if volno_vlavo and volno_vpravo:
        #        self.smer_otacania = self.Pohyb.DoPrava.value
        #        return self.smer_otacania
        #    if volno_vpravo:
        #        self.smer_otacania = self.Pohyb.DoPrava.value
        #        return self.smer_otacania
        #    if volno_vlavo:
        #        self.smer_otacania = self.Pohyb.Dolava.value
        #        return self.smer_otacania
        
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
  