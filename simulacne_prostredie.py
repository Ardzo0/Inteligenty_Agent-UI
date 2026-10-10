from dataclasses import dataclass
import agenti 

import numpy as np

@dataclass
class Parametre:
    sirka:int 
    vyska: int 
    n_lovec: int 
    n_obet: int 
    seed: int 

class Prostredie:
    def __init__(self, parametre: Parametre):
        self.parametre = parametre
        self.generator_nahodnych_cisiel = np.random.default_rng(parametre.seed)
        self.tick = 0
        self.agent =[]
        self.reset(self)
        pass
    
    def reset(self):
        self.rozlozenie_prostredia = np.zeros((self.parametre.vyska, self.parametre.sirka), dtype=int)
        self.rozlozenie_prostredia[0,:] = 1
        self.rozlozenie_prostredia[49,:] = 1
        self.rozlozenie_prostredia[:,0] = 1
        self.rozlozenie_prostredia[:,49] = 1
        self.rozlozenie_prostredia[2,2:] =1
        
        self.tick = 0
        np.zeros(self.agents)
        self.generator_nahodnych_cisiel = np.random.default_rng(self.parametre.seed)
        pass
    
    def vision(self,Agenti):
        visible=[]
        for n in self.agent:
            if Lovec.trieda == 1:
               
            if Koristc.trieda ==2:
                #TODO Napisat fog of war visiu resp kruhovu

        
        pass
    def pozorovanie(self,agent):
        
        pass
    def krok(self):
        
        
        pass
    def sprav(self, agent, action):
        
        pass