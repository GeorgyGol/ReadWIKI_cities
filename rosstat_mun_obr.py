import sys
import pandas as pd
import sqlite3

import z_service
import re

# parse file C:\Documents and Settings\ggolyshev\PycharmProjects\Cities\Base\Tabl-36-17.xls

def Read_Excel(strFile=r'C:\Documents and Settings\ggolyshev\PycharmProjects\Cities\Base\Tabl-36-17.xls'):
    def correct_oktmo(x):
        x=str(x)
        if len(x)>10:
            return x[:-4]
        else:
            return z_service.codes_correct(x[:-2], iSize=8)

    pdf=pd.read_excel(strFile, sheetname=1, header=1, skiprows =list(range(4))+[7],
                      na_values=0, converters ={0:correct_oktmo}).dropna(how='all')
    pdf.rename(columns={'ТЕРСОН-МО':'oktmo', 'Оценка численности постоянного населения на 1 января 2017г.':'name',
                        'население':'people', 'городское':'city_people', 'сельское':'country_people'}, inplace=True)

    #pdf['oktmo']=pdf['oktmo_rs'].apply(correct_oktmo)
    conn = sqlite3.connect(r'cities.sqlite')
    #pdReg = pd.read_sql('select * from Regions', conn)
    #stRegs=set(pdReg['norm_name'].tolist())

    pdf.to_sql('MunObrsPeople2017', conn, if_exists='replace',
                  index=False, dtype={'oktmo':'TEXT', 'name':'TEXT',
                                      'people':'INTEGER', 'city_people':'INTEGER', 'country_people':'INTEGER'})

    #pdf['Reg']=pdf[]
    return pdf


def main():
    p=Read_Excel()
    print(p.ix[p['oktmo'].str.len()>8])


if __name__ == "__main__":
    sys.exit(main())