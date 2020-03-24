
import pandas as pd
import numpy as np
import random


dataAllQuiz = pd.DataFrame(columns=['id', 'group', 'changeGroup', 'favGroup',
                                    'listOfFavIds', 'listOfTogFor', 'listFavPeople', 'listCananBe', 'listHaters'])

list_of_names = []
with open(r'c:\Users\Professional\Documents\GitHub\sort-groups\200names.txt', 'r') as f:
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

dataAllQuiz = dataAllQuiz.astype('object')
dataAllQuiz['listOfFavIds'][dataAllQuiz.changeGroup ==
                            1 & dataAllQuiz.favGroup.isnull()] = list_of_fav_ids

dataAllQuiz = dataAllQuiz.astype('object')
list_of_tog_for = []
for i in range(len(dataAllQuiz[dataAllQuiz.changeGroup == 0])):
    if np.random.binomial(1, 0.3) == 1:
        times = random.randint(1, 2)
        a = list(set(random.choices(dataAllQuiz[(dataAllQuiz.group == dataAllQuiz.loc[i].group) & (
            dataAllQuiz.id != dataAllQuiz.iloc[i].id)].id.tolist(), k=times)))
        list_of_tog_for.append(a)
    else:
        list_of_tog_for.append(np.nan)
#         dataAllQuiz.loc[i, 'listOfTogFor'].loc[dataAllQuiz.changeGroup == 0] = random.choices(dataAllQuiz[dataAllQuiz.group == dataAllQuiz.loc[i].group].id.tolist(), k = times)


# In[36]:


dataAllQuiz['listOfTogFor'][dataAllQuiz.changeGroup == 0] = list_of_tog_for


# In[ ]:


# In[37]:


# dataAllQuiz[dataAllQuiz.changeGroup == 0]['listOfTogFor']


# In[ ]:


# In[38]:


# dataAllQuiz[dataAllQuiz.listOfTogFor.notna()]


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[39]:


dataAllQuiz = dataAllQuiz.astype('object')
for i in range(len(dataAllQuiz)):
    if np.random.binomial(1, 0.2) == 1:
        times = random.randint(1, 2)
        a = list(set(random.choices(dataAllQuiz[(dataAllQuiz.group != dataAllQuiz.loc[i].group) & (
            dataAllQuiz.id != dataAllQuiz.iloc[i].id)].id.tolist(), k=times)))
        dataAllQuiz.loc[i, 'listCananBe'] = a


# In[40]:


for i in range(len(dataAllQuiz)):
    if np.random.binomial(1, 0.15) == 1:
        times = random.randint(1, 2)
        a = list(
            set(random.choices(dataAllQuiz[dataAllQuiz.id != dataAllQuiz.iloc[i].id].id.tolist(), k=times)))
        dataAllQuiz.loc[i, 'listHaters'] = a


# In[41]:


for i in range(len(dataAllQuiz)):
    if np.random.binomial(1, 0.4) == 1:
        times = random.randint(1, 3)
        a = list(set(random.choices(dataAllQuiz[(dataAllQuiz.group == dataAllQuiz.loc[i].group) & (
            dataAllQuiz.id != dataAllQuiz.iloc[i].id)].id.tolist(), k=times)))
        dataAllQuiz.loc[i, 'listFavPeople'] = a


# In[42]:


# dataAllQuiz.to_excel('dataAllQuiz1.xlsx', index = False)


# In[ ]:


# In[43]:


dataAllName = dataAllQuiz.copy()


# In[44]:


dict_int_name = {}
for i, j in enumerate(list_of_names):
    dict_int_name[str(i + 1)] = j


# In[45]:


dataAllName['name'] = ''
for i in range(len(dataAllName)):
    key = str(i + 1)
    dataAllName['name'].iloc[i] = dict_int_name[key]


# In[ ]:


# In[ ]:


# In[ ]:


# In[46]:


def int_to_name(list_ints):
    if not np.isnan(list_ints).all():
        list_names = []
        for i in list_ints:
            list_names.append(dict_int_name[str(i)])
        return list_names


for i in dataAllName.columns[4:-1].tolist():
    dataAllName[i] = dataAllName[i].apply(int_to_name)
# apply почему-то не работает


dict_number_students = {}
for i, j in enumerate(dataAllQuiz.groupby('group').count().changeGroup):
    dict_number_students[str(i + 1)] = j


# In[50]:


# dict_number_students


# In[51]:


# list_ids = dataAllQuiz.id.tolist()
# dict_group_students = {}
# for i in dict_number_students.keys():
#     list_of_students = []
#     for j in range(1, dict_number_students[i] + 1):
#         list_of_students.append(list_ids.pop(0))
#     dict_group_students[i] = list_of_students


# In[52]:


list_names = dataAllName.name.tolist()
dict_group_students = {}
for i in dict_number_students.keys():
    list_of_students = []
    for j in range(1, dict_number_students[i] + 1):
        list_of_students.append(list_names.pop(0))
    dict_group_students[i] = list_of_students


# In[ ]:


# In[ ]:


# In[53]:


# dataAllName.head(4)


# In[ ]:


# In[54]:


# def get_dict_relation(key, dataAllQuiz = dataAllQuiz, cChange = 0.5, cFavGroup = 0.5, cFavIds = 4, cTogFor = 10, cFavPeople = 3, cCanan = 2, cHaters = -5):
#     dict_one_relation = {}
#     key = int(key)
#     if dataAllQuiz.iloc[key - 1, 2] == 0:
#         for i in dataAllQuiz['id'][(dataAllQuiz.group == dataAllQuiz.iloc[key - 1].group) & (dataAllQuiz.id != dataAllQuiz.iloc[key - 1].id)]:
#             dict_one_relation[str(i)] = cChange
#     else:
#         if np.isnan(dataAllQuiz.iloc[key - 1, 3]):
#             for i in dataAllQuiz.iloc[key - 1, 4]:
#                 dict_one_relation[str(i)] = cFavIds
#         else:
#             for i in dataAllQuiz['id'][dataAllQuiz.group == dataAllQuiz.iloc[key - 1, 3]]:
#                 dict_one_relation[str(i)] = cFavGroup

#     if not np.isnan(dataAllQuiz.iloc[key - 1].listOfTogFor).all():
#         for i in dataAllQuiz.iloc[key - 1].listOfTogFor:
#             dict_one_relation[str(i)] = cTogFor
#     if not np.isnan(dataAllQuiz.iloc[key - 1].listFavPeople).all():
#         for i in dataAllQuiz.iloc[key - 1].listFavPeople:
#             dict_one_relation[str(i)] = cFavPeople
#     if not np.isnan(dataAllQuiz.iloc[key - 1].listCananBe).all():
#         for i in dataAllQuiz.iloc[key - 1].listCananBe:
#             dict_one_relation[str(i)] = cCanan
#     if not np.isnan(dataAllQuiz.iloc[key - 1].listHaters).all():
#         for i in dataAllQuiz.iloc[key - 1].listHaters:
#             dict_one_relation[str(i)] = cHaters
#     return dict_one_relation
# Ключ пусть будем именным


# In[55]:


dataAllName = dataAllName.fillna(np.nan)


# In[56]:


# fixed. It will work with strings.
# Что исправить. Да, вот будет не id, а фамилии. И надо их заставить корректно встать в словарь.
# То есть сгенерировать более точно, плюс заменить цифры на фамилии.
# Если человек хочет покинуть группу, но не знает какую, -1 для всех членов текущей группы
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


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[61]:


# get_dict_relation(dataAllName.name.tolist()[47], dataAllQuiz = dataAllName)


# In[57]:


# dataAllName.name.tolist()[0]


# In[ ]:


# In[328]:


# full_dict_relations = {}
# list_ids = dataAllQuiz.id.tolist()
# for i in list_ids:
#     full_dict_relations[str(i)] = get_dict_relation(i)

# In[58]:
full_dict_relations = {}
list_names = dataAllName.name.tolist()
for i in list_names:
    full_dict_relations[i] = get_dict_relation(i, dataAllQuiz=dataAllName)

# name_dict_relations = input('type the name of dictionary of relationships')
# with open(r'C:\Users\Professional\Documents\GitHub\sort-groups\full_dict_relations1.txt', 'w') as f:
#     f.write(str(full_dict_relations))


list_groups = [[], [], [], [], [], []]


last_people = dataAllName.name.tolist()


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
    if remove == True:
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


for i in range(30):
    list_groups[0].append(best_person(1))

print(list_groups)
# best_random_group(1)

# max(test_dict, key=test_dict.get)


# list(test_dict.values())[0]


# sum_relation(6)

# last_people.pop(random.randrange(len(last_people)))
