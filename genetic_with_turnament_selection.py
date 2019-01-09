from genetski_algoritam_binarne_funkcije import *

#vraca indekse sudionika
def izaberi_sudionike(velicina_populacije, k):
    j = 0
    sudionici = []
    while j < k:
        r = randint(0, velicina_populacije - 1)
        if r not in sudionici:
            sudionici.append(r)
            j += 1
    return sudionici

#f je funkcija koju minimiziramo
def k_turnirski_algoritam(f, velicina_populacije=50, p_mutacije=0.01, k=3, broj_gena = 5, min_element=-4, max_element=4, 
                                                                        broj_iteracija=10**4, epsilon=10**-4, ispisuj=False):

    def napravi_f_index(f, populacija):
        def f_index_(i):
            return f(populacija[i])

        return f_index_

    if k > velicina_populacije or k < 3:
        return

    populacija = stvori_populaciju2(velicina_populacije, broj_gena)

    for i in range(broj_iteracija):
        f_index = napravi_f_index(f, populacija)
        sudionici = izaberi_sudionike(velicina_populacije, k)
        najgori = max(sudionici, key = f_index)

        if k == 3:
            prvi, drugi = [populacija[sudionik] for sudionik in sudionici if sudionik != najgori]
        else:
            prvi, drugi = izaberi_sudionike(k, 2)
            while prvi == najgori or drugi == najgori:
                prvi, drugi = izaberi_sudionike(k, 2)

        novi = krizanje(prvi, drugi)
        novi = mutacija([novi], p_mutacije)[0]
        populacija[najgori] = novi

        if ispisuj and i % 1000 == 0:
            najbolji = min(populacija, key=f)
            print(f(najbolji))

        if epsilon and i % 1000 == 0 and f(populacija[0]) < epsilon:
            najbolji = min(populacija, key=f)
            return najbolji, f(najbolji)

    najbolji = min(populacija, key=f)
    return najbolji, f(najbolji)

        