from abc import abstractproperty
from typing import Text
import requests 
import json
from bs4 import BeautifulSoup as bs
#DBS
db_LETU = ['programmnaya-inzheneriya' , 'prikladnaya-matematika-i-informatika' 
, 'informatika-i-vychislitelnaya-tehnika-kmip' , 'informacionnye-sistemy-i-tehnologii'
 , 'elektroenergetika-i-elektrotehnika' , 'upravlenie-v-tehnicheskih-sistemah-fea' ]

#LINK
line_LETU = "https://etu.ru/ru/abiturientam/priyom-na-1-y-kurs/podavshie-zayavlenie/ochnaya/byudzhet/"
line_POLITECH = "https://enroll.spbstu.ru/ajax/interactive_detail?report_option=25f848f5-daa1-11eb-8040-0050569f980a&scenario=e816affc-5f19-11eb-803a-0050569f980a&scenarioN=Списки поступающих по программам бакалавриата/специалитета в 2021 году для граждан РФ&level_education=b7af2da3-5972-11eb-803a-0050569f980a&form_education=a5ae897b-5972-11eb-803a-0050569f980a&basis_admission=a5ae8977-5972-11eb-803a-0050569f980a|false&faculty=34e3382d-5ef2-11eb-803a-0050569f980a&direction=74d76527-9ed2-11eb-803c-0050569f980a&profile=00000000-0000-0000-0000-000000000000&actions=list_applicants"

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



#OUTPUT LETU
for j in range(0 , 6):

    r = requests.get(line_LETU + db_LETU[j])

    persons = html_parser_LETU(r.text)

    for i in range(len(persons)):
        if persons[i]["snils"] == "190-785-069 02":
            print(db_LETU[j] , persons[i])
            break

r = requests.get(line_POLITECH)

print(html_parser_POLITECH(r.json()))

