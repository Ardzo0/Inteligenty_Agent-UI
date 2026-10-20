from simulacne_prostredie import Parametre, Prostredie
import numpy as np
import matplotlib.pyplot as plt
import agenti
import math
np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=300)



parametre = Parametre(sirka =50, vyska=50, n_lovec=1, n_obet=0, seed=np.random.seed())
prostredie = Prostredie(parametre)


kopia = prostredie.rozlozenie_prostredia.copy()
def render_agentov(prostredie):
    pozicie = []
    triedy = []
    
    for agent in prostredie.agents:
            if agent.zivot:
                pos_y,pos_x = agent.pozicia
                
                pozicie.append([pos_x-0.5,pos_y-0.5])
                triedy.append(agent.trieda)

    return np.array(pozicie),np.array(triedy)


pozicie, triedy = render_agentov(prostredie)
plt.ion()
fig, ax = plt.subplots()

obrazok_prostredai = ax.imshow(prostredie.rozlozenie_prostredia, cmap="gray_r", vmin=0, vmax=11)
obrazok = ax.scatter(pozicie[:,0], pozicie[:,1], c = triedy, vmin=0, vmax=11)

for _ in range(1000):
    prostredie.krok()
    pozicie, triedy = render_agentov(prostredie)
    obrazok_prostredai.set_array(kopia)
    obrazok.set_offsets(pozicie)
    obrazok.set_array(triedy)
    plt.pause(0.05)
    if not plt.fignum_exists(fig.number):
         break    

    
plt.ioff()    
plt.show()
    
    



          
    
    
    