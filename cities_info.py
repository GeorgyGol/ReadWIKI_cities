import sys
import pandas as pd
import z_service
import re
from bs4 import BeautifulSoup
import requests

def main1():
    dtf1=pd.read_csv(r'C:\Documents and Settings\ggolyshev\PycharmProjects\Cities\Base\cities_info.csv',
                     sep=';', encoding='cp1251', dtype={'oktmo':str, 'reg':int})
    dtf2=pd.read_csv(r'C:\Documents and Settings\ggolyshev\PycharmProjects\Cities\wiki_NPs.csv',
                     sep=';', encoding='cp1251')
    dtfReg=pd.read_csv(r'C:\Documents and Settings\ggolyshev\PycharmProjects\Cities\Base\regionsF.csv',
                     sep=';', encoding='cp1251', dtype={'okato':int})

    print(dtf1['reg'].dtype, dtfReg['okato'].dtype)
    lst_end=['href', 'name_x', 'people', 'reg', 'lat', 'long', 'oktmo', 'phone_code', 'post_ind',
            'square', 'timezone', 'norm_name', 'name_y']
    dtf = pd.merge(dtf1, dtfReg[['norm_name', 'name', 'okato']], left_on='reg', right_on='okato', how='left')[lst_end]
    dtf=dtf.rename(columns={'name_y':'name_reg', 'name_x': 'name', 'norm_name':'norm_reg'})
    dtf['norm_name']=dtf['name'].str.replace(r'(?i)ё', 'е')

    print(dtf.columns.tolist())

    #print(sorted(dtf2['norm_reg'].unique().tolist()))
    dtf_res=pd.merge(dtf, dtf2, on=['norm_name', 'norm_reg'], how='outer', indicator=True)
    dtf_res=dtf_res[dtf_res['_merge']=='right_only'][['norm_reg', 'name_reg', 'norm_name', 'href_y', 'name_y',
                                                      'peaple_16', 'people_15', 'reg_y']]
    dtf_res['norm_reg']=dtf_res['reg_y'].apply(z_service.norm_region)

    print(dtf_res)
    dtf_res.to_csv('wiki_svod.csv', encoding='cp1251', sep=';')


def main2():
    dtf1 = pd.read_csv(r'C:\Documents and Settings\ggolyshev\PycharmProjects\Cities\Base\cities_info.csv',
                       sep=';', encoding='cp1251', dtype={'oktmo': str, 'reg': int})
    dtfReg = pd.read_csv(r'C:\Documents and Settings\ggolyshev\PycharmProjects\Cities\Base\regionsF.csv',
                         sep=';', encoding='cp1251', dtype={'okato': int})

    lst_end = ['href', 'name_x', 'people', 'reg', 'lat', 'long', 'oktmo', 'phone_code', 'post_ind',
               'square', 'timezone', 'norm_name', 'name_y']
    dtf = pd.merge(dtf1, dtfReg[['norm_name', 'name', 'okato']], left_on='reg', right_on='okato', how='left')[lst_end]
    dtf = dtf.rename(columns={'name_y': 'name_reg', 'name_x': 'name', 'norm_name': 'norm_reg'})
    dtf['norm_name'] = dtf['name'].str.replace(r'(?i)ё', 'е')

    dtf_add=pd.read_csv(r'C:\Documents and Settings\ggolyshev\PycharmProjects\Cities\wiki_svod.csv',
                        encoding='cp1251', sep=';')
    dtf_res=dtf.append(dtf_add).reset_index(drop=True)
    print(dtf_res)
    dtf_res.to_csv('full_cities_info.csv', encoding='cp1251', sep=';')

if __name__ == "__main__":
    sys.exit(main())