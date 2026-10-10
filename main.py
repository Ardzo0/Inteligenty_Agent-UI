from simulacne_prostredie import Parametre, Prostredie


parametre = Parametre(sirka =50, vyska=50, n_lovec=2, n_obet=10, seed=1)
prostredie = Prostredie(parametre)

for _ in range(100):
    
    #print(prostredie.tick)
    print(prostredie.rozlozenie_prostredia)