import pandas as pd
#  from genetic_agorithm import *
from genetic_with_turnament_selection import *


def score_A(df_students):
    score = 0
    for _, student in df_students.iterrows():
        if student['new_group_id'] != 0:
            score += student['swap_weight']

    return score


def score_B(df_students, award_activity):
    students_swaped = dict()
    for _, student in df_students.iterrows():
        if student['new_group_id'] != 0:
            if student['student_id'] in students_swaped:
                students_swaped[student['student_id']] += 1
            else:
                students_swaped[student['student_id']] = 1

    score = 0
    for _, value in students_swaped.items():
        try:
            score += award_activity[value - 1] #index 0 is for 1 swap
        except IndexError:
            score += award_activity[-1]

    return score


def score_C(df_students, student_award):
    students_not_swaped = set()
    diff_students = set()
    for _, student in df_students.iterrows():
        diff_students.add(student['new_group_id'])
        if student['new_group_id'] == 0:
            students_not_swaped.add(student['new_group_id'])

    num_swaped_students = len(diff_students) - len(students_not_swaped)
    return student_award * num_swaped_students


def score_D(df_students, df_limits, minmax_penalty):
    group_count = get_group_change_count(df_students)
    score = 0
    for group_id, change in group_count.items():
        for _, group in df_limits.iterrows():
            if group['group_id'] == group_id:
                count = change + group['students_cnt'] 
                if count < group['min_preferred']:
                    score += (group['min_preferred'] - count) * minmax_penalty

    return score


def score_E(df_students, df_limits, minmax_penalty):
    group_count = get_group_change_count(df_students)
    score = 0
    for group_id, change in group_count.items():
        for _, group in df_limits.iterrows():
            if group['group_id'] == group_id:
                count = change + group['students_cnt'] 
                if count > group['max_preferred']:
                    score += (count - group['max_preferred']) * minmax_penalty

    return score


def get_group_change_count(df_students):
    group_count = dict()
    for _, student in df_students.iterrows():
        if student['new_group_id'] != 0:

            if student['new_group_id'] in group_count:
                group_count[student['new_group_id']] += 1
            else:
                group_count[student['new_group_id']] = 1

            if student['group_id'] in group_count:
                group_count[student['group_id']] -= 1
            else:
                group_count[student['group_id']] = -1

    return group_count


def valid_student_count(df_students, df_limits):
    group_count = get_group_change_count(df_students)
    for group_id, change in group_count.items():
        for _, group in df_limits.iterrows():
            if group['group_id'] == group_id:
                count = change + group['students_cnt'] 
                if count > group['max'] or count < group['min']:
                    return False
    print('great')
    return True


def no_overlaps(df_students, gruops_overlaps):
    groups = set()
    dict_new_group_student = dict()
    dict_old_group_student = dict()
    for _, student in df_students.iterrows():
        groups.add(student['group_id'])

        if student['new_group_id'] != 0:
            if not student['new_group_id'] in dict_new_group_student:
                dict_new_group_student[student['new_group_id']] = set()
            dict_new_group_student[student['new_group_id']].add(student['new_group_id'])
        else:
            if not student['group_id'] in dict_old_group_student:
                dict_old_group_student[student['group_id']] = set()
            dict_old_group_student[student['group_id']].add(student['group_id'])


    for group in groups:
        for overlaping_group in gruops_overlaps.get(group, []):
            for student in dict_new_group_student.get(group, []):
                if student in dict_new_group_student.get(overlaping_group, []):
                    print('not good')
                    return False
                if student in dict_old_group_student.get(overlaping_group, []):
                    print('bad')
                    return False
    print('good')
    return True


def solution_is_valid(df_students, df_limits, gruops_overlaps):
    return valid_student_count(df_students, df_limits) and no_overlaps(df_students, gruops_overlaps)


def final_score(df_students, df_limits, minmax_penalty, student_award, award_activity, gruops_overlaps):
    if solution_is_valid(df_students, df_limits, gruops_overlaps):
        print('cost: ', 1 / (1 + max([0, score_A(df_students) + score_B(df_students, award_activity) + score_C(df_students, student_award) - score_D(df_students, df_limits, minmax_penalty) - score_E(df_students, df_limits, minmax_penalty)])))
        return max([0, score_A(df_students) + score_B(df_students, award_activity) + score_C(df_students, student_award) - score_D(df_students, df_limits, minmax_penalty) - score_E(df_students, df_limits, minmax_penalty)])
    else:
        print('cost2: ', 2)
        return -0.5


#  KOMPLIKACIJA ZBOG BRZINE
def change_df_student(df_students, df_requests, req_to_fulfill):
    students = dict()
    for _, student in df_students.iterrows():
        students[(student['student_id'], student['activity_id'])] = student['new_group_id']

    for i, request in df_requests.iterrows():
        try:
            if req_to_fulfill == 'all' or req_to_fulfill[i] == 1:
                students[(request['student_id'], request['activity_id'])] = request['req_group_id']
        except KeyError:
            print('besmislen request')

    for _, student in df_students.iterrows():
        student['new_group_id'] = students[(student['student_id'], student['activity_id'])]


def cost_function(df_students, df_limits, df_requests, minmax_penalty, student_award, award_activity, gruops_overlaps):
    def cost_function_(x):
        change_df_student(df_students, df_requests, x)
        return 1 / (1 + final_score(df_students, df_limits, minmax_penalty, student_award, award_activity, gruops_overlaps))

    return cost_function_


def clean_df_requests(df_requests, df_students, gruops_overlaps):
    dict_new_group_student = dict()
    dict_old_group_student = dict()
    for _, student in df_students.iterrows():
        if student['new_group_id'] != 0:
            if not student['new_group_id'] in dict_new_group_student:
                dict_new_group_student[student['new_group_id']] = set()
            dict_new_group_student[student['new_group_id']].add(student['new_group_id'])
        else:
            if not student['group_id'] in dict_old_group_student:
                dict_old_group_student[student['group_id']] = set()
            dict_old_group_student[student['group_id']].add(student['group_id'])

    for _, request in df_requests.iterrows():
        for overlaping_group in gruops_overlaps.get(request['req_group_id'], []):
            if request['student_id'] in dict_new_group_student.get(overlaping_group, []):
                if True:
                    pass



def main():
    df_students = pd.read_csv('C:\\Users\\viktor\\Downloads\\student.csv')
    df_requests = pd.read_csv('C:\\Users\\viktor\\Downloads\\requests.csv')
    df_limits = pd.read_csv('C:\\Users\\viktor\\Downloads\\limits.csv')
    df_overlaps = pd.read_csv('C:\\Users\\viktor\\Downloads\\overlaps.csv')

    print(df_students.head())
    print(df_requests.head())
    print(df_limits.head())
    print(df_overlaps.head())

    award_activity = [1, 2, 4]
    student_award = 1
    minmax_penalty = 1

    gruops_overlaps = dict()
    for _, overlap in df_overlaps.iterrows():
        if not overlap['group1_id'] in gruops_overlaps:
            gruops_overlaps[overlap['group1_id']] = set()
        gruops_overlaps[overlap['group1_id']].add(overlap['group2_id'])

    clean_df_requests(df_requests, df_students, gruops_overlaps)

    print(final_score(df_students, df_limits, minmax_penalty, student_award, award_activity, gruops_overlaps))

    #change_df_student(df_students, df_requests, 'all')

    f = cost_function(df_students, df_limits, df_requests, minmax_penalty, student_award, award_activity, gruops_overlaps)
    rezultat, error = k_turnirski_algoritam(f, broj_gena=len(df_requests), p_mutacije=0.08, broj_iteracija=10**2, epsilon=10**-3)
    print(rezultat)
    print(error)

    print(final_score(df_students, df_limits, minmax_penalty, student_award, award_activity, gruops_overlaps))


if __name__ == '__main__':
    main()
