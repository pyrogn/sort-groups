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
