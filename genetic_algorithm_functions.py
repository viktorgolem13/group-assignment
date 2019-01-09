from random import randint, random

def stvori_populaciju(velicina_populacije, broj_gena):

    return [[randint(0, 1) for i in range(broj_gena)] for j in range(velicina_populacije)]

def stvori_populaciju2(velicina_populacije, broj_gena, p_ones = 10**-4):

    populacija = []
    for i in range(velicina_populacije):
        tocka = []
        for j in range(broj_gena):
            r = random()
            if r < p_ones:
                tocka.append(1)
            else:
                tocka.append(0)

        populacija.append(tocka)

    return populacija

        
def krizanje(x, y):

    tocka_krizanja = randint(1, len(x) - 1)
    nova_tocka = []
    for i in range(tocka_krizanja):
        nova_tocka.append(x[i])

    for j in range(tocka_krizanja, len(y)):
        nova_tocka.append(y[j])

    return nova_tocka

def mutacija(populacija, p_mutacije):
    p_m_gena = p_mutacije / len(populacija[0])
    for x in populacija:
        for i in range(len(x)):
            r = random()
            if r < p_m_gena:
                x[i] = 1 - x[i]
    
    return populacija