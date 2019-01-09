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
