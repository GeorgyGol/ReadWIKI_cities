import re
from itertools import repeat
import numpy as np

__version__= 1.0

def codes_correct(x, iSize=8, iFill='0'):
    """ Make right form for formal codes like OKATO - string codes from digits chars """
    if type(x) is float:
        return x
    return '{:{fill}>{size}}'.format(x.replace('\n', '')[:iSize], fill=iFill, size=iSize)

def get_all_digits(strX, convert_to=int):
    """ Make number from string with digits, spaces, footnote symbols: 123 345[1] - > 12345"""
    try:
        return convert_to(''.join(re.findall(r'(\d+)(?:\[.+\])*', strX)))
    except ValueError:
        return 0

def norm_region(strReg, do_split=True):
    """ Normalize region name """
    #print(strReg)
    if re.search(r'(?i)Хант[ыэе]-Мансийск[^\b]', strReg):
        return 'Югра'
    if re.search(r'(?i)осетия\b.*', strReg):
        return 'Алания'
    if re.search(r'Якутия', strReg):
        return 'Саха'

    strS=re.sub(r'(?i)^(обл\w*|\.?\b)', '', strReg)
    strS=re.sub(r'(?i)^(респ\w*|\.?\b)', '', strS).strip()
    #strS=re.sub(r'(?i)^(гор\w*|\.?\b)', '', strS).strip()
    strS=re.sub(r'(?i)^(край\b)', '', strS).strip()
    
    strS=re.sub(r'(?i)ингуш\w*|\.\b', 'Ингушетия', strS)
    strS=re.sub(r'(?i)удмурт\w*|\.\b', 'Удмуртия', strS)
    strS=re.sub(r'Чеч\w*|\.\b', 'Чечня', strS)
    strS=re.sub(r'Чуваш\w*|\.\b', 'Чувашия', strS)
    strS=re.sub(r'Морд\w*|\.\b', 'Мордовия', strS)
    strS=re.sub(r'(?i)Балкарская', 'Балкария', strS)
    strS=re.sub(r'(?i)Черкесская', 'Черкесия', strS)
    if do_split:
        try:
            return re.search(r'([\w-]+)\s*', strS).group().title().strip()
        except AttributeError:
            pass
    return strS.strip()

def make_coords(xGrad):
    str_t=xGrad
    mtch=list(filter(None, re.findall(r'(\d{,2})', str_t)))
    half=int(len(mtch)/2)
    lst_lat=list(map(float, mtch[:half]))+list(repeat(0, 3-half))
    lst_long=list(map(float, mtch[half:]))+list(repeat(0, 3-half))
    
    latitude=lst_lat[0]+lst_lat[1]/60 + lst_lat[2]/3600
    longitude=lst_long[0]+lst_long[1]/60 + lst_long[2]/3600
    return {'lat':latitude, 'long': longitude}

def convert_to_float(strT):
    d=re.search(r'(\d+\.?\d*)', strT.replace(' ', '').replace(',', '.'))
    return float(d.group())
