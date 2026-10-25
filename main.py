from simulacne_prostredie import Parametre, Prostredie
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as pltm
import agenti
import math
np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=300)



parametre = Parametre(sirka =25, vyska=25, n_lovec=1, n_obet=0, seed=np.random.seed())
prostredie = Prostredie(parametre)


kopia = prostredie.rozlozenie_prostredia.copy()#Kopia, render_agentov až po obrázok obsahuje väčšiu aktivitu AI. Forma vysvetlovaňia a debugging 
def render_agentov(prostredie):
    pozicie = []
    triedy = []
    
    for agent in prostredie.agents:
            if agent.zivot:
                pos_y,pos_x = agent.pozicia
                pltm.patches.Circle(agent.polomer)
                pozicie.append([pos_x-0.5,pos_y-0.5])
                triedy.append(agent.trieda)

    return np.array(pozicie),np.array(triedy)


pozicie, triedy = render_agentov(prostredie)
plt.ion()
fig, ax = plt.subplots()

obrazok_prostredai = ax.imshow(prostredie.rozlozenie_prostredia, cmap="gray_r", vmin=0, vmax=11)
obrazok = ax.scatter(pozicie[:,0], pozicie[:,1], c = triedy, vmin=0, vmax=11)

while plt.fignum_exists(fig.number):
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
    
    



          
    
    
    