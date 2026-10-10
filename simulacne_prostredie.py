from dataclasses import dataclass
import agenti 
import numpy as np

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
        for n in self.agent:
            if agenti.Lovec.trieda == 5:
                #TODO napisat ray v tvare kuzelu
                pass
               
            if agenti.Koristc.trieda ==11:
                #TODO Napisat ray v tvare kruhu
                pass

        
        pass

    #TODO Napisat, funkcia funguje ako server resp. ak mate serverovy anticheat tak ten server musi za urcity cyklus vykonat predpisane funkcie:range_agentov, rozhodnutie agentov a skontrolovanie agentov.
    # tick je hodnota kolko krat
    def krok(self):
        
        
        pass
    #TODO Napisat, v tejto funkci su definovane pravidla ako 1 = stena, 0 = prazne, 2 = jedlo..., a rozhoduje, ci vyber agenta je legalny, a ak je aplikuje ho
    def sprav(self, agent, action):
        
        pass