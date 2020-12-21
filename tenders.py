import requests
from bs4 import BeautifulSoup
import csv
import time
import urllib
import fake_useragent
import transliterate
import datetime
import dataAutorize

now = datetime.datetime.now()
date = now.strftime("%d-%m-%Y %H:%M")
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0', 'accept': '*/*'}
session = requests.Session()
HOST = 'http://t1.torgi223.ru/'
link = 'http://t1.torgi223.ru/login.php'
user = fake_useragent.UserAgent().random

header = {
    'user-agent': user
}

data = dataAutorize.data

responce = session.post(link, data=data, headers=header).text

def get_html(url, params=None):
    r = session.get(url, headers=header, params=params)
    return r

def get_html2(url, params=None):
    d = requests.get(url, headers=HEADERS, params=params)
    return d



# Считаем количество страниц в категории/каталоге
def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    paginationTo = soup.find('div', class_='pagination')

    if paginationTo:
        paginationTo = soup.find('div', class_='pagination')
        pagination = paginationTo.find_all('a') 
        pagination2 = str(pagination[-1].get('href'))
        pagination3 = pagination2[21:]
        return int(pagination3)  

    else:
        return 1
        

# Получаем необходимые поля/данные
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('tr', {"id": "rowId-0"})
    catalog = []  
    for item in items:


        nameProcedure = item.find('td', class_='row-purchaseName').get_text(strip=True)
        nameProcedure2 = str(nameProcedure)

        words = ["печатная", "конверты", "конвертов", "бланочной", "журналы", "журналов", "полиграфической", "полиграфии",
         "печатного", "печать", "печати", "полиграфических", "бланки", "бланков", "бланочной", "газеты",
          "газет", "папок", "папки", "типографская", "полиграфические", "печатная", "фотоальбомов", "фотоальбомы", "альбомы",
           "альбомов", "календари", "календарей", "фотокалендари", "фотокалендарей", "визитные карточки", "визитных карточек",
            "журналов", "журналы", "календаря", "открыток", "открытки", "печатных",  "каталогов", "газет", "открытки", "открыток",
             "типорграфических", "типографические", "печатных", "печатных", "печатных", "печатных", "печатных", "печатных",
              "конверты", "конвертов", "наклеек", "визиток", "визитки", "сувенирная", "календарь", "календарная", "подарочная"]
        
        for word in words:
            if word.lower() in nameProcedure2.lower():
                # Ссылка на процедуру
                href = item.find('a').get('href')

                html2 = get_html(href)
                soup2 = BeautifulSoup(html2.text, 'html.parser')
                items2 = soup2.find('li', class_='current')                
        
                # Наименование заказчика    
                customer = item.find('td', class_='row-customerName').get_text(strip=True)
                print(customer)                            
            
                # Номер процедуры
                numberProcedure = item.find('td', class_='row-id').get_text(strip=True)
                print(numberProcedure)
                
                # Номер извещения в ЕИС
                numberEIS = item.find('td', class_='row-registrationNumber').get_text(strip=True)             

                # Начальная (максимальная) цена процедуры
                cost = item.find('td', class_='row-lotPrice').get_text(strip=True)        

                # Дата публикации
                date = item.find('td', class_='row-publicDate').get_text(strip=True)         

                # Дата окончания подачи заявок
                dateLast = item.find('td', class_='row-endPublicationDate').get_text(strip=True)      

                # Тип процедуры
                typeProcedure = item.find('td', class_='row-typeTorgsName').get_text(strip=True)         

                # Статус процедуры
                typeProcedure = item.find('td', class_='row-statusName').get_text(strip=True)           
            else:
                continue
               

            catalog.append({
                'numberProcedure': numberProcedure,
                'numberEIS': numberEIS,
                'customer': customer,
                'nameProcedure': nameProcedure2,
                'cost': cost,
                'date': date,
                'dateLast': dateLast,
                'typeProcedure': typeProcedure,


            })            
            
    return catalog                    
            

            



# функция записи спарсенных значений в csv файл
def save_file(items, path):
    with open(path, 'w',  encoding='utf8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Категории',])
        for item in items:
            writer.writerow([item['title'],])

# Основная функция Создаём каталог
def parse():
    for URL in [
        
'http://t1.torgi223.ru/registry/list/'

    ]:

        html = get_html(URL)
        print(html)
        if html.status_code == 200:
            catalog = []
            pages_count = get_pages_count(html.text)
            for page in range (1, pages_count + 1):
                print(f'Парсинг страницы {page} {pages_count} {URL}...')
                html = get_html(URL, params={'page': page})
                catalog.extend(get_content(html.text))
                time.sleep(1)
            FILE = date + '.csv'   
            save_file(catalog, FILE)


            print(f'Получено {len(catalog)} товаров')
        else:
            print('Error')  

# Функция срабатывает каждые сутки (86400 секунд)





parse()



""" 'https://2676270.ru/catalog/yarn/92/',
'https://2676270.ru/catalog/yarn/93/',
'https://2676270.ru/catalog/yarn/1419/'
'https://2676270.ru/catalog/yarn/1677/',
'https://2676270.ru/catalog/yarn/2453/',
'https://2676270.ru/catalog/yarn/909/',
'https://2676270.ru/catalog/yarn/95/' 

while True:
    time.sleep(30)
    parse()"""