import re
from pprint import pprint
import csv
## Читаем адресную книгу в формате CSV в список contacts_list:

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

new_list = []

#№Разделим ФИО на Ф+И+О

for name in contacts_list[1:]:
    res = " ".join(name[:3]).split()
    if len(res) == 3:
        name[0] = res[0]
        name[1] = res[1]
        name[2] = res[2]
    elif len(res) == 2:
        name[0] = res[0]
        name[1] = res[1]
        name[2] = ''
    elif len(res) == 1:
        name[0] = res[0]
        name[1] = ''
        name[2] = ''

##Заменим номера телефонов

pattern = re.compile(r'(\+7|8)?\s*\(?(\d{3})\)?[\s*-]?(\d{3})[\s*-]?(\d{2})[\s*-]?(\d{2})(\s*)\(?(доб\.?)?\s*(\d*)?\)?')
replace = r'+7(\2)\3-\4-\5\6\7\8'
for contact in contacts_list:
    contact[5] = re.sub(pattern, replace, contact[5])
#pprint(contact[5])

#Объединение дублирующих записей

contact_list = {}
for element in contacts_list:
    key = element[0]
    if key not in contact_list:
        contact_list[key] = element
    else:
        for id, el in enumerate(contact_list[key]):
            if el == '':
                contact_list[key][id] = element[id]
#pprint(contact_list)

for element, contact in contact_list.items():
    for element in contact:
        if contact not in new_list:
            new_list.append(contact)
#pprint(new_list)

## Код для записи файла в формате CSV:
with open("phonebook.csv", "w", encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(new_list)

