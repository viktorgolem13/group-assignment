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


def create_neighborhood_subset(s, tabu_list, last_chosen_s, subset_size,
                                                    aspiration_crit=None):
    neighb = []

    if round(last_chosen_s - subset_size/2) <= 0:          # subset bound calculation
        lower_bound = 0
        upper_bound = subset_size
    elif round(last_chosen_s + subset_size/2) >= len(s):
        lower_bound = len(s) - subset_size
        upper_bound = len(s)
    else:
        lower_bound = round(last_chosen_s - subset_size/2)
        upper_bound = round(last_chosen_s + subset_size/2)

    for i in range(lower_bound, upper_bound):
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


def find_new_solution_subset(N, f_index, f):

    best = min(N, key=f)
    return best, f(best), N.index(best)


def update_tabu_list(tabu_list, s, tabu_tenure):

    if len(tabu_list) >= tabu_tenure:
        tabu_list.pop()

    tabu_list.appendleft(s)
