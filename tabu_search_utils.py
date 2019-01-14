from random import randint, random


def initial_solution(size, p_ones=10**-4):

    value = []
    for j in range(size):
        r = random()
        if r < p_ones:
            value.append(1)
        else:
            value.append(0)

    return value


def create_neighborhood(s, tabu_list, aspiration_crit=None):

    neighb = []

    for i in range(len(s)):
        new_s = s.copy()
        new_s[i] = 1 - s[i]

        if new_s not in tabu_list:
            neighb.append(new_s)

        else:
            neighb.append(None)

    return neighb


def find_new_solution(N, f_index, f):

    best = min(N, key=f)
    return best, f(best)


def update_tabu_list(tabu_list, s, tabu_tenure):

    if len(tabu_list) >= tabu_tenure:
        tabu_list.pop()

    tabu_list.appendleft(s)
