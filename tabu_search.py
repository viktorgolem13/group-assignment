import tabu_search_utils as tsu
from collections import deque


def tabu_search(f, neighborhood_size=50, tabu_tenure=3, solution_size=5, no_of_iterations=10 ** 4, print_progress=True):
    """f is the function which we're minimizing"""

    def make_f_index(f, populacija):
        def f_index_(i):
            return f(populacija[i])
        return f_index_

    if tabu_tenure > neighborhood_size or tabu_tenure < 3:
        return

    s = tsu.initial_solution(solution_size, p_ones=10**-4)
    s_best = s
    s_best_f = f(s_best)
    tabu_list = deque(maxlen=tabu_tenure)

    s_index = 0

    # TODO Initialize aspiration criterion (AC)
    # TODO Initialize other memory structures(e.g. long -term) if any;

    for i in range(no_of_iterations):

        N = tsu.create_neighborhood_subset(s, tabu_list, last_chosen_s=s_index, subset_size=neighborhood_size,
                                                    aspiration_crit=None)         # neighborhood subject to tabu
                                                                                  # list and aspiration criterion
        f_index = make_f_index(f, N)

        s_new, s_new_f, s_index = tsu.find_new_solution_subset(N, f_index, f)

        s = s_new
        if s_new_f < s_best_f:
            s_best = s
            s_best_f = s_new_f

        tsu.update_tabu_list(tabu_list, s, tabu_tenure)

        # TODO Update aspiration criterion, other memory structures
        # TODO If intesification or diversification criterion, then intesify or diversify search;

        if print_progress and i % 1000 == 0:
            print('> Iteration: {} - best score: {}'.format(i, s_best_f))

    return s_best, s_best_f
