from alldef import best_person

from gen_relationships import full_dict_relations
# либо же локально загружать этот словарь

list_groups = [[], [], [], [], [], []]
# full_dict_relations - сгенерированный словарь
# print(full_dict_relations)

for i in range(15):
    list_groups[0].append(best_person(1))

print(list_groups[0])
