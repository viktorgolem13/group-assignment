from genetski_algoritam_binarne_funkcije import *
from time import time

#vraca sudionike
def moja_selekcija(populacija, broj_sudionika, p_faktor=None):
    if p_faktor == None:
        p_faktor = 1 - (1 / broj_sudionika)
    i = 0
    p = 1
    sudionici = []
    while len(sudionici) < broj_sudionika:
        r = random()
        if r < p:
            sudionici.append(populacija[i])
            i += 1
            p *= p_faktor

        if i == len(populacija):
            i = 0
            p = 1
    return sudionici

#vraca sudionike
def selekcija(populacija, broj_sudionika, elitizam):
    granice = []
    faktor = 2 / (len(populacija) * (len(populacija) + 1))
    for i in range(len(populacija)):
        if i == 0:
            granice.append((len(populacija) - i) * faktor)
        else:
            granice.append(granice[-1] + (len(populacija) - i) * faktor)

    sudionici = []
    for i in range(broj_sudionika):
        if elitizam and len(sudionici) == broj_sudionika - 1 and populacija[0] not in sudionici:
            sudionici.append(populacija[0])
            break
        r = random()
        for (j, granica) in enumerate(granice):
            if r <= granica:
                sudionici.append(populacija[j])
                break


    return sudionici


#f je funkcija koju minimiziramo
def generacijski_algoritam(f, velicina_populacije=50, p_mutacije=0.01, p_krizanja=0.5, broj_gena = 5, 
                                        broj_iteracija=10**3, epsilon=10**-4,  ispisuj=False, standardna_selekcija=True, elitizam=True):
    begining = time()
    populacija = stvori_populaciju2(velicina_populacije, broj_gena)
    print(time() - begining)
    for i in range(broj_iteracija):
        begining = time()
        populacija.sort(key=f)
        print('time1: ', time() - begining)
        if standardna_selekcija:
            nova_generacija = selekcija(populacija, int(p_krizanja * len(populacija)), elitizam)
        else:
            nova_generacija = moja_selekcija(populacija, int(p_krizanja * len(populacija))) #prominit da bude proporcionalno dobroti
        nova_populacija = []
        for x in nova_generacija:
            nova_populacija.append(x)

        populacija = nova_populacija
        nova_populacija = []

        while len(populacija) + len(nova_populacija) < velicina_populacije:
            r1 = randint(0, len(populacija) - 1)
            r2 = randint(0, len(populacija) - 1)
            if r1 != r2:
                novi = krizanje(populacija[r1], populacija[r2])
                nova_populacija.append(novi)
        mutacija(nova_populacija, p_mutacije)

        for x in nova_populacija:
            populacija.append(x)
        
        if  ispisuj and i % 100 == 0:
            print(f(populacija[0]))

        if epsilon and i % 100 == 0 and f(populacija[0]) < epsilon:
            return populacija[0], f(populacija[0])

        print('time2: ', time() - begining)
    najbolji = min(populacija, key=f)
    return najbolji, f(najbolji)

        