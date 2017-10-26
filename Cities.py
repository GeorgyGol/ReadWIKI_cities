import sys
import pandas as pd
import z_service
import re
from bs4 import BeautifulSoup
import requests

strWIKIpgt10k=r'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BF%D0%BE%D1%81%D1%91%D0%BB%D0%BA%D0%BE%D0%B2_%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D1%81%D0%BA%D0%BE%D0%B3%D0%BE_%D1%82%D0%B8%D0%BF%D0%B0_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8_%D1%81_%D0%BD%D0%B0%D1%81%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%D0%BC_%D0%B1%D0%BE%D0%BB%D0%B5%D0%B5_10_%D1%82%D1%8B%D1%81%D1%8F%D1%87_%D0%B6%D0%B8%D1%82%D0%B5%D0%BB%D0%B5%D0%B9'
strWikiMore10k=r'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BD%D0%B0%D1%81%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D1%8B%D1%85_%D0%BF%D1%83%D0%BD%D0%BA%D1%82%D0%BE%D0%B2_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8_%D1%81_%D0%BD%D0%B0%D1%81%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%D0%BC_%D0%B1%D0%BE%D0%BB%D0%B5%D0%B5_10_%D1%82%D1%8B%D1%81%D1%8F%D1%87_%D0%B6%D0%B8%D1%82%D0%B5%D0%BB%D0%B5%D0%B9'
strWikisela10r=r'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BA%D1%80%D1%83%D0%BF%D0%BD%D1%8B%D1%85_%D0%BD%D0%B0%D1%81%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D1%8B%D1%85_%D0%BF%D1%83%D0%BD%D0%BA%D1%82%D0%BE%D0%B2_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8,_%D0%BD%D0%B5_%D0%B8%D0%BC%D0%B5%D1%8E%D1%89%D0%B8%D1%85_%D1%81%D1%82%D0%B0%D1%82%D1%83%D1%81_%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%B0'
strWikiCities=r'https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D0%B0_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8'

def read_rosstat(strFile=r'C:\Documents and Settings\ggolyshev\PycharmProjects\Cities\Base\Tabl-31-17.csv'):
    def make_type(x):
        strRet=re.sub(x['city'], '', x['City'])
        strRet=re.sub('(\(рп\))|\s{2,}|(\.)', '', strRet).strip()
        return strRet

    dtf=pd.read_csv(strFile, encoding='cp1251', sep=';').dropna()
    dtf['Region']=dtf['Region'].apply(z_service.norm_region)
    dtf['city'] = dtf['City'].str.replace(r'(пгт\b)|(г\.)|(\(р?п\))|(посёлок)', '').str.strip()
    dtf['city']=dtf['city'].str.replace(r'\s?-\s?', '-')
    dtf['type'] = dtf[['City', 'city']].apply(make_type, axis=1)
    dtf['city'] = dtf['city'].str.replace(r'ё', 'е')

    return dtf

def read_city_info(strFile=r'C:\Documents and Settings\ggolyshev\PycharmProjects\Cities\Base\cities_info.csv'):
    lst=['href', 'name', 'people', 'reg','oktmo','square']
    dtf = pd.read_csv(strFile, encoding='cp1251', sep=';')
    return dtf[lst]

def read_regions(strFile=r'C:\Documents and Settings\ggolyshev\PycharmProjects\Cities\Base\regionsF.csv'):
    dtf = pd.read_csv(strFile, encoding='cp1251', sep=';')
    return dtf

def make_reg2city(dtfR, dtfC):
    def make_okato(x):
        if x>100: return z_service.codes_correct(str(x), iSize=5)
        else: return z_service.codes_correct(str(x), iSize=2)
    dtfR['reg_code']=dtfR['okato'].apply(make_okato)

    dtf=dtfC.join(dtfR.set_index('okato')[['norm_name', 'FederalDistrictID']], on='reg', lsuffix='_city', rsuffix='_reg')
    return dtf

def check_rosstat_wiki():
    dtfRS = read_rosstat()
    dtfWiki = read_city_info()
    dtfReg = read_regions()

    dtfCity = make_reg2city(dtfReg, dtfWiki)

    print(dtfRS.shape, dtfWiki.shape)
    print(dtfWiki.columns.tolist())
    # print(dtfReg)
    dtR = pd.merge(dtfCity, dtfRS, how='outer', indicator=True, left_on=['norm_name', 'name'],
                   right_on=['Region', 'city'])
    #print(dtR[dtR['_merge'] == 'both'][['name', 'city', 'people', 'People']])
    print(dtR.ix[(dtR['_merge'] == 'both') & (dtR['people']!=dtR['People']), ('name', 'people', 'People')])

def read_wiki_cities():
    req=requests.get(strWikiCities)
    soup=BeautifulSoup(req.text, 'html.parser')
    tbls=soup.find_all('table', attrs={'class':'collapsible'})[0:6]
    lst_cities=[]
    for tbl in tbls:
        trs=tbl.find_all('tr')
        for tr in trs[2:]:
            tds=tr.find_all('td')
            dct={'name':tds[1].text, 'href': r'https://ru.wikipedia.org' + tds[1].find('a')['href'], 'reg':tds[2].text,
                 'peaple_16': z_service.get_all_digits(tds[3].text),
                 'people_15': z_service.get_all_digits(tds[4].text), 'type':'город'}
            lst_cities.append(dct)
    dtfCities=pd.DataFrame(lst_cities)
    dtfCities['norm_reg']=dtfCities['reg'].apply(z_service.norm_region)
    dtfCities['norm_name']=dtfCities['name'].str.replace(r'(?i)ё', 'е')
    return dtfCities

def read_wiki_10k():
    # strWikiMore10k
    req=requests.get(strWikiMore10k)
    soup=BeautifulSoup(req.text, 'html.parser')
    tbls=soup.find_all('table')
    lst_cities = []
    trs = tbls[-1].find_all('tr')

    for tr in trs[2:]:
        tds = tr.find_all('td')
        dct = {'name': tds[1].text, 'href': r'https://ru.wikipedia.org' + tds[1].find('a')['href'],
               'reg': tds[3].text,
               'peaple_16': z_service.get_all_digits(tds[7].text),
               'people_15': z_service.get_all_digits(tds[6].text), 'type': tds[2].text.lower()}
        lst_cities.append(dct)

    dtfNP = pd.DataFrame(lst_cities)
    dtfNP['norm_reg'] = dtfNP['reg'].apply(z_service.norm_region)
    dtfNP['norm_name'] = dtfNP['name'].str.replace(r'(?i)ё', 'е')
    return dtfNP


def main1():
    dtf1=read_wiki_cities()
    lst_cols=dtf1.columns.tolist()

    dtf2=read_wiki_10k()
    msk=dtf2['type']=='город'

    dtf=pd.merge(dtf1, dtf2, on=['norm_name', 'norm_reg'], how='outer', indicator=True)
    lst_cols_m=[i for i in dtf.columns.tolist() if i.endswith('_y')]+ ['norm_reg', 'norm_name']
    d_add=dtf.ix[(dtf['_merge']=='right_only')][lst_cols_m].rename(columns=dict(zip(lst_cols_m, lst_cols)))

    d_res=dtf1.append(d_add).reset_index(drop=True)
    print(d_res)
    d_res.to_csv('wiki_NPs.csv', encoding='cp1251', sep=';')

    #print(dtf.ix[(dtf['_merge']=='right_only')] )
    #dtf.to_csv('wiki_svod.csv', encoding='cp1251', sep=';')
    #print(dict(zip(lst_cols, lst_cols_m)))

if __name__ == "__main__":
    sys.exit(main())


