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

# Такая же функция, что и предыдущая, но принимающая значение depth, обозначающее количество людей на замену
# Нужен модуль itertools
def student_change1(group_dict, depth, is_change = True):
    while is_change == True or depth != 0:
        sorted_list = []
        is_change = False
        for group_num in group_dict:
            for student_tuple in list(itertools.combinations(group_dict[group_num], depth)):
                if set(sorted_list) & set(student_tuple):
                    continue
                max_coef_change = 0
                for other_group_num in group_dict:
                    if other_group_num != group_num:
                        for other_student_tuple in list(itertools.combinations(group_dict[other_group_num], depth)):
                            if set(sorted_list) & set(other_student_tuple):
                                continue
                            whatif_dict = copy.deepcopy(group_dict)
                            for student_id in student_tuple:
                                whatif_dict[group_num].remove(student_id)
                                whatif_dict[other_group_num].add(student_id)
                            for other_student_id in other_student_tuple:
                                whatif_dict[other_group_num].remove(other_student_id)
                                whatif_dict[group_num].add(other_student_id)
                            sumcoef_before = all_coef_count(group_dict)
                            sumcoef_after = all_coef_count(whatif_dict)
                            if sumcoef_after - sumcoef_before > max_coef_change:
                                max_coef_change = sumcoef_after - sumcoef_before
                                student_change_tuple = other_student_tuple
                                group_change = other_group_num
                if max_coef_change > 0:
                    for student_id in student_tuple:
                        group_dict[group_num].remove(student_id)
                        group_dict[group_change].add(student_id)
                        sorted_list.append(student_id)
                    for student_change_id in student_change_tuple:
                        group_dict[group_change].remove(student_change_id)
                        group_dict[group_num].add(student_change_id)
                        sorted_list.append(student_change_id)
                    is_change = True
        if is_change == False:
            depth -= 1
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
'''
Принимает словарь (ключ - id студента, значение - словарь(ключ - id другого студента, значение - коэффициент отношения)) и количество групп
Возвращает словарь в том же формате, объединяя людей, у которых сумма коэффициентов равна 20. Ключ в таком случа будет кортеж с id студентов.
Количество групп нужно, чтобы посчитать длину группы с помощью функции count_group_vol.
Это значение нужно, чтобы предотвращать объединение людей в количестве большем, чем должно быть людей в группе.
Все коэффициенты отношения у объединённых людей суммируются. Названия в словорях отношений других людей заменяются на соответствующие кортежи
Функция учитывает возможность объединения людей в группы по 2 и более людей (вплоть до максимальной длины группы)
Если объединяются больше 2 людей, то сумма коэффициентов каждой пары должна быть равна 20
Если есть несколько людей, имеющих сумму коэффициентов 20 с одним человеком, но между ними эта сумма меньше,
то берётся человек, имеющий наибольшую сумму коэффициентов в группе людей, имеющих сумму коэффицентов 20 с данным человеком.
Данный выбор делается, чтобы избежать ситуации добавления человека с плохими отношениями с остальными,
другими словами, чтобы сортировка с большей вероятностью объединила оставшихся желающих быть в группе с данным человеком.
Полученные объединения рассматриваются как один человек. Чтобы учитывалось количество людей в объединениях, придется немного изменить сортировку.
К сожалению, если наоборот, два разных данных человека хотят объединиться с одним и их сумма коэффициентов меньше 20,
то объединится первый попавшийся. Я все еще пытаюсь решить эту проблему.
'''
def student_unite(student_dict, group_number):
    student_unite_dict = {} # Cловарь
    student_unite_list = []
    for student_id in student_dict:
        might_be_pair = []
        if student_id in student_unite_list:
            continue
        for other_student_id in student_dict[student_id]:
            if student_id in student_dict[other_student_id]:
                if student_dict[student_id][other_student_id] + student_dict[other_student_id][student_id] == 20:
                    if other_student_id in student_unite_list:
                        continue
                    if student_id in student_unite_list:
                        sumcoef = 0
                        for student_in_pair in student_unite_dict[student_id]:
                            if student_in_pair in student_dict[other_student_id] and other_student_id in student_dict[student_in_pair]:
                                sumcoef += student_dict[student_in_pair][other_student_id] + student_dict[other_student_id][student_in_pair]
                        if sumcoef / len(student_unite_dict[student_id]) == 20 and len(student_unite_dict[student_id]) in range (2, count_group_vol(student_dict, group_number)):
                            student_unite_dict[student_id].append(other_student_id)
                            student_unite_list.append(other_student_id)
                    else:
                        student_unite_dict[student_id] = [student_id]
                        student_unite_list.append(student_id)
                        might_be_pair.append(other_student_id)
        if might_be_pair and len(student_unite_dict[student_id]) in range (1, count_group_vol(student_dict, group_number)):
            for might_add_id in might_be_pair:
                maxcoef = -20 * (len(might_be_pair + student_unite_dict[student_id]) - 1) - 1
                for other_student_id in might_be_pair + student_unite_dict[student_id]:
                    sumcoef = 0
                    if other_student_id != might_add_id:
                        if might_add_id in student_dict[other_student_id]:
                            sumcoef += student_dict[other_student_id][might_add_id]
                        if other_student_id in student_dict[might_add_id]:
                            sumcoef += student_dict[might_add_id][other_student_id]
                    if sumcoef > maxcoef and might_add_id not in student_unite_list:
                        maxcoef = sumcoef
                        add_id = might_add_id
            student_unite_dict[student_id].append(add_id)
            student_unite_list.append(add_id)
    for student_pair in student_unite_dict:
        coef_in_pair = student_dict[student_unite_dict[student_pair][0]]
        for student_in_pair in student_unite_dict[student_pair]:
            if student_in_pair != student_unite_dict[student_pair][0]:
                for third_student_id in student_dict[student_in_pair]:
                    if third_student_id != student_unite_dict[student_pair][0]:
                        if third_student_id not in coef_in_pair:
                            coef_in_pair[third_student_id] = 0
                        else:
                            coef_in_pair[third_student_id] += student_dict[student_in_pair][third_student_id]
                        if coef_in_pair[third_student_id] == 0:
                            del coef_in_pair[third_student_id]
                del student_dict[student_unite_dict[student_pair][0]][student_in_pair]
                del student_dict[student_in_pair]
        student_dict[student_unite_dict[student_pair][0]] = coef_in_pair
        student_dict[tuple(student_unite_dict[student_pair])] = student_dict.pop(student_unite_dict[student_pair][0])
        for third_student_id in student_dict:
            if third_student_id != student_unite_dict[student_pair][0]:
                if student_unite_dict[student_pair][0] in student_dict[third_student_id]:
                    coef_for_student = student_dict[third_student_id][student_unite_dict[student_pair][0]]
                else:
                    coef_for_student = 0
                for student_in_pair in student_unite_dict[student_pair]:
                    if student_in_pair != student_unite_dict[student_pair][0] and student_in_pair in student_dict[third_student_id]:
                        coef_for_student += student_dict[third_student_id][student_in_pair]
                        del student_dict[third_student_id][student_in_pair]
                if coef_for_student != 0:
                    student_dict[third_student_id][student_unite_dict[student_pair][0]] = coef_for_student
                    student_dict[third_student_id][tuple(student_unite_dict[student_pair])] = student_dict[third_student_id].pop(student_unite_dict[student_pair][0])
    return student_dict

# Принимает словарь студентов(ключ - id, значение словарь(ключ - id, значение - коэффициент)) и количество групп
# Возвращает длину максимальную длину групп. Если не делится нацело, возвращает целую часть от деления + 1
def count_group_vol(student_dict, group_number):
    if len(student_dict) / group_number == int(len(student_dict) / group_number):
        return len(student_dict) / group_number
    return len(student_dict) // group_number + 1
