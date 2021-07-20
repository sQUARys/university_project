from abc import abstractproperty
from typing import Text
import requests 
import json
from bs4 import BeautifulSoup as bs

db = ['programmnaya-inzheneriya' , 'prikladnaya-matematika-i-informatika' 
, 'informatika-i-vychislitelnaya-tehnika-kmip' , 'informacionnye-sistemy-i-tehnologii'
 , 'elektroenergetika-i-elektrotehnika' , 'upravlenie-v-tehnicheskih-sistemah-fea' ]

line = "https://etu.ru/ru/abiturientam/priyom-na-1-y-kurs/podavshie-zayavlenie/ochnaya/byudzhet/"

def html_parser(str):

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

for j in range(0 , 6):

    r = requests.get(line + db[j])

    persons = html_parser(r.text)

    for i in range(len(persons)):
        if persons[i]["snils"] == "190-785-069 02":
            print(db[j] , persons[i])