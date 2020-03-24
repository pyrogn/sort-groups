# возвращает full_dict_relations как словарь словарей


import pandas as pd
import numpy as np
import random
pd.set_option('mode.chained_assignment', None)
dataAllQuiz = pd.DataFrame(columns=['id', 'group', 'changeGroup', 'favGroup',
                                    'listOfFavIds', 'listOfTogFor', 'listFavPeople', 'listCananBe', 'listHaters'])

list_of_names = []
with open('200names.txt', 'r') as f:
    for i in f.readlines():
        list_of_names.append(i.split('\n')[0])
random.shuffle(list_of_names)

numPeople = 174
dataAllQuiz = dataAllQuiz.astype('object')

dataAllQuiz['id'] = range(1, numPeople + 1)

basicNumPeople = numPeople // 7 + 1
leftNumPeople = numPeople - basicNumPeople * 6
uniqueGroup = list(range(1, 8))
allGroup = []
for i in enumerate(uniqueGroup):
    if i[0] < 6:
        allGroup.append([i[1]] * basicNumPeople)
    else:
        allGroup.append([i[1]] * leftNumPeople)

dataAllQuiz['group'] = [x for y in allGroup for x in y]

dataAllQuiz['changeGroup'] = np.random.binomial(1, 0.07, 174)

for i in range(len(dataAllQuiz[dataAllQuiz.changeGroup == 1]['favGroup'])):
    if int(np.random.binomial(1, 0.5, 1)) == 1:
        dataAllQuiz.loc[dataAllQuiz.changeGroup == 1, 'favGroup'] = random.choice(uniqueGroup)

list_of_favGroup = []
for i in range(len(dataAllQuiz[dataAllQuiz.changeGroup == 1])):
    if int(np.random.binomial(1, 0.5, 1)) == 1:
        changeGroupWOut = uniqueGroup.copy()
        changeGroupWOut.remove(dataAllQuiz[dataAllQuiz.changeGroup == 1].iloc[i].group)
        list_of_favGroup.append(random.choice(changeGroupWOut))
    else:
        list_of_favGroup.append(np.nan)

dataAllQuiz['favGroup'].loc[dataAllQuiz.changeGroup == 1] = list_of_favGroup

list_of_fav_ids = []
for i in range(len(dataAllQuiz[dataAllQuiz.changeGroup == 1 & dataAllQuiz.favGroup.isnull()])):
    times = random.randint(1, 3)
    list_of_fav_ids.append(random.choices(
        dataAllQuiz[dataAllQuiz.group != dataAllQuiz.iloc[1].group].id.tolist(), k=times))

dataAllQuiz['listOfFavIds'][dataAllQuiz.changeGroup ==
                            1 & dataAllQuiz.favGroup.isnull()] = list_of_fav_ids

list_of_tog_for = []
for i in range(len(dataAllQuiz[dataAllQuiz.changeGroup == 0])):
    if np.random.binomial(1, 0.3) == 1:
        times = random.randint(1, 2)
        a = list(set(random.choices(dataAllQuiz[(dataAllQuiz.group == dataAllQuiz.loc[i].group) & (
            dataAllQuiz.id != dataAllQuiz.iloc[i].id)].id.tolist(), k=times)))
        list_of_tog_for.append(a)
    else:
        list_of_tog_for.append(np.nan)

dataAllQuiz['listOfTogFor'][dataAllQuiz.changeGroup == 0] = list_of_tog_for

dataAllQuiz = dataAllQuiz.astype('object')
for i in range(len(dataAllQuiz)):
    if np.random.binomial(1, 0.2) == 1:
        times = random.randint(1, 2)
        a = list(set(random.choices(dataAllQuiz[(dataAllQuiz.group != dataAllQuiz.loc[i].group) & (
            dataAllQuiz.id != dataAllQuiz.iloc[i].id)].id.tolist(), k=times)))
        dataAllQuiz.loc[i, 'listCananBe'] = a

for i in range(len(dataAllQuiz)):
    if np.random.binomial(1, 0.15) == 1:
        times = random.randint(1, 2)
        a = list(
            set(random.choices(dataAllQuiz[dataAllQuiz.id != dataAllQuiz.iloc[i].id].id.tolist(), k=times)))
        dataAllQuiz.loc[i, 'listHaters'] = a

for i in range(len(dataAllQuiz)):
    if np.random.binomial(1, 0.4) == 1:
        times = random.randint(1, 3)
        a = list(set(random.choices(dataAllQuiz[(dataAllQuiz.group == dataAllQuiz.loc[i].group) & (
            dataAllQuiz.id != dataAllQuiz.iloc[i].id)].id.tolist(), k=times)))
        dataAllQuiz.loc[i, 'listFavPeople'] = a

dataAllName = dataAllQuiz.copy()
# In[32]:
dict_int_name = {}
for i, j in enumerate(list_of_names):
    dict_int_name[str(i + 1)] = j
# In[33]:
dataAllName['name'] = ''
for i in range(len(dataAllName)):
    key = str(i + 1)
    dataAllName['name'].iloc[i] = dict_int_name[key]


def int_to_name(list_ints):
    if not np.isnan(list_ints).all():
        list_names = []
        for i in list_ints:
            list_names.append(dict_int_name[str(i)])
        return list_names


for i in dataAllName.columns[4:-1].tolist():
    dataAllName[i] = dataAllName[i].apply(int_to_name)

dict_number_students = {}
for i, j in enumerate(dataAllQuiz.groupby('group').count().changeGroup):
    dict_number_students[str(i + 1)] = j

list_names = dataAllName.name.tolist()
dict_group_students = {}
for i in dict_number_students.keys():
    list_of_students = []
    for j in range(1, dict_number_students[i] + 1):
        list_of_students.append(list_names.pop(0))
    dict_group_students[i] = list_of_students


def get_dict_relation(key, dataAllQuiz=dataAllQuiz, cChange=0.5, cFavGroup=0.5, cFavIds=4, cTogFor=10, cFavPeople=3, cCanan=2, cHaters=-5):
    dict_one_relation = {}
    id_on_key = int(dataAllQuiz[dataAllQuiz.name == key].id)
    if dataAllQuiz.iloc[id_on_key - 1, 2] == 0:
        for i in dataAllQuiz['name'][(dataAllQuiz.group == dataAllQuiz.iloc[id_on_key - 1].group) & (dataAllQuiz.id != dataAllQuiz.iloc[id_on_key - 1].id)]:
            dict_one_relation[i] = cChange
    else:
        if np.isnan(dataAllQuiz.iloc[id_on_key - 1, 3]):
            for i in dataAllQuiz.iloc[id_on_key - 1, 4]:
                dict_one_relation[i] = cFavIds
        else:
            for i in dataAllQuiz['name'][dataAllQuiz.group == dataAllQuiz.iloc[id_on_key - 1, 3]]:
                dict_one_relation[i] = cFavGroup
    columns_values = {'listOfTogFor': cTogFor, 'listFavPeople': cFavPeople,
                      'listCananBe': cCanan, 'listHaters': cHaters}
    for keys, values in columns_values.items():
        try:
            if type(pd.isna(dataAllName.iloc[id_on_key - 1][keys])) is not bool:
                for i in dataAllQuiz.iloc[id_on_key - 1][keys]:
                    dict_one_relation[i] = values
        except:
            pass
    return dict_one_relation


full_dict_relations = {}
list_names = dataAllName.name.tolist()
for i in list_names:
    full_dict_relations[i] = get_dict_relation(i, dataAllQuiz=dataAllName)

# with open('full_dict_relations.txt', 'w') as f:
#     f.write(str(full_dict_relations))
