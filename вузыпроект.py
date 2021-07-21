import University_DB as db
from typing import Text
import requests 
from bs4 import BeautifulSoup as bs


line_LETU = db.line_LETU
db_LETU = db.db_LETU
db_POLITECH = db.db_POLITECH

#ЛЭТИ
def html_parser_LETU(str):

    soup = bs(str , 'html.parser')

    own_places = soup.find_all('td' , class_ = "number")
    all_snils = soup.find_all('td' , class_ = "fio")
    prioryties = soup.find_all('td' , class_ = "priority")

    persons = []

    for i in range(len(all_snils)):

        persons.append(
            {
                'place' : own_places[i].text,
                'snils' : all_snils[i].text,
                'priority' : prioryties[i].text
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


choosed_university = 1
while choosed_university != 'End':
    choosed_university = input()


    if choosed_university == "ЛЭТИ":
        #OUTPUT LETU
        for j in range(0 , 6):

            r = requests.get(line_LETU + db_LETU[j])

            persons = html_parser_LETU(r.text)

            for i in range(len(persons)):
                if persons[i]["snils"] == "190-785-069 02":
                    print(db_LETU[j] , persons[i])
                    break
    elif choosed_university == "ПОЛИТЕХ":
        #OUTPUT POLITECH
        for j in range(0 , 4):

            r = requests.get(db_POLITECH[j][1])
            
            persons = html_parser_POLITECH(r.json())

            for i in range(len(persons)):
                if persons[i]["snils"] == "190-785-069 02":
                    print(db_POLITECH[j][0] , persons[i])
                    break


