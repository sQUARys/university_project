from re import L
from sys import implementation

from nltk.util import pr
import University_DB as db
from typing import Text
import requests 
from bs4 import BeautifulSoup as bs

line_LETU = db.line_LETU
db_LETU = db.db_LETU
db_POLITECH = db.db_POLITECH
line_ITMO = db.line_ITMO
db_ITMO = db.db_ITMO

#ЛЭТИ
def html_parser_LETU(str):

    soup = bs(str , 'html.parser')

    own_places = soup.find_all('td' , class_ = "number")
    all_snils = soup.find_all('td' , class_ = "fio")
    prioryties = soup.find_all('td' , class_ = "priority")
    summa_ballov = soup.find_all('td' , class_ = "ball")

    persons = []

    for i in range(len(all_snils)):

        persons.append(
            {
                'place' : own_places[i].text,
                'snils' : all_snils[i].text,
                'priority' : prioryties[i].text,
                'balls' : summa_ballov[i].text
            }
        )
    
    return persons


#Политех
def html_parser_POLITECH(str):

    list_applicants = str["data"]['list_applicants']
    persons = []

    for i in range(0 , len(list_applicants)):
        
        persons.append(
            {
                'place' : list_applicants[i]['Номер'],
                'snils' : list_applicants[i]['УникальныйКод'],
                'summ_ballov' : list_applicants[i]['СуммаБаллов']
            }
        )
    
    return persons



#Итмо
def html_parser_ITMO(str):
    soup = bs(str , 'html.parser')
    
    all_info =  soup.find_all('td' ,)

    persons = []

    count = 0
    person = []

    for i in range(0 , len(all_info)):
        if count < 14:

            person.append(all_info[i].text)
            count += 1

        else:

            persons.append(person)
            person = []
            count = 0

    return persons



choosed_university = True

while choosed_university != 'End':
    choosed_university = input()


    if choosed_university == "ЛЭТИ":
        #OUTPUT LETU
        for j in range(0 , 6):

            r = requests.get(line_LETU + db_LETU[j])

            persons = html_parser_LETU(r.text)
            count = 0
            for i in range(len(persons)):

                if persons[i]["snils"] == "190-785-069 02":
                    print("Специальность:" , db_LETU[j] ,"Данные о человеке:"  , persons[i])
                    print("Количество людей до меня, у которых не первый приоритет на эту специальность:" , count)
                    print('')
                    break

                if persons[i]['priority'] != '1':
                    count += 1

        for i in range(7, len(db_LETU)):
            r = requests.get(line_LETU + db_LETU[i])

            persons = html_parser_LETU(r.text)

            count = 0

            for j in range(len(persons)):
                
                if persons[j]["balls"] == "273":
                    print("Специальность:" , db_LETU[i] ,"Данные о человеке:"  , persons[j])
                    print("Количество людей до меня, у которых не первый приоритет на эту специальность:" , count)
                    print('')
                    break

                if persons[j]['priority'] != '1':
                    count += 1

        print("That's all, what i can write you)")

        
    elif choosed_university == "ПОЛИТЕХ":
        #OUTPUT POLITECH
        for j in range(0 , 4):

            r = requests.get(db_POLITECH[j][1])
            
            persons = html_parser_POLITECH(r.json())

            for i in range(len(persons)):
                if persons[i]["snils"] == "190-785-069 02":
                    print("Специальность:" , db_POLITECH[j][0] ,"Данные о человеке:" , persons[i])
                    print('')
                    break
        print("That's all, what i can write you)")


    elif choosed_university == "ИТМО":

        count = 0
        
        for i in range(0 , 4):

            r = requests.get(line_ITMO + db_ITMO[i][1])
            print(line_ITMO + db_ITMO[i][1])
            persons = html_parser_ITMO(r.text)
            persons.pop(0)
            print(persons[i][2])
            if persons[i][2] == "Косенко Роман Дмитриевич":
                print(db_ITMO[i][0] , persons[i])
                break

        # r = requests.get(line_ITMO + db_ITMO[0][1])

        # persons = html_parser_ITMO(r.text)
        # for i in range(0 , len(persons)):
        #     # pesons[1] - приоритет
        #     if persons[i][1] != '1' and persons[i][7] !='273' and  persons[i][10] == 'Нет' and  persons[i][11] == 'Нет':
        #         count += 1
        #     elif persons[i][7] == '273':
        #         print("Моё место на эту специальность, НЕ СЧИТАЯ БВИ И ОСОБЫХ:" , persons[i][0])
        # print("Количество людей до меня, для которых данная специальность не в приоритете:" , count)
