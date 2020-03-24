import random

# в других файлах писать from alldef import *, это импортнет функции.
# написать функцию, которая просто считает вклад человека в группу.
from gen_relationships import dataAllName
last_people = dataAllName.name.tolist()
list_groups = [[], [], [], [], [], []]
full_dict_relations = {}


def best_person(group, list_last_people=last_people, remove=True):
    mid_dict = {}
    for i in list_last_people:
        sum_1_to_others = 0
        for j in list_groups[group - 1]:
            try:
                sum_1_to_others += full_dict_relations[i][j]
            except:
                pass
            try:
                sum_1_to_others += full_dict_relations[j][i]
            except:
                pass
        mid_dict[i] = sum_1_to_others
    sorted_dict = {k: v for k, v in sorted(
        mid_dict.items(), key=lambda item: item[1], reverse=True)}
    a = list(sorted_dict.keys())[0]
    if remove:
        list_last_people.remove(a)
    return a


def sum_relation(group):
    all_sum = 0
    for i in list_groups[group - 1]:
        for j in list_groups[group - 1]:
            try:
                all_sum += full_dict_relations[i][j]
            except:
                pass
            try:
                all_sum += full_dict_relations[j][i]
            except:
                pass
    return all_sum


# эту функцию стоит доисправить
def best_random_group(group, last_people_def=last_people, pop=10):
    dict_attempts = {}
    dict_of_students = {}
    for i in range(10):
        list_groups = [[], [], [], [], [], []]
        last_people = last_people_def
        list_groups[group - 1].append(last_people.pop(random.randrange(len(last_people))))
        for j in range(pop - 1):
            list_groups[group - 1].append(best_person(group, remove=True))
        dict_attempts[i] = sum_relation(group)
        dict_of_students[i] = list_groups[group - 1]
    max_key = max(dict_attempts, key=dict_attempts.get)

    return dict_of_students[max_key], dict_attempts[max_key]
