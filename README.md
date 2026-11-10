Projekt obsahuje bludisko, dva typy agentov a 5 vstupných parametrov(môže ich byť v buducnosti viac). Cieľom je spraviť funkčné pohyby agentov a ich chovanie s prepojením krátko dobej a dlhodobej pamäte.

POZNAMKY K ROZBEHANIU PROSTREDIA PRE SPUSTENIE PROGRAMU. 
- Python 3.14 
- knižnica mazelib-alt
- úprava AppData\Local\Programs\Python\Python314\Lib\site-packages\mazelib\generate\Ellers.py
  ===> potrebne zmenit riadok 34 z 
sets = np.empty((self.H, self.W), dtype=np.int8) na sets = np.empty((self.H, self.W), dtype=np.int32) Poznamka mneviem, či nejde použiť aj int to by malo byť predvolene 32 bit treba otestovať toto tvrdenie.

Rozdelenie prace na dokončenie:
Grafy a značenie môžeme spoločne. 
Jakub: Lovec špecifické spravanie.
Vlado: Lovec špecifické spravanie.
Lukáš: Všeobecné pravidlo dvoch rovnakých polí, korisť špecifické spravanie.  
Peťo: Krátkodoba, dlhodoba pamäť a učenie.  


