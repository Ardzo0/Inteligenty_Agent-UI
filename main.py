from simulacne_prostredie import Parametre, Prostredie
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=300)

parametre = Parametre(sirka =25, vyska=25, n_lovec=1, n_obet=1, seed=1,)
prostredie = Prostredie(parametre)

for _ in range(1):
    
    for agent in prostredie.agents:
            rozhodovanie = Prostredie.range_agentov(prostredie,agent)
            print(rozhodovanie)

    
    plt.imshow(prostredie.rozlozenie_prostredia, cmap="gray",interpolation="nearest")
    plt.colorbar()
    plt.title("50x50")
    plt.show()
    
    
    
    
    
    