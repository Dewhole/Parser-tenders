import requests
from bs4 import BeautifulSoup
import csv
import time
import urllib
import fake_useragent
import transliterate
import datetime
import dataAutorize
from multiprocessing import Pool


now = datetime.datetime.now()
date = now.strftime("%d-%m-%Y %H:%M")


# Авторизация сессии
session = requests.Session()
HOST = 'http://t1.torgi223.ru/'
link = 'http://t1.torgi223.ru/login.php'
user = fake_useragent.UserAgent().random
data = dataAutorize.data
header = {
    'user-agent': user
}
responce = session.post(link, data=data, headers=header).text


HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0', 'accept': '*/*'}




def get_html(url, params=None):
    r = session.get(url, headers=HEADERS, params=params)
    return r


def get_ajax(ajaxhref, ajaxId, HEADERSajax, params=None):
    d = session.post(ajaxhref, data=ajaxId, headers=HEADERSajax, params=params)
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
  #      return 100
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
                hrefLot = href
                print(href)
                print(nameProcedure2)
                html2 = get_html(href)
                soup2 = BeautifulSoup(html2.text, 'html.parser')  




                # Наименование заказчика    
                customer = item.find('td', class_='row-customerName').get_text(strip=True)

                # Номер процедуры
                numberProcedure = item.find('td', class_='row-id').get_text(strip=True)

                
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
                statusProcedure = item.find('td', class_='row-statusName').get_text(strip=True)         

                # Получаем id ajax запроса
                try:
                    ajaxId0 = soup2.find('td', class_='viewDatanLot').get('lotid')


                except:
                    try:
                        ajaxId0 = soup2.find('td', class_='viewDatanLotPriceRequest').get('lotid')


                    except:
                        try:
                            ajaxId0 = soup2.find('td', class_='viewDatanLotAuction').get('lotid')

                        except:
                            try:
                                ajaxId0 = soup2.find('td', class_='viewDatanLotEShop').get('lotid')

                            except:
                                try:
                                    ajaxId0 = soup2.find('td', class_='viewDatanLotMlpdo').get('lotid')
                           
                                except:
                                    print('error')


                ajaxId = {
                    'id': ajaxId0
                }

                HEADERSajax = {
                    'Accept': 'text/html, */*',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Connection': 'keep-alive',
                    'Content-Length': '8',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Cookie': '_ym_uid=1608004265188028299; _ym_d=1608004265; _fbp=fb.1.1608004265021.1214446099; viewError=; PHPSESSID=m6jfdgp7dlqtp6qpltlv8k4ul2',
                    'Host': 't1.torgi223.ru',
                    'Origin': 'http://t1.torgi223.ru',
                    'Referer': 'http://t1.torgi223.ru/index.php?module=71&mode=viewRequest&requestId=20815',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest',
                }
               
                
                ajaxhref = 'http://t1.torgi223.ru/includes/AuctionIS/ajax/viewLot.php'
                ajaxhref2 = 'http://t1.torgi223.ru/ajaxViewLotProffer.php'
                ajaxhref3 = 'http://t1.torgi223.ru/qrAjaxViewLotQuotation.php'
                ajaxhref4 = 'http://t1.torgi223.ru/includes/QuotationNt/ajax/qntAjaxViewLotQuotation.php'
                ajaxhref4 = 'http://t1.torgi223.ru/includes/AuctionIS/ajax/viewLot.php'
                ajaxhref5 = 'http://t1.torgi223.ru/includes/Cez/ajax/viewLot.php'



                html3 = get_ajax(ajaxhref, ajaxId, HEADERSajax)
                soup3 = BeautifulSoup(html3.text, 'html.parser').get_text
                strsoup3 = str(soup3)
                lenstr = ((len(strsoup3)))
                if lenstr == 31:
                    html3 = get_ajax(ajaxhref2, ajaxId, HEADERSajax)
                    soup3 = BeautifulSoup(html3.text, 'html.parser').get_text
                    strsoup3 = str(soup3)
                    lenstr = ((len(strsoup3)))
                else:
                    html3 = get_ajax(ajaxhref, ajaxId, HEADERSajax)
                    soup3 = BeautifulSoup(html3.text, 'html.parser').get_text

                if lenstr == 31:
                    html3 = get_ajax(ajaxhref3, ajaxId, HEADERSajax)
                    soup3 = BeautifulSoup(html3.text, 'html.parser').get_text
                    strsoup3 = str(soup3)
                    lenstr = ((len(strsoup3)))
                else:
                    html3 = get_ajax(ajaxhref2, ajaxId, HEADERSajax)
                    soup3 = BeautifulSoup(html3.text, 'html.parser').get_text
                    
                if lenstr == 31:
                    html3 = get_ajax(ajaxhref4, ajaxId, HEADERSajax)
                    soup3 = BeautifulSoup(html3.text, 'html.parser').get_text
                    strsoup3 = str(soup3)
                    lenstr = ((len(strsoup3)))
                else:
                    html3 = get_ajax(ajaxhref3, ajaxId, HEADERSajax)
                    soup3 = BeautifulSoup(html3.text, 'html.parser').get_text
                    
                if lenstr == 31:
                    html3 = get_ajax(ajaxhref5, ajaxId, HEADERSajax)
                    soup3 = BeautifulSoup(html3.text, 'html.parser').get_text
                    strsoup3 = str(soup3)
                    lenstr = ((len(strsoup3)))
                else:
                    html3 = get_ajax(ajaxhref4, ajaxId, HEADERSajax)
                    soup3 = BeautifulSoup(html3.text, 'html.parser').get_text
                

                catalog.append({
                    'hrefLot': hrefLot,
                    'numberProcedure': numberProcedure,
                    'numberEIS': numberEIS,
                    'customer': customer,
                    'nameProcedure': nameProcedure2,
                    'cost': cost,
                    'date': date,
                    'dateLast': dateLast,
                    'typeProcedure': typeProcedure,
                    'statusProcedure': statusProcedure,
                    'hiddenText': soup3,
                })        

            else:
                continue
               

    
            
    return catalog                    
            

            



# функция записи спарсенных значений в csv файл
def save_file(items, FILE):
    with open(FILE, 'a',  encoding='utf8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for item in items:
            writer.writerow([item['hrefLot'], item['numberProcedure'], item['numberEIS'], item['customer'], item['nameProcedure'], item['cost'], item['date'], item['dateLast'], item['typeProcedure'], item['statusProcedure'], item['hiddenText']])


def new_file(FILE):
    with open(FILE, 'a',  encoding='utf8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Ссылка на тендер', 'Номер процедуры', 'Номер извещения в ЕИС', 'Наименование заказчика', 'Наименование процедуры', 'Начальная цена процедуры','Дата публикации', 'Дата окончания подачи заявок', 'Тип процедуры', 'Статус процедуры', 'Скрытый текст'])

   
def make_all(links):
    print(f'Парсинг страницы {links} {len(links)}...')
    html = get_html(links)
    catalog = []
    catalog.extend(get_content(html.text))
    FILE = date + '.csv' 
    save_file(catalog, FILE)


    print(f'Получено {len(catalog)} товаров') 


# Основная функция Создаём каталог
def parse1():
    for URL in [
    
'http://t1.torgi223.ru/registry/list/'

    ]:

        html = get_html(URL)
        print(html)
        if html.status_code == 200:
            FILE = date + '.csv'   
            new_file(FILE)
            catalog = []
            pages_count = get_pages_count(html.text)
            links = []
            for page in range (1, pages_count + 1):
                href = 'http://t1.torgi223.ru/registry/list/?auth=1&page=' + str(page)       
                links.append(href)
             

            with Pool(20) as p:
                p.map(make_all, links)



        else:
            print('Error') 







parse1()
#parser2()



""" 'https://2676270.ru/catalog/yarn/92/',
'https://2676270.ru/catalog/yarn/93/',
'https://2676270.ru/catalog/yarn/1419/'
'https://2676270.ru/catalog/yarn/1677/',
'https://2676270.ru/catalog/yarn/2453/',
'https://2676270.ru/catalog/yarn/909/',
'https://2676270.ru/catalog/yarn/95/' 

while True:
    try:
        next_button = driver.find_element_by_id('oq-nav-nxt')
    except NoSuchElementException:
        break
    next_button.click()

                print(f'Парсинг страницы {page} {pages_count} {URL}...')
                html = get_html(URL, params={'page': page})
                catalog.extend(get_content(html.text))
                time.sleep(1)
            FILE = date + '.csv'   
            save_file(catalog, FILE)


            print(f'Получено {len(catalog)} товаров') 

while True:
    time.sleep(30)
    parse()
    
def make_all(links, catalog):
    html = get_html(link)
    catalog.extend(get_content(html.text))
    return catalog


# Основная функция Создаём каталог
def parse1():
    for URL in [
    
'http://t1.torgi223.ru/registry/list/'

    ]:

        html = get_html(URL)
        print(html)
        if html.status_code == 200:
            catalog = []
            pages_count = get_pages_count(html.text)
            links = []
            for page in range (1, pages_count + 1):
                href = 'http://t1.torgi223.ru/registry/list/?auth=1&page=' + str(page)       
                links.append(href)


            with Pool(2) as p:
                p.map(make_all, links)


            FILE = date + '.csv'   
            save_file(catalog, FILE)


            print(f'Получено {len(catalog)} товаров') 
        else:
            print('Error')  

# Функция срабатывает каждые сутки (86400 секунд)







parse1()
#parser2()    
    
    
    
    
    
    
    
    
    
    
    
    
    """
    