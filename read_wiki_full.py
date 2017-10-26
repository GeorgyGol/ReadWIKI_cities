import sys
import pandas as pd
import z_service
import re
from bs4 import BeautifulSoup
import requests

def read_csv():
    pdf=pd.read_csv(r'C:\Documents and Settings\ggolyshev\PycharmProjects\Cities\Base\full_cities_info.csv',
                    sep=';', encoding='cp1251', dtype={'lat':float, 'long':float, 'oktmo':str,
                                                       'people':int, 'reg':float, 'square':float})
    return  pdf

def get_code(strX):
    return re.search(r'(\d+)', strX.replace(' ', '')).group(0)

def get_num(strX, to_type=int):
    strT=re.sub(r'\s', '', strX).replace(',', '.')
    return to_type(re.search(r'\d+\.?\d*', strT).group(0))

def read_page(strURL):
    req = requests.get(strURL)
    soup = BeautifulSoup(req.text, 'html.parser')
    tbl_Card=soup.find('table', class_='infobox vcard')
    trs=tbl_Card.find_all('tr')

    dct_ret={'people':0, 'oktmo':'', 'okato':'', 'square':0, 'href':strURL,
             'height':0, 'post_index':'', 'timezone':'', 'phone_code':'', 'desnity':0}

    for tr in trs:
        tds=tr.find_all('td')
        ths=tr.find_all('th')
        if len(ths)>0:
            try:
                if re.search(r'(?i)координаты', ths[0].text):
                    dct_ret.update(z_service.make_coords(tds[0].text))
                    #print('coord - ', z_service.make_coords(tds[0].text))
                if re.search(r'(?i)население', ths[0].text):
                    try:
                        dct_ret['people']=get_num(tds[0].text)
                    except ValueError:
                        dct_ret['people'] = int(get_num(tds[0].text, to_type=float) * 1000)
                    #print('people - ', get_num(tds[0].text))
                if re.search(r'(?i)ОКТМО', ths[0].text):
                    dct_ret['oktmo']=z_service.codes_correct(get_code(tds[0].text), iSize=11)
                    #print('oktmo - ', z_service.codes_correct(get_code(tds[0].text), iSize=11))
                if re.search(r'(?i)Площадь', ths[0].text):
                    try:
                        dct_ret['square']=get_num(tds[0].text, to_type=float)
                    except:
                        dct_ret['square'] = 0
                    #print('square - ', get_num(tds[0].text, float))
                if re.search(r'(?i)Высота', ths[0].text):
                    dct_ret['height']=get_num(tds[0].text.strip(), to_type=float)
                    #print('height - ', get_code(tds[0].text.strip(), float))
                if re.search(r'(?i)Почтовый индекс', ths[0].text):
                    dct_ret['post_index']=tds[0].text.strip()
                    #print('post - ', tds[0].text.strip())
                if re.search(r'(?i)ОКАТО', ths[0].text):
                    dct_ret['okato']=tds[0].text.strip()
                    #print('okato - ', tds[0].text.strip())
                if re.search(r'(?i)Часовой пояс', ths[0].text):
                    dct_ret['timezone']=tds[0].text.strip()
                    #print('hours - ', tds[0].text.strip())
                if re.search(r'(?i)Телефонный код', ths[0].text):
                    dct_ret['phone_code']=tds[0].text.strip()
                    #print('phone - ', tds[0].text.strip())
                if re.search(r'(?i)Плотность', ths[0].text):
                    try:
                        dct_ret['desnity']=get_num(tds[0].text, float)
                    except:
                        dct_ret['desnity'] = 0
                    #print('dens - ', get_num(tds[0].text, float))
            except AttributeError:
                print(strURL)
                sys.exit(-1)

    return dct_ret




def main():
    pdfCities=read_csv()
    lst_end=[]
    for k, i in pdfCities.iterrows():
        print('Ind = {0}, NAME = {1}, href = {2}'.format(k, i['name'], i['href']))
        try:
            dct={'name': i['name'], 'norm_name': i['norm_name'],
                        'norm_reg':i['norm_reg']}
            dct.update(read_page(i['href']))
            lst_end.append(dct)

        except AttributeError:
            print('error for NAME ', i['name'])


    pdf=pd.DataFrame(lst_end)
    pdf.to_csv('work.csv', sep=';', encoding='cp1251')
    print(pdf)

if __name__ == "__main__":
    sys.exit(main())
