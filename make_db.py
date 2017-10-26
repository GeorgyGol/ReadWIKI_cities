import sys
import pandas as pd
import sqlite3
import z_service

def make_fedtbl(sq_conn):
    dtfReg=pd.read_csv(r'C:\Documents and Settings\ggolyshev\PycharmProjects\Cities\Base\regionsF.csv',
                       sep=';', encoding='cp1251')
    dtfFO=dtfReg[['FederalDistrictName', 'FederalDistrictID']].drop_duplicates(['FederalDistrictName', 'FederalDistrictID'])
    dtfFO.rename(columns={'FederalDistrictName':'name', 'FederalDistrictID':'ID'}, inplace=True)
    dtfFO.to_sql('FDistricts', sq_conn, if_exists='replace', index_label='ID',
                 index=False, dtype={'name':'TEXT', 'ID':'INTEGER'})
    return dtfFO

def make_cities_db(sq_conn):
    dtfCities=pd.read_csv(r'C:\Documents and Settings\ggolyshev\PycharmProjects\Cities\Base\info.csv',
                       sep=';', encoding='cp1251')[['norm_name', 'name', 'norm_reg', 'href', 'lat', 'long', 'okato',
                       'oktmo', 'people', 'square', 'height', 'phone_code', 'post_index', 'timezone']]
    dtfCities['oktmo']=dtfCities['oktmo'].apply(lambda x: z_service.codes_correct(x, iSize=11))

    dtfCities.to_sql('Localities', sq_conn, if_exists='replace', index_label='oktmo',
                 index=False, dtype={'norm_name':'TEXT', 'name':'TEXT', 'norm_reg':'TEXT', 'href':'TEXT',
                                     'lat':'REAL', 'long':'REAL', 'okato':'TEXT',
                       'oktmo':'TEXT', 'people':'INTEGER', 'square':'REAL', 'height':'REAL',
                                     'phone_code':'TEXT', 'post_index':'TEXT', 'timezone':'TEXT'})
    return dtfCities


def connect(strDBName):
    return sqlite3.connect(strDBName)

def make_vliages_db(con):
    dtfVil=pd.read_csv(r'C:\Documents and Settings\ggolyshev\PycharmProjects\Cities\Base\villages_info.csv',
                       sep=';', encoding='cp1251', dtype=str)[['name', 'okato1', 'okato2', 'oktmo', 'name2',
                                                               'oktmo_parent', 'name_parent', 'type', 'norm_name']]

    dtfVil=dtfVil.drop(dtfVil[dtfVil['oktmo'].isnull()].index)
    msk=dtfVil['oktmo'].str.len()==11

    dtfVil[msk].to_sql('All_Places', con, if_exists='replace', index_label='oktmo',
                     index=False, dtype={'name': 'TEXT', 'okato1': 'TEXT', 'okato2': 'TEXT', 'oktmo':
                                          'TEXT', 'name2': 'TEXT', 'oktmo_parent': 'TEXT',
                                           'name_parent': 'TEXT', 'type': 'TEXT', 'norm_name': 'TEXT'})

    return dtfVil[msk]

def make_munobr_db(con):
    dtfVil = pd.read_csv(r'C:\Documents and Settings\ggolyshev\PycharmProjects\Cities\Base\villages_info.csv',
                         sep=';', encoding='cp1251', dtype=str)[['name', 'okato1', 'okato2', 'oktmo', 'name2',
                                                                 'oktmo_parent', 'name_parent', 'type', 'norm_name']]

    dtfVil = dtfVil.drop(dtfVil[dtfVil['oktmo'].isnull()].index)
    msk = dtfVil['oktmo'].str.len() == 11

    #sign_budget
    #oktmo_budget
    #name_budget
    dtfRet = pd.read_csv(r'C:\Documents and Settings\ggolyshev\PycharmProjects\Cities\Base\munobr01042016.csv',
                         sep=';', encoding='cp1251', dtype=str)[['name', 'type', 'okato', 'oktmo', 'name2',
                                                                 'sign_budget', 'oktmo_budget', 'name_budget',
                                                                 'oktmo_parent', 'name_parent']]

    lst=dtfRet.columns.tolist()
    lstT=['TEXT'] * len(lst)

    dtfRet=dtfRet.append(dtfVil[~msk])
    dtfRet.to_sql('MunObrs', con, if_exists='replace',
                       index=False, dtype=dict(zip(lst, lstT)))

    return dtfRet

def main():
    conn = connect(r'cities.sqlite')
    pdf=pd.read_sql('select * from All_Places', conn)
    print(pdf)
    #print(make_munobr_db(conn).shape)
    #print(make_vliages_db(conn))
    #print(make_cities_db(conn).shape)
    #print(make_fedtbl(conn))

if __name__ == "__main__":
    sys.exit(main())