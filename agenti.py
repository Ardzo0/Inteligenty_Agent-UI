from dataclasses import dataclass
import numpy as np
from simulacne_prostredie import Prostredie


class Agenti:
    def __init__(self, sur):
        self.energia = 10
        self.pozicia = sur
    pass

    def rozhodnutie(self, vysledok_pozorovania):
        raise NotImplementedError
        pass


class Lovec(Agenti):
    trieda =1
    zivot = True
    def rozhodnutie(self, vysledok_pozorovania):
            
            
        pass 
      
class Korist(Agenti):
    trieda = 2
    zivot = True
    def rozhodnutie(self, vysledok_pozorovania):
            
        pass