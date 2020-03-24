import random

# в других файлах писать from alldef import *, это импортнет функции.
from gen_relationships import dataAllName
last_people = dataAllName.name.tolist()
list_groups = [[], [], [], [], [], []]
full_dict_relations = {}


# она берёт номер группы, список оставшихся людей, можно выбрать удалять ли выбранного человека из того списка или нет. Возвращает лишь имя лучшего учащегося.


def best_person(group, last_people, remove=True):
    mid_dict = {}
    for i in last_people:
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
        last_people.remove(a)
    return a


# на вход получает номер группы, выдаёт обратно число - сумма отношений
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


# получаем имя человека, номер группы и просто считает его вносимый вклад в эту группу. Возвращает имя человека и вносимый вклад одновременно, чтобы было удобно занести в словарь.
def contribution_one_person(person, num_group):
    sum_contr = 0
    for i in list_groups[num_group - 1]:
        try:
            sum_contr += full_dict_relations[person][i]
        except:
            pass
        try:
            sum_contr += full_dict_relations[i][person]
        except:
            pass
    return person, sum_contr

# принимает словарь (ключ - номер группы, значение - множество id cтудентов); возвращает словарь того же формата; производит замены в группах
# для работы нужен модуль copy и функция all_coef_count
def student_change(group_dict, is_change = True):
    while is_change == True:
        is_change = False
        for group_num in group_dict:
            for student_id in group_dict[group_num]:
                max_coef_change = 0
                for other_group_num in group_dict:
                    if other_group_num != group_num:
                        for other_student_id in group_dict[other_group_num]:
                            whatif_dict = copy.deepcopy(group_dict)
                            whatif_dict[group_num].remove(student_id)
                            whatif_dict[other_group_num].add(student_id)
                            whatif_dict[other_group_num].remove(other_student_id)
                            whatif_dict[group_num].add(other_student_id)
                            sumcoef_before = all_coef_count(group_dict)
                            sumcoef_after = all_coef_count(whatif_dict)
                            if sumcoef_after - sumcoef_before > max_coef_change:
                                max_coef_change = sumcoef_after - sumcoef_before
                                student_change_id = other_student_id
                                group_change = other_group_num
                if max_coef_change > 0:
                    group_dict[group_num].remove(student_id)
                    group_dict[group_change].add(student_id)
                    group_dict[group_change].remove(student_change_id)
                    group_dict[group_num].add(student_change_id)
                    is_change = True
    return group_dict

# принимает словарь (ключ - номер группы, значение - множество id cтудентов); возвращает числовое значение(int), обозначающее сумму коэффициентов отношений во всех группах
def all_coef_count(group_dict):
    summcoef = 0
    for group_number in group_dict:
        for student_id in group_dict[group_number]:
            for other_student_id in student_dict1[student_id]:
                if other_student_id in group_dict[group_number]:
                    summcoef += student_dict1[student_id][other_student_id]
    return summcoef
